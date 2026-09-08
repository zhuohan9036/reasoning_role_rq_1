"""Deterministic, strictly balanced task-calibration data generation."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform
import random
from typing import Any, Mapping, Sequence

import yaml

from reasoning_role import __version__
from reasoning_role.tasks.registry import get_task_family
from reasoning_role.tasks.schema import (
    SCHEMA_VERSION,
    CanonicalInstance,
    canonical_json,
    stable_digest,
    validate_records,
)

from .io import detect_code_revision, sha256_file, write_json, write_jsonl
from .split import (
    assert_disjoint_semantic_id,
    audit_split_overlaps,
    expand_factor_cells,
    validate_holdout_axes,
)


def load_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError("configuration root must be a mapping")
    return value


def validate_config(config: Mapping[str, Any]) -> None:
    required = {"schema_version", "generator_version", "seed", "families", "splits"}
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"configuration is missing required fields: {missing}")
    if str(config["schema_version"]) != SCHEMA_VERSION:
        raise ValueError(
            f"configuration schema_version must be {SCHEMA_VERSION!r}"
        )
    if not isinstance(config["seed"], int):
        raise ValueError("seed must be an integer")
    if not isinstance(config["generator_version"], str):
        raise ValueError("generator_version must be a string")

    families = config["families"]
    splits = config["splits"]
    if not isinstance(families, dict) or not families:
        raise ValueError("families must be a non-empty mapping")
    if not isinstance(splits, dict) or not splits:
        raise ValueError("splits must be a non-empty mapping")
    family_names = sorted(str(name) for name in families)

    for family_name in family_names:
        family = get_task_family(family_name)
        family_spec = families[family_name]
        if not isinstance(family_spec, dict):
            raise ValueError(f"family {family_name!r} settings must be a mapping")
        if family.generator_version != str(config["generator_version"]):
            raise ValueError(
                f"family {family_name!r} generator version "
                f"{family.generator_version!r} does not match configuration"
            )

    for split_name, split_spec in splits.items():
        if not isinstance(split_spec, dict):
            raise ValueError(f"split {split_name!r} must be a mapping")
        count = split_spec.get("count_per_family")
        if not isinstance(count, int) or count <= 0:
            raise ValueError(
                f"split {split_name!r} count_per_family must be a positive integer"
            )
        factors = split_spec.get("factors")
        render = split_spec.get("render")
        if not isinstance(factors, dict) or not isinstance(render, dict):
            raise ValueError(f"split {split_name!r} needs factors and render mappings")
        for factor_name in (
            "chain_lengths",
            "distractor_counts",
            "presentation_orders",
        ):
            values = factors.get(factor_name)
            if not isinstance(values, list) or not values:
                raise ValueError(
                    f"split {split_name!r} factor {factor_name!r} must be a non-empty list"
                )
        if any(int(value) < 1 for value in factors["chain_lengths"]):
            raise ValueError("chain lengths must be positive")
        if any(int(value) < 0 for value in factors["distractor_counts"]):
            raise ValueError("distractor counts must be non-negative")
        if any(
            value not in {"canonical", "shuffled"}
            for value in factors["presentation_orders"]
        ):
            raise ValueError("presentation orders must be canonical or shuffled")

        for family_name in family_names:
            family = get_task_family(family_name)
            options = render.get(family_name)
            if not isinstance(options, dict):
                raise ValueError(
                    f"split {split_name!r} has no render settings for {family_name!r}"
                )
            supported_fields = (
                ("templates", family.supported_templates),
                ("vocabularies", family.supported_vocabularies),
                ("answer_encodings", family.supported_answer_encodings),
            )
            for option_name, supported in supported_fields:
                values = options.get(option_name)
                if not isinstance(values, list) or not values:
                    raise ValueError(
                        f"{split_name}.{family_name}.{option_name} must be a non-empty list"
                    )
                unsupported = sorted(set(values) - set(supported))
                if unsupported:
                    raise ValueError(
                        f"unsupported {option_name} for {family_name!r}: {unsupported}"
                    )
            cell_count = len(expand_factor_cells(split_spec, family_name))
            if count % cell_count:
                raise ValueError(
                    f"split {split_name!r} count_per_family={count} is not divisible "
                    f"by its {cell_count} requested factor cells for {family_name!r}"
                )

    validate_holdout_axes(splits, family_names)


def derive_seed(global_seed: int, *parts: Any) -> int:
    payload = canonical_json([global_seed, *parts]).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def generate_dataset(
    config: Mapping[str, Any],
    output_dir: str | Path,
    *,
    code_revision: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate all configured splits into a new output directory."""

    validate_config(config)
    resolved_config = deepcopy(dict(config))
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=False)
    max_attempts = int(config.get("max_generation_attempts", 1_000))
    if max_attempts < 1:
        raise ValueError("max_generation_attempts must be positive")

    records_by_split: dict[str, list[CanonicalInstance]] = {}
    semantic_assignments: dict[str, str] = {}
    target_verified = 0

    for split_name, split_spec in config["splits"].items():
        split_records: list[CanonicalInstance] = []
        for family_name in sorted(config["families"]):
            family = get_task_family(family_name)
            cells = expand_factor_cells(split_spec, family_name)
            repetitions = int(split_spec["count_per_family"]) // len(cells)
            for cell_index, cell in enumerate(cells):
                for repetition in range(repetitions):
                    record: CanonicalInstance | None = None
                    for attempt in range(max_attempts):
                        rng = random.Random(
                            derive_seed(
                                int(config["seed"]),
                                split_name,
                                family_name,
                                cell_index,
                                repetition,
                                attempt,
                            )
                        )
                        task = family.generate(
                            rng,
                            chain_length=int(cell["chain_length"]),
                            distractor_count=int(cell["distractor_count"]),
                            presentation_order=str(cell["presentation_order"]),
                            settings=config["families"][family_name],
                        )
                        semantic_id = f"{family_name}:" + stable_digest(
                            task.semantic_payload, prefix=f"{family_name}:semantic"
                        )
                        if semantic_id in semantic_assignments:
                            continue

                        verified_target = family.solve(task.canonical_problem)
                        if verified_target != task.canonical_target:
                            raise ValueError(
                                f"reference solver disagrees with generated target for {family_name}"
                            )
                        final_state_values = list(
                            task.task_side_trace[-1].output_state.values()
                        )
                        if final_state_values != [task.canonical_target]:
                            raise ValueError(
                                f"task-side trace disagrees with generated target for {family_name}"
                            )
                        rendered = family.render(
                            task,
                            template_id=str(cell["template_id"]),
                            vocabulary_id=str(cell["vocabulary_id"]),
                            answer_encoding=str(cell["answer_encoding"]),
                        )
                        nuisance_factors = {**cell, **task.family_factors}
                        canonical_problem_hash = stable_digest(
                            task.canonical_problem,
                            prefix=f"{family_name}:canonical_problem",
                            length=32,
                        )
                        prompt_hash = stable_digest(
                            rendered.prompt,
                            prefix=f"{family_name}:prompt",
                            length=32,
                        )
                        instance_id = f"{family_name}:" + stable_digest(
                            {
                                "semantic_id": semantic_id,
                                "nuisance_factors": nuisance_factors,
                                "canonical_problem_hash": canonical_problem_hash,
                            },
                            prefix=f"{family_name}:instance",
                        )
                        record = CanonicalInstance(
                            schema_version=SCHEMA_VERSION,
                            instance_id=instance_id,
                            family=family_name,
                            generator_version=family.generator_version,
                            canonical_problem=task.canonical_problem,
                            prompt=rendered.prompt,
                            target=rendered.target,
                            dependency_graph=task.dependency_graph,
                            task_side_trace=task.task_side_trace,
                            candidate_operations=family.candidate_operations,
                            nuisance_factors=nuisance_factors,
                            split=str(split_name),
                            group_keys={
                                "semantic_id": semantic_id,
                                "canonical_problem_hash": canonical_problem_hash,
                                "prompt_hash": prompt_hash,
                            },
                        )
                        record.validate()
                        assert_disjoint_semantic_id(
                            semantic_id, str(split_name), semantic_assignments
                        )
                        target_verified += 1
                        break
                    if record is None:
                        raise RuntimeError(
                            f"could not generate a unique {family_name!r} example for "
                            f"split {split_name!r}, cell {cell}, repetition {repetition} "
                            f"after {max_attempts} attempts"
                        )
                    split_records.append(record)
        split_records.sort(key=lambda item: item.instance_id)
        validate_records(split_records)
        records_by_split[str(split_name)] = split_records

    overlap_audit = audit_split_overlaps(records_by_split)
    if not overlap_audit["passed"]:
        raise ValueError("cross-split overlap audit failed")

    file_entries: dict[str, dict[str, Any]] = {}
    for split_name, records in records_by_split.items():
        filename = f"{split_name}.jsonl"
        path = destination / filename
        write_jsonl(path, records)
        file_entries[filename] = {
            "records": len(records),
            "sha256": sha256_file(path),
        }

    validation_summary = {
        "status": "passed",
        "records": sum(len(records) for records in records_by_split.values()),
        "targets_verified": target_verified,
        "graphs_validated": target_verified,
        "overlap_audit": overlap_audit,
    }
    validation_path = destination / "validation_summary.json"
    write_json(validation_path, validation_summary)
    file_entries[validation_path.name] = {
        "sha256": sha256_file(validation_path)
    }

    revision = dict(code_revision) if code_revision is not None else detect_code_revision()
    manifest = {
        "artifact_schema_version": "1.0",
        "package_version": __version__,
        "generator_version": str(config["generator_version"]),
        "code_revision": revision,
        "environment": {
            "python": platform.python_version(),
            "pyyaml": str(yaml.__version__),
        },
        "seed": int(config["seed"]),
        "resolved_config": resolved_config,
        "config_sha256": hashlib.sha256(
            canonical_json(resolved_config).encode("utf-8")
        ).hexdigest(),
        "counts": {
            split_name: _count_summary(records)
            for split_name, records in records_by_split.items()
        },
        "files": file_entries,
        "validation": validation_summary,
    }
    write_json(destination / "manifest.json", manifest)
    return manifest


def _count_summary(records: Sequence[CanonicalInstance]) -> dict[str, Any]:
    by_family = Counter(record.family for record in records)
    distributions: dict[str, dict[str, dict[str, int]]] = {}
    for family_name in sorted(by_family):
        family_records = [record for record in records if record.family == family_name]
        factor_names = sorted(
            {
                factor
                for record in family_records
                for factor in record.nuisance_factors
            }
        )
        distributions[family_name] = {}
        for factor_name in factor_names:
            counter = Counter(
                canonical_json(record.nuisance_factors[factor_name])
                for record in family_records
            )
            distributions[family_name][factor_name] = dict(sorted(counter.items()))
    joint_cells = {
        family_name: dict(
            sorted(
                Counter(
                    canonical_json(record.nuisance_factors)
                    for record in records
                    if record.family == family_name
                ).items()
            )
        )
        for family_name in sorted(by_family)
    }
    return {
        "total": len(records),
        "by_family": dict(sorted(by_family.items())),
        "factor_distributions": distributions,
        "joint_factor_cells": joint_cells,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate deterministic task-side calibration datasets."
    )
    parser.add_argument("--config", required=True, help="YAML generation config")
    parser.add_argument(
        "--output",
        required=True,
        help="new output directory; existing directories are not overwritten",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    manifest = generate_dataset(config, args.output)
    print(
        json.dumps(
            {
                "status": manifest["validation"]["status"],
                "records": manifest["validation"]["records"],
                "manifest": str(Path(args.output) / "manifest.json"),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
