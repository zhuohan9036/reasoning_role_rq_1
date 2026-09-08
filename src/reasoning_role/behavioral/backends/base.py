"""Backend protocol shared by fake and real model implementations."""

from __future__ import annotations

from typing import Any, Mapping, Protocol, Sequence

from ..schema import BackendResult, InferenceRequest


class InferenceBackend(Protocol):
    def prepare(self) -> Mapping[str, Any]: ...

    def format_input(self, prompt: str) -> str: ...

    def generate(
        self, requests: Sequence[InferenceRequest]
    ) -> Sequence[BackendResult]: ...

    def close(self) -> None: ...
