"""Behavioral metrics with explicit denominators and Wilson intervals."""

from __future__ import annotations

from collections import defaultdict
import csv
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

from .schema import EvaluationRecord


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> list[float]:
    if total <= 0:
        return [0.0, 0.0]
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = proportion + z * z / (2 * total)
    margin = z * math.sqrt(
        proportion * (1 - proportion) / total + z * z / (4 * total * total)
    )
    return [
        max(0.0, (centre - margin) / denominator),
        min(1.0, (centre + margin) / denominator),
    ]


def metric_summary(records: Sequence[EvaluationRecord]) -> dict[str, Any]:
    total = len(records)
    trimmed = sum(record.trimmed_exact for record in records)
    raw = sum(record.raw_exact for record in records)
    parsed = sum(record.parsed_exact for record in records)
    format_valid = sum(record.format_valid for record in records)
    failures = sum(record.error_code is not None for record in records)
    empty = sum(record.empty_output for record in records)
    extra = sum(record.extra_text for record in records)
    invalid_or_failure = sum(
        record.error_code is not None or not record.format_valid for record in records
    )

    def rate(count: int) -> float:
        return count / total if total else 0.0

    return {
        "attempted": total,
        "raw_exact": raw,
        "raw_exact_rate": rate(raw),
        "trimmed_exact": trimmed,
        "trimmed_exact_rate": rate(trimmed),
        "trimmed_exact_wilson_95": wilson_interval(trimmed, total),
        "format_valid": format_valid,
        "format_valid_rate": rate(format_valid),
        "parsed_exact": parsed,
        "parsed_exact_rate": rate(parsed),
        "failures": failures,
        "failure_rate": rate(failures),
        "empty_outputs": empty,
        "empty_output_rate": rate(empty),
        "extra_text": extra,
        "extra_text_rate": rate(extra),
        "invalid_or_failure": invalid_or_failure,
        "invalid_or_failure_rate": rate(invalid_or_failure),
    }


def summarize(
    records: Sequence[EvaluationRecord],
    *,
    strata: Sequence[str],
    eligibility: Mapping[str, Any],
) -> dict[str, Any]:
    if not records:
        raise ValueError("cannot summarize an empty evaluation")
    groups: dict[str, dict[str, list[EvaluationRecord]]] = {}
    for field in strata:
        field_groups: dict[str, list[EvaluationRecord]] = defaultdict(list)
        for record in records:
            value = _field_value(record, field)
            field_groups[str(value)].append(record)
        groups[field] = {
            key: value for key, value in sorted(field_groups.items())
        }

    family_length: dict[str, list[EvaluationRecord]] = defaultdict(list)
    for record in records:
        key = f"{record.family}|{record.nuisance_factors.get('chain_length')}"
        family_length[key].append(record)

    by_family: dict[str, list[EvaluationRecord]] = defaultdict(list)
    for record in records:
        by_family[record.family].append(record)
    decisions: dict[str, Any] = {}
    for family, family_records in sorted(by_family.items()):
        overall = metric_summary(family_records)
        length_cells = {
            key.split("|", 1)[1]: metric_summary(cell_records)
            for key, cell_records in sorted(family_length.items())
            if key.startswith(f"{family}|")
        }
        thresholds = {
            "overall_trimmed_exact_min": float(
                eligibility["overall_trimmed_exact_min"]
            ),
            "each_chain_length_trimmed_exact_min": float(
                eligibility["each_chain_length_trimmed_exact_min"]
            ),
            "invalid_or_inference_failure_max": float(
                eligibility["invalid_or_inference_failure_max"]
            ),
        }
        passed = (
            overall["trimmed_exact_rate"]
            >= thresholds["overall_trimmed_exact_min"]
            and all(
                cell["trimmed_exact_rate"]
                >= thresholds["each_chain_length_trimmed_exact_min"]
                for cell in length_cells.values()
            )
            and overall["invalid_or_failure_rate"]
            <= thresholds["invalid_or_inference_failure_max"]
        )
        decisions[family] = {
            "passed_provisional_gate": passed,
            "paper_claim_supported": False,
            "thresholds": thresholds,
            "overall": overall,
            "chain_lengths": length_cells,
        }

    return {
        "attempted_instance_ids": len({record.instance_id for record in records}),
        "overall": metric_summary(records),
        "strata": {
            field: {
                key: metric_summary(group_records)
                for key, group_records in field_groups.items()
            }
            for field, field_groups in groups.items()
        },
        "family_by_chain_length": {
            key: metric_summary(group_records)
            for key, group_records in sorted(family_length.items())
        },
        "eligibility": decisions,
    }


def _field_value(record: EvaluationRecord, field: str) -> Any:
    if field in {"family", "split", "model_id", "prompt_mode"}:
        return getattr(record, field)
    if field not in record.nuisance_factors:
        raise ValueError(f"summary stratum {field!r} is missing from a record")
    return record.nuisance_factors[field]


def write_summary_csv(path: Path, summary: Mapping[str, Any]) -> None:
    rows: list[dict[str, Any]] = [
        _csv_row("overall", "all", summary["overall"])
    ]
    for field, groups in summary["strata"].items():
        for value, metrics in groups.items():
            rows.append(_csv_row(field, value, metrics))
    for value, metrics in summary["family_by_chain_length"].items():
        rows.append(_csv_row("family_by_chain_length", value, metrics))

    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def _csv_row(group: str, value: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    interval = metrics["trimmed_exact_wilson_95"]
    return {
        "group": group,
        "value": value,
        "attempted": metrics["attempted"],
        "trimmed_exact": metrics["trimmed_exact"],
        "trimmed_exact_rate": metrics["trimmed_exact_rate"],
        "wilson_95_low": interval[0],
        "wilson_95_high": interval[1],
        "format_valid_rate": metrics["format_valid_rate"],
        "failure_rate": metrics["failure_rate"],
        "invalid_or_failure_rate": metrics["invalid_or_failure_rate"],
        "extra_text_rate": metrics["extra_text_rate"],
    }
