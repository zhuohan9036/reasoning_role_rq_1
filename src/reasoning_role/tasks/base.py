"""Common interfaces for controlled task families."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any, Mapping, Protocol

from .schema import DependencyGraph, TaskSideTraceStep


@dataclass(frozen=True)
class GeneratedTask:
    """Canonical task-side object before surface rendering."""

    canonical_problem: Mapping[str, Any]
    dependency_graph: DependencyGraph
    task_side_trace: tuple[TaskSideTraceStep, ...]
    canonical_target: Any
    semantic_payload: Mapping[str, Any]
    family_factors: Mapping[str, Any]


@dataclass(frozen=True)
class RenderedTask:
    prompt: str
    target: str


class TaskFamily(Protocol):
    family_name: str
    generator_version: str
    candidate_operations: tuple[str, ...]
    supported_templates: tuple[str, ...]
    supported_vocabularies: tuple[str, ...]
    supported_answer_encodings: tuple[str, ...]

    def generate(
        self,
        rng: random.Random,
        *,
        chain_length: int,
        distractor_count: int,
        presentation_order: str,
        settings: Mapping[str, Any],
    ) -> GeneratedTask:
        """Generate a canonical task using only the explicit RNG."""

    def solve(self, canonical_problem: Mapping[str, Any]) -> Any:
        """Recompute the answer without reading a stored target."""

    def render(
        self,
        task: GeneratedTask,
        *,
        template_id: str,
        vocabulary_id: str,
        answer_encoding: str,
    ) -> RenderedTask:
        """Render model-facing fields without exposing intermediate states."""
