"""Factor-cell expansion and leakage audits for named dataset splits."""

from __future__ import annotations

from itertools import combinations, product
from typing import Any, Mapping, Sequence

from reasoning_role.tasks.schema import CanonicalInstance


SPLIT_KINDS = {
    "train",
    "iid",
    "heldout_surface",
    "heldout_template",
    "heldout_length",
}


def expand_factor_cells(
    split_spec: Mapping[str, Any], family_name: str
) -> list[dict[str, Any]]:
    factors = split_spec["factors"]
    render = split_spec["render"][family_name]
    values = (
        factors["chain_lengths"],
        factors["distractor_counts"],
        factors["presentation_orders"],
        render["templates"],
        render["vocabularies"],
        render["answer_encodings"],
    )
    return [
        {
            "chain_length": int(chain_length),
            "distractor_count": int(distractor_count),
            "presentation_order": str(presentation_order),
            "template_id": str(template_id),
            "vocabulary_id": str(vocabulary_id),
            "answer_encoding": str(answer_encoding),
        }
        for (
            chain_length,
            distractor_count,
            presentation_order,
            template_id,
            vocabulary_id,
            answer_encoding,
        ) in product(*values)
    ]


def assert_disjoint_semantic_id(
    semantic_id: str,
    split_name: str,
    assignments: dict[str, str],
) -> None:
    previous = assignments.get(semantic_id)
    if previous is not None and previous != split_name:
        raise ValueError(
            f"semantic identity {semantic_id!r} appears in both "
            f"{previous!r} and {split_name!r}"
        )
    assignments[semantic_id] = split_name


def audit_split_overlaps(
    records_by_split: Mapping[str, Sequence[CanonicalInstance]],
) -> dict[str, Any]:
    """Audit multiple identity levels between every pair of exclusive splits."""

    keys = ("semantic_id", "canonical_problem_hash", "prompt_hash")
    pairs: dict[str, dict[str, int]] = {}
    passed = True
    for left, right in combinations(sorted(records_by_split), 2):
        pair_result: dict[str, int] = {}
        for key in keys:
            left_values = {record.group_keys[key] for record in records_by_split[left]}
            right_values = {
                record.group_keys[key] for record in records_by_split[right]
            }
            overlap_count = len(left_values & right_values)
            pair_result[key] = overlap_count
            if overlap_count:
                passed = False
        pairs[f"{left}__{right}"] = pair_result
    return {"passed": passed, "pairs": pairs}


def validate_holdout_axes(
    splits: Mapping[str, Mapping[str, Any]], family_names: Sequence[str]
) -> None:
    train_entries = [
        (name, spec) for name, spec in splits.items() if spec.get("kind") == "train"
    ]
    if len(train_entries) != 1:
        raise ValueError("configuration must contain exactly one train split")
    _, train = train_entries[0]

    for split_name, split_spec in splits.items():
        kind = str(split_spec.get("kind"))
        if kind not in SPLIT_KINDS:
            raise ValueError(
                f"split {split_name!r} has unsupported kind {kind!r}; "
                f"choose from {sorted(SPLIT_KINDS)}"
            )
        for family_name in family_names:
            train_render = train["render"][family_name]
            render = split_spec["render"][family_name]
            train_lengths = set(train["factors"]["chain_lengths"])
            lengths = set(split_spec["factors"]["chain_lengths"])
            train_distractors = set(train["factors"]["distractor_counts"])
            distractors = set(split_spec["factors"]["distractor_counts"])
            train_orders = set(train["factors"]["presentation_orders"])
            orders = set(split_spec["factors"]["presentation_orders"])
            train_templates = set(train_render["templates"])
            templates = set(render["templates"])
            train_vocabularies = set(train_render["vocabularies"])
            vocabularies = set(render["vocabularies"])
            train_encodings = set(train_render["answer_encodings"])
            encodings = set(render["answer_encodings"])

            if kind != "train" and (
                distractors != train_distractors
                or orders != train_orders
                or encodings != train_encodings
            ):
                raise ValueError(
                    f"split {split_name!r} must match train distractor, "
                    "presentation-order, and answer-encoding domains"
                )

            if kind == "iid":
                if lengths != train_lengths:
                    raise ValueError(
                        f"IID split {split_name!r} must match train chain lengths"
                    )
                if templates != train_templates or vocabularies != train_vocabularies:
                    raise ValueError(
                        f"IID split {split_name!r} must match train rendering domains"
                    )
            elif kind == "heldout_surface":
                if train_vocabularies & vocabularies:
                    raise ValueError(
                        f"surface holdout {split_name!r} must use disjoint vocabularies"
                    )
                if lengths != train_lengths or templates != train_templates:
                    raise ValueError(
                        f"surface holdout {split_name!r} must change only its surface axis"
                    )
            elif kind == "heldout_template":
                if train_templates & templates:
                    raise ValueError(
                        f"template holdout {split_name!r} must use disjoint templates"
                    )
                if lengths != train_lengths or vocabularies != train_vocabularies:
                    raise ValueError(
                        f"template holdout {split_name!r} must change only its template axis"
                    )
            elif kind == "heldout_length":
                if train_lengths & lengths:
                    raise ValueError(
                        f"length holdout {split_name!r} must use disjoint chain lengths"
                    )
                if templates != train_templates or vocabularies != train_vocabularies:
                    raise ValueError(
                        f"length holdout {split_name!r} must change only its length axis"
                    )
