"""Versioned, JSON-serializable task-side records.

The objects in this module describe the generator's externally specified
computation. They are deliberately named task-side traces and must not be
interpreted as observations of a model's internal reasoning.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "1.0"


def canonical_json(value: Any) -> str:
    """Return a stable, compact JSON representation."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def stable_digest(value: Any, *, prefix: str = "", length: int = 24) -> str:
    """Hash a JSON-compatible value with an optional semantic namespace."""

    payload = f"{prefix}\0{canonical_json(value)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:length]


@dataclass(frozen=True)
class DependencyNode:
    node_id: str
    operation: str
    parameters: Mapping[str, Any]

    def validate(self) -> None:
        if not self.node_id:
            raise ValueError("dependency node_id must be non-empty")
        if not self.operation:
            raise ValueError(f"node {self.node_id!r} has no operation")


@dataclass(frozen=True)
class DependencyEdge:
    source: str
    target: str

    def validate(self) -> None:
        if not self.source or not self.target:
            raise ValueError("dependency edge endpoints must be non-empty")
        if self.source == self.target:
            raise ValueError(f"self-loop at dependency node {self.source!r}")


@dataclass(frozen=True)
class DependencyGraph:
    nodes: tuple[DependencyNode, ...]
    edges: tuple[DependencyEdge, ...]
    output_node_id: str

    def validate(self) -> None:
        if not self.nodes:
            raise ValueError("dependency graph must contain at least one node")
        for node in self.nodes:
            node.validate()
        for edge in self.edges:
            edge.validate()

        node_ids = [node.node_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("dependency node IDs must be unique")
        node_set = set(node_ids)
        if self.output_node_id not in node_set:
            raise ValueError("output_node_id is not present in the graph")
        for edge in self.edges:
            if edge.source not in node_set or edge.target not in node_set:
                raise ValueError(
                    f"edge {edge.source!r}->{edge.target!r} references an unknown node"
                )

        outgoing: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
        indegree: dict[str, int] = {node_id: 0 for node_id in node_ids}
        for edge in self.edges:
            outgoing[edge.source].append(edge.target)
            indegree[edge.target] += 1

        queue = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
        visited: list[str] = []
        while queue:
            node_id = queue.pop(0)
            visited.append(node_id)
            for target in sorted(outgoing[node_id]):
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
                    queue.sort()
        if len(visited) != len(node_ids):
            raise ValueError("dependency graph must be acyclic")

        reverse: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
        for edge in self.edges:
            reverse[edge.target].append(edge.source)
        ancestors = {self.output_node_id}
        frontier = [self.output_node_id]
        while frontier:
            target = frontier.pop()
            for source in reverse[target]:
                if source not in ancestors:
                    ancestors.add(source)
                    frontier.append(source)
        if ancestors != node_set:
            unreachable = sorted(node_set - ancestors)
            raise ValueError(
                "all dependency nodes must contribute to the output; "
                f"non-contributing nodes: {unreachable}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [asdict(node) for node in self.nodes],
            "edges": [asdict(edge) for edge in self.edges],
            "output_node_id": self.output_node_id,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DependencyGraph":
        return cls(
            nodes=tuple(DependencyNode(**node) for node in value["nodes"]),
            edges=tuple(DependencyEdge(**edge) for edge in value["edges"]),
            output_node_id=str(value["output_node_id"]),
        )


@dataclass(frozen=True)
class TaskSideTraceStep:
    step_id: str
    node_id: str
    operation: str
    input_state: Mapping[str, Any]
    output_state: Mapping[str, Any]

    def validate(self) -> None:
        if not self.step_id or not self.node_id or not self.operation:
            raise ValueError("trace step identifiers and operation must be non-empty")


@dataclass(frozen=True)
class CanonicalInstance:
    schema_version: str
    instance_id: str
    family: str
    generator_version: str
    canonical_problem: Mapping[str, Any]
    prompt: str
    target: str
    dependency_graph: DependencyGraph
    task_side_trace: tuple[TaskSideTraceStep, ...]
    candidate_operations: tuple[str, ...]
    nuisance_factors: Mapping[str, Any]
    split: str
    group_keys: Mapping[str, str]

    def validate(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(
                f"unsupported schema_version {self.schema_version!r}; "
                f"expected {SCHEMA_VERSION!r}"
            )
        for field_name, value in (
            ("instance_id", self.instance_id),
            ("family", self.family),
            ("generator_version", self.generator_version),
            ("prompt", self.prompt),
            ("target", self.target),
            ("split", self.split),
        ):
            if not value:
                raise ValueError(f"{field_name} must be non-empty")
        if "semantic_id" not in self.group_keys:
            raise ValueError("group_keys must contain semantic_id")
        if not self.candidate_operations:
            raise ValueError("candidate_operations must be non-empty")
        if len(self.candidate_operations) != len(set(self.candidate_operations)):
            raise ValueError("candidate_operations must be unique")

        self.dependency_graph.validate()
        if not self.task_side_trace:
            raise ValueError("task_side_trace must be non-empty")
        for step in self.task_side_trace:
            step.validate()

        node_by_id = {
            node.node_id: node for node in self.dependency_graph.nodes
        }
        trace_node_ids = [step.node_id for step in self.task_side_trace]
        if len(trace_node_ids) != len(set(trace_node_ids)):
            raise ValueError("a dependency node may appear only once in a trace")
        if set(trace_node_ids) != set(node_by_id):
            raise ValueError("trace steps must cover exactly the dependency nodes")
        for step in self.task_side_trace:
            node = node_by_id[step.node_id]
            if step.operation != node.operation:
                raise ValueError(
                    f"trace operation for {step.node_id!r} does not match graph node"
                )
            if step.operation not in self.candidate_operations:
                raise ValueError(
                    f"trace operation {step.operation!r} is not a candidate operation"
                )

        position = {node_id: index for index, node_id in enumerate(trace_node_ids)}
        for edge in self.dependency_graph.edges:
            if position[edge.source] >= position[edge.target]:
                raise ValueError("task-side trace must follow dependency order")
        if trace_node_ids[-1] != self.dependency_graph.output_node_id:
            raise ValueError("final trace step must be the graph output node")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "instance_id": self.instance_id,
            "family": self.family,
            "generator_version": self.generator_version,
            "canonical_problem": dict(self.canonical_problem),
            "prompt": self.prompt,
            "target": self.target,
            "dependency_graph": self.dependency_graph.to_dict(),
            "task_side_trace": [asdict(step) for step in self.task_side_trace],
            "candidate_operations": list(self.candidate_operations),
            "nuisance_factors": dict(self.nuisance_factors),
            "split": self.split,
            "group_keys": dict(self.group_keys),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "CanonicalInstance":
        return cls(
            schema_version=str(value["schema_version"]),
            instance_id=str(value["instance_id"]),
            family=str(value["family"]),
            generator_version=str(value["generator_version"]),
            canonical_problem=dict(value["canonical_problem"]),
            prompt=str(value["prompt"]),
            target=str(value["target"]),
            dependency_graph=DependencyGraph.from_dict(value["dependency_graph"]),
            task_side_trace=tuple(
                TaskSideTraceStep(**step) for step in value["task_side_trace"]
            ),
            candidate_operations=tuple(value["candidate_operations"]),
            nuisance_factors=dict(value["nuisance_factors"]),
            split=str(value["split"]),
            group_keys=dict(value["group_keys"]),
        )


def validate_records(records: Sequence[CanonicalInstance]) -> None:
    """Validate records and require unique instance IDs."""

    instance_ids: set[str] = set()
    for record in records:
        record.validate()
        if record.instance_id in instance_ids:
            raise ValueError(f"duplicate instance_id {record.instance_id!r}")
        instance_ids.add(record.instance_id)
