"""Versioned records for behavioral model-output evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from typing import Any, Mapping


EVALUATION_SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class InferenceRequest:
    request_id: str
    instance_id: str
    prompt: str
    expected_answer: str
    family: str
    answer_encoding: str
    nuisance_factors: Mapping[str, Any]

    def validate(self) -> None:
        for name, value in (
            ("request_id", self.request_id),
            ("instance_id", self.instance_id),
            ("prompt", self.prompt),
            ("expected_answer", self.expected_answer),
            ("family", self.family),
            ("answer_encoding", self.answer_encoding),
        ):
            if not value:
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True)
class BackendResult:
    request_id: str
    input_text: str
    completion: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    latency_ms: float | None
    error_code: str | None = None
    error_message: str | None = None

    def validate(self) -> None:
        if not self.request_id or not self.input_text:
            raise ValueError("backend result needs request_id and input_text")
        if self.error_code is None and self.completion is None:
            raise ValueError("successful backend result needs a completion")
        if self.error_code is not None and self.completion is not None:
            raise ValueError("failed backend result must not contain a completion")


@dataclass(frozen=True)
class EvaluationRecord:
    schema_version: str
    run_id: str
    request_id: str
    instance_id: str
    family: str
    split: str
    nuisance_factors: Mapping[str, Any]
    dataset_sha256: str
    model_id: str
    model_revision: str
    tokenizer_id: str
    tokenizer_revision: str
    prompt_mode: str
    input_text: str
    input_sha256: str
    expected_answer: str
    raw_completion: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    latency_ms: float | None
    error_code: str | None
    error_message: str | None
    raw_exact: bool
    trimmed_exact: bool
    format_valid: bool
    parsed_answer: Any
    parsed_exact: bool
    empty_output: bool
    extra_text: bool

    def validate(self) -> None:
        if self.schema_version != EVALUATION_SCHEMA_VERSION:
            raise ValueError("unsupported evaluation schema version")
        for name, value in (
            ("run_id", self.run_id),
            ("request_id", self.request_id),
            ("instance_id", self.instance_id),
            ("family", self.family),
            ("split", self.split),
            ("dataset_sha256", self.dataset_sha256),
            ("model_id", self.model_id),
            ("model_revision", self.model_revision),
            ("tokenizer_id", self.tokenizer_id),
            ("tokenizer_revision", self.tokenizer_revision),
            ("prompt_mode", self.prompt_mode),
            ("input_text", self.input_text),
            ("input_sha256", self.input_sha256),
            ("expected_answer", self.expected_answer),
        ):
            if not value:
                raise ValueError(f"{name} must be non-empty")
        if self.error_code is None and self.raw_completion is None:
            raise ValueError("successful record needs a raw completion")
        if self.error_code is not None and self.raw_completion is not None:
            raise ValueError("failed record must not contain a raw completion")
        if not self.format_valid and self.parsed_exact:
            raise ValueError("parsed_exact requires format_valid")
        if self.format_valid != (self.parsed_answer is not None):
            raise ValueError("format_valid must match parsed-answer availability")
        if self.raw_exact and not self.trimmed_exact:
            raise ValueError("raw_exact must imply trimmed_exact")
        if self.trimmed_exact and not self.parsed_exact:
            raise ValueError("trimmed_exact must imply parsed_exact")
        actual_input_hash = hashlib.sha256(self.input_text.encode("utf-8")).hexdigest()
        if self.input_sha256 != actual_input_hash:
            raise ValueError("input_sha256 does not match input_text")
        if self.error_code is not None and any(
            (self.raw_exact, self.trimmed_exact, self.format_valid, self.parsed_exact)
        ):
            raise ValueError("failed records cannot be correct or format-valid")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "EvaluationRecord":
        record = cls(**value)
        record.validate()
        return record
