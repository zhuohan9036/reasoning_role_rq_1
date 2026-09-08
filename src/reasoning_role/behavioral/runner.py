"""Behavioral evaluation orchestration, checkpointing, and CLI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from reasoning_role.data.io import sha256_file
from reasoning_role.tasks.schema import CanonicalInstance, canonical_json, stable_digest

from .backends.base import InferenceBackend
from .backends.fake import FakeBackend
from .backends.huggingface import HuggingFaceBackend
from .parsing import score_completion
from .provenance import code_provenance, environment_provenance, load_dataset_records
from .schema import (
    EVALUATION_SCHEMA_VERSION,
    BackendResult,
    EvaluationRecord,
    InferenceRequest,
)
from .summary import summarize, write_summary_csv


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def load_evaluation_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError("evaluation configuration root must be a mapping")
    return value


def validate_evaluation_config(config: Mapping[str, Any]) -> None:
    required = {"evaluation_schema_version", "seed", "dataset", "backend", "generation", "summary", "eligibility"}
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"evaluation configuration is missing: {missing}")
    if str(config["evaluation_schema_version"]) != EVALUATION_SCHEMA_VERSION:
        raise ValueError("unsupported evaluation_schema_version")
    if not isinstance(config["seed"], int):
        raise ValueError("evaluation seed must be an integer")
    if not isinstance(config["dataset"], dict) or not config["dataset"].get("manifest"):
        raise ValueError("dataset.manifest is required")
    backend = config["backend"]
    if not isinstance(backend, dict) or backend.get("kind") not in {"fake", "huggingface"}:
        raise ValueError("backend.kind must be fake or huggingface")
    generation = config["generation"]
    if generation.get("do_sample", False):
        raise ValueError("behavioral calibration v1 requires greedy decoding")
    if int(generation.get("batch_size", 0)) < 1:
        raise ValueError("generation.batch_size must be positive")
    if int(generation.get("max_new_tokens", 0)) < 1:
        raise ValueError("generation.max_new_tokens must be positive")
    strata = config["summary"].get("strata")
    if not isinstance(strata, list) or not strata:
        raise ValueError("summary.strata must be a non-empty list")
    for field in (
        "overall_trimmed_exact_min",
        "each_chain_length_trimmed_exact_min",
        "invalid_or_inference_failure_max",
    ):
        value = float(config["eligibility"][field])
        if value < 0 or value > 1:
            raise ValueError(f"eligibility threshold {field} must be in [0, 1]")


def run_evaluation(
    config: Mapping[str, Any],
    output_dir: str | Path,
    *,
    resume: bool = False,
    backend: InferenceBackend | None = None,
    code_revision: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validate_evaluation_config(config)
    records, dataset_identity = load_dataset_records(config["dataset"])
    config_hash = hashlib.sha256(canonical_json(config).encode("utf-8")).hexdigest()
    code_identity = code_provenance(REPOSITORY_ROOT, code_revision)
    preflight = {
        "evaluation_schema_version": EVALUATION_SCHEMA_VERSION,
        "config_sha256": config_hash,
        "dataset": dataset_identity,
        "code": code_identity,
    }
    preflight_hash = hashlib.sha256(
        canonical_json(preflight).encode("utf-8")
    ).hexdigest()

    destination = Path(output_dir)
    state_path = destination / "run_state.json"
    records_path = destination / "records.jsonl"
    if destination.exists() and not resume:
        raise FileExistsError(f"output directory already exists: {destination}")
    if resume and not destination.exists():
        raise FileNotFoundError("cannot resume a missing output directory")
    if resume:
        if not state_path.is_file():
            raise ValueError("resume requires run_state.json")
        old_state = json.loads(state_path.read_text(encoding="utf-8"))
        if old_state.get("preflight_sha256") != preflight_hash:
            raise ValueError("resume provenance mismatch")
    else:
        destination.mkdir(parents=True, exist_ok=False)

    active_backend = backend or _build_backend(config)
    try:
        backend_metadata = dict(active_backend.prepare())
        full_identity = {**preflight, "backend": backend_metadata}
        run_id = "behavioral:" + stable_digest(
            full_identity, prefix="behavioral-run", length=32
        )
        state = {
            "run_id": run_id,
            "preflight_sha256": preflight_hash,
            "full_identity_sha256": hashlib.sha256(
                canonical_json(full_identity).encode("utf-8")
            ).hexdigest(),
            "identity": full_identity,
        }
        if resume:
            old_state = json.loads(state_path.read_text(encoding="utf-8"))
            if old_state != state:
                raise ValueError("resume backend identity mismatch")
        else:
            _atomic_write_json(state_path, state)

        completed = _load_existing_records(records_path, run_id) if resume else []
        source_by_id = {record.instance_id: record for record in records}
        completed_by_id = {record.instance_id: record for record in completed}
        unknown = sorted(set(completed_by_id) - set(source_by_id))
        if unknown:
            raise ValueError(f"resume contains unknown instance IDs: {unknown[:3]}")

        pending = [record for record in records if record.instance_id not in completed_by_id]
        batch_size = int(config["generation"]["batch_size"])
        evaluated = list(completed)
        for start in range(0, len(pending), batch_size):
            source_batch = pending[start : start + batch_size]
            requests = [_make_request(record, config_hash) for record in source_batch]
            for request in requests:
                request.validate()
            backend_results = list(active_backend.generate(requests))
            _validate_backend_results(requests, backend_results)
            for source, request, result in zip(source_batch, requests, backend_results):
                result.validate()
                evaluated.append(
                    _make_evaluation_record(
                        source=source,
                        request=request,
                        result=result,
                        run_id=run_id,
                        dataset_sha256=dataset_identity["selection_sha256"],
                        backend_metadata=backend_metadata,
                    )
                )
            evaluated.sort(key=lambda item: (item.split, item.instance_id))
            _atomic_write_records(records_path, evaluated)

        expected_ids = {record.instance_id for record in records}
        actual_ids = [record.instance_id for record in evaluated]
        if len(actual_ids) != len(set(actual_ids)):
            raise ValueError("evaluation output contains duplicate instance IDs")
        if set(actual_ids) != expected_ids:
            missing = sorted(expected_ids - set(actual_ids))
            raise ValueError(f"evaluation output is missing instances: {missing[:3]}")

        summary = summarize(
            evaluated,
            strata=[str(value) for value in config["summary"]["strata"]],
            eligibility=config["eligibility"],
        )
        summary_path = destination / "summary.json"
        _atomic_write_json(summary_path, summary)
        csv_path = destination / "summary.csv"
        write_summary_csv(csv_path, summary)
        run_manifest = {
            "evaluation_schema_version": EVALUATION_SCHEMA_VERSION,
            "run_id": run_id,
            "identity": full_identity,
            "environment": environment_provenance(
                ["reasoning-role", "PyYAML", "torch", "transformers", "accelerate"]
            ),
            "attempted": len(records),
            "completed": len(evaluated),
            "files": {
                path.name: {"sha256": sha256_file(path)}
                for path in (state_path, records_path, summary_path, csv_path)
            },
            "eligibility": summary["eligibility"],
            "scientific_interpretation": "behavioral calibration only",
        }
        _atomic_write_json(destination / "run_manifest.json", run_manifest)
        return run_manifest
    finally:
        active_backend.close()


def _build_backend(config: Mapping[str, Any]) -> InferenceBackend:
    backend_config = {**config["backend"], **config["generation"]}
    if backend_config["kind"] == "fake":
        return FakeBackend(backend_config)
    return HuggingFaceBackend(backend_config)


def _make_request(record: CanonicalInstance, config_hash: str) -> InferenceRequest:
    return InferenceRequest(
        request_id="request:" + stable_digest(
            [record.instance_id, config_hash], prefix="behavioral-request"
        ),
        instance_id=record.instance_id,
        prompt=record.prompt,
        expected_answer=record.target,
        family=record.family,
        answer_encoding=str(record.nuisance_factors["answer_encoding"]),
        nuisance_factors=dict(record.nuisance_factors),
    )


def _validate_backend_results(
    requests: Sequence[InferenceRequest], results: Sequence[BackendResult]
) -> None:
    expected = [request.request_id for request in requests]
    actual = [result.request_id for result in results]
    if actual != expected:
        raise ValueError(
            "backend results must contain exactly one result per request in request order"
        )


def _make_evaluation_record(
    *,
    source: CanonicalInstance,
    request: InferenceRequest,
    result: BackendResult,
    run_id: str,
    dataset_sha256: str,
    backend_metadata: Mapping[str, Any],
) -> EvaluationRecord:
    metrics = score_completion(
        expected=request.expected_answer,
        completion=result.completion,
        family=request.family,
        answer_encoding=request.answer_encoding,
        error_code=result.error_code,
    )
    record = EvaluationRecord(
        schema_version=EVALUATION_SCHEMA_VERSION,
        run_id=run_id,
        request_id=request.request_id,
        instance_id=request.instance_id,
        family=request.family,
        split=source.split,
        nuisance_factors=dict(request.nuisance_factors),
        dataset_sha256=dataset_sha256,
        model_id=str(backend_metadata["model_id"]),
        model_revision=str(backend_metadata["model_revision"]),
        tokenizer_id=str(backend_metadata["tokenizer_id"]),
        tokenizer_revision=str(backend_metadata["tokenizer_revision"]),
        prompt_mode=str(backend_metadata["prompt_mode"]),
        input_text=result.input_text,
        input_sha256=hashlib.sha256(result.input_text.encode("utf-8")).hexdigest(),
        expected_answer=request.expected_answer,
        raw_completion=result.completion,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
        latency_ms=result.latency_ms,
        error_code=result.error_code,
        error_message=result.error_message,
        **metrics,
    )
    record.validate()
    return record


def _load_existing_records(path: Path, run_id: str) -> list[EvaluationRecord]:
    if not path.exists():
        return []
    records: list[EvaluationRecord] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            record = EvaluationRecord.from_dict(json.loads(line))
            if record.run_id != run_id:
                raise ValueError(f"run ID mismatch at records line {line_number}")
            if record.instance_id in seen:
                raise ValueError(f"duplicate instance ID at records line {line_number}")
            seen.add(record.instance_id)
            records.append(record)
    return records


def _atomic_write_records(path: Path, records: Sequence[EvaluationRecord]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(canonical_json(record.to_dict()))
            handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def _atomic_write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(rendered)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run model-output-only behavioral calibration."
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--resume", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = run_evaluation(
        load_evaluation_config(args.config), args.output, resume=args.resume
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "attempted": manifest["attempted"],
                "completed": manifest["completed"],
                "run_id": manifest["run_id"],
                "manifest": str(Path(args.output) / "run_manifest.json"),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
