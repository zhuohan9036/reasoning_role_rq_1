"""Deterministic offline backend used only for harness validation."""

from __future__ import annotations

import hashlib
import re
from typing import Any, Mapping, Sequence

from ..parsing import parse_complete
from ..schema import BackendResult, InferenceRequest


class FakeBackend:
    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = dict(config)
        self.prompt_mode = str(self.config.get("prompt_mode", "plain"))
        self.percentages = {
            key: int(self.config.get("outcome_percentages", {}).get(key, default))
            for key, default in (
                ("correct", 100),
                ("wrong", 0),
                ("invalid", 0),
                ("failure", 0),
            )
        }
        if sum(self.percentages.values()) != 100 or any(
            value < 0 for value in self.percentages.values()
        ):
            raise ValueError("fake outcome percentages must be non-negative and sum to 100")
        if self.prompt_mode not in {"plain", "fake_chat"}:
            raise ValueError("fake prompt_mode must be plain or fake_chat")

    def prepare(self) -> Mapping[str, Any]:
        return {
            "backend": "fake",
            "model_id": "fake-causal-lm",
            "model_revision": "1",
            "tokenizer_id": "fake-tokenizer",
            "tokenizer_revision": "1",
            "prompt_mode": self.prompt_mode,
            "parameters_frozen": True,
            "gradients_enabled": False,
        }

    def format_input(self, prompt: str) -> str:
        if self.prompt_mode == "plain":
            return prompt
        return f"<user>\n{prompt}\n</user>\n<assistant>\n"

    def generate(
        self, requests: Sequence[InferenceRequest]
    ) -> Sequence[BackendResult]:
        results: list[BackendResult] = []
        for request in requests:
            request.validate()
            input_text = self.format_input(request.prompt)
            outcome = self._outcome(request.instance_id)
            if outcome == "failure":
                results.append(
                    BackendResult(
                        request_id=request.request_id,
                        input_text=input_text,
                        completion=None,
                        prompt_tokens=self._token_count(input_text),
                        completion_tokens=None,
                        latency_ms=0.0,
                        error_code="fake_inference_failure",
                        error_message="deterministic fake failure",
                    )
                )
                continue
            if outcome == "correct":
                completion = request.expected_answer
            elif outcome == "invalid":
                completion = f"The answer is {request.expected_answer}."
            else:
                completion = self._valid_wrong_answer(request)
            results.append(
                BackendResult(
                    request_id=request.request_id,
                    input_text=input_text,
                    completion=completion,
                    prompt_tokens=self._token_count(input_text),
                    completion_tokens=self._token_count(completion),
                    latency_ms=0.0,
                )
            )
        return results

    def close(self) -> None:
        return None

    def _outcome(self, instance_id: str) -> str:
        bucket = int(hashlib.sha256(instance_id.encode("utf-8")).hexdigest()[:8], 16) % 100
        boundary = 0
        for outcome in ("correct", "wrong", "invalid", "failure"):
            boundary += self.percentages[outcome]
            if bucket < boundary:
                return outcome
        raise AssertionError("unreachable fake outcome bucket")

    @staticmethod
    def _token_count(text: str) -> int:
        return len(re.findall(r"\S+", text))

    @staticmethod
    def _valid_wrong_answer(request: InferenceRequest) -> str:
        parsed = parse_complete(
            request.expected_answer, request.family, request.answer_encoding
        )
        if request.family == "function_composition":
            replacement = "WRONG" if parsed != "WRONG" else "OTHER"
            return (
                replacement
                if request.answer_encoding == "symbol"
                else f"[{replacement}]"
            )
        dx, dy = parsed
        if request.answer_encoding == "vector":
            return f"({dx + 1},{dy})"
        return f"x={dx + 1};y={dy}"
