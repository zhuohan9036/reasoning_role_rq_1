"""Strict whole-output scoring for task-calibration answers."""

from __future__ import annotations

import re
from typing import Any


_SYMBOL = re.compile(r"[A-Za-z][A-Za-z0-9_]*\Z")
_BRACKETED = re.compile(r"\[([A-Za-z][A-Za-z0-9_]*)\]\Z")
_INTEGER = r"(?:0|[1-9][0-9]*|-[1-9][0-9]*)"
_VECTOR = re.compile(rf"\(({_INTEGER}),({_INTEGER})\)\Z")
_LABELED_VECTOR = re.compile(rf"x=({_INTEGER});y=({_INTEGER})\Z")


def parse_complete(text: str, family: str, answer_encoding: str) -> Any | None:
    """Parse only if the entire already-trimmed text is canonical."""

    if family == "function_composition":
        if answer_encoding == "symbol":
            return text if _SYMBOL.fullmatch(text) else None
        if answer_encoding == "bracketed":
            match = _BRACKETED.fullmatch(text)
            return match.group(1) if match else None
    elif family == "relational_path":
        if answer_encoding == "vector":
            match = _VECTOR.fullmatch(text)
            return (int(match.group(1)), int(match.group(2))) if match else None
        if answer_encoding == "labeled_vector":
            match = _LABELED_VECTOR.fullmatch(text)
            return (int(match.group(1)), int(match.group(2))) if match else None
    raise ValueError(
        f"unsupported family/answer encoding: {family!r}/{answer_encoding!r}"
    )


def score_completion(
    *,
    expected: str,
    completion: str | None,
    family: str,
    answer_encoding: str,
    error_code: str | None = None,
) -> dict[str, Any]:
    if error_code is not None:
        return {
            "raw_exact": False,
            "trimmed_exact": False,
            "format_valid": False,
            "parsed_answer": None,
            "parsed_exact": False,
            "empty_output": False,
            "extra_text": False,
        }
    if completion is None:
        raise ValueError("completion is required when error_code is absent")

    trimmed = completion.strip()
    parsed = parse_complete(trimmed, family, answer_encoding) if trimmed else None
    expected_parsed = parse_complete(expected, family, answer_encoding)
    if expected_parsed is None:
        raise ValueError(f"expected answer is not canonical: {expected!r}")
    format_valid = parsed is not None
    return {
        "raw_exact": completion == expected,
        "trimmed_exact": trimmed == expected,
        "format_valid": format_valid,
        "parsed_answer": parsed,
        "parsed_exact": format_valid and parsed == expected_parsed,
        "empty_output": not trimmed,
        "extra_text": bool(trimmed) and not format_valid and expected in trimmed,
    }
