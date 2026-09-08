"""Explicit registry for approved pilot task families."""

from __future__ import annotations

from .base import TaskFamily
from .function_composition import FunctionCompositionTask
from .relational_path import RelationalPathTask


_FAMILIES: dict[str, type[TaskFamily]] = {
    FunctionCompositionTask.family_name: FunctionCompositionTask,
    RelationalPathTask.family_name: RelationalPathTask,
}


def get_task_family(name: str) -> TaskFamily:
    try:
        family_type = _FAMILIES[name]
    except KeyError as error:
        raise ValueError(
            f"unknown task family {name!r}; choose from {sorted(_FAMILIES)}"
        ) from error
    return family_type()


def available_task_families() -> tuple[str, ...]:
    return tuple(sorted(_FAMILIES))
