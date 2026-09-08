"""Controlled relational path-composition tasks."""

from __future__ import annotations

from collections import deque
import random
from typing import Any, Mapping

from .base import GeneratedTask, RenderedTask
from .schema import DependencyEdge, DependencyGraph, DependencyNode, TaskSideTraceStep


_DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


class RelationalPathTask:
    family_name = "relational_path"
    generator_version = "1.0"
    candidate_operations = ("compose_relation",)
    supported_templates = ("compact", "prose")
    supported_vocabularies = ("names_a", "names_b", "neutral_entities")
    supported_answer_encodings = ("vector", "labeled_vector")

    def generate(
        self,
        rng: random.Random,
        *,
        chain_length: int,
        distractor_count: int,
        presentation_order: str,
        settings: Mapping[str, Any],
    ) -> GeneratedTask:
        del settings
        if chain_length < 1:
            raise ValueError("chain_length must be positive")
        if distractor_count < 0:
            raise ValueError("distractor_count must be non-negative")
        if presentation_order not in {"canonical", "shuffled"}:
            raise ValueError(
                "presentation_order must be 'canonical' or 'shuffled'"
            )

        path_vectors = self._sample_nonzero_path(rng, chain_length)
        graph_nodes: list[DependencyNode] = []
        graph_edges: list[DependencyEdge] = []
        trace: list[TaskSideTraceStep] = []
        relation_edges: list[dict[str, Any]] = []
        offset = [0, 0]

        for index, vector in enumerate(path_vectors):
            relation_id = f"rel_{index}"
            relation_edges.append(
                {
                    "relation_id": relation_id,
                    "source": index,
                    "target": index + 1,
                    "vector": list(vector),
                    "relevant": True,
                }
            )
            node_id = f"step_{index}"
            graph_nodes.append(
                DependencyNode(
                    node_id=node_id,
                    operation="compose_relation",
                    parameters={"relation_id": relation_id},
                )
            )
            if index:
                graph_edges.append(DependencyEdge(f"step_{index - 1}", node_id))
            next_offset = [offset[0] + vector[0], offset[1] + vector[1]]
            trace.append(
                TaskSideTraceStep(
                    step_id=f"trace_{index}",
                    node_id=node_id,
                    operation="compose_relation",
                    input_state={"offset": list(offset)},
                    output_state={"offset": list(next_offset)},
                )
            )
            offset = next_offset

        next_entity = chain_length + 1
        for index in range(distractor_count):
            vector = rng.choice(_DIRECTIONS)
            relation_edges.append(
                {
                    "relation_id": f"distractor_rel_{index}",
                    "source": next_entity,
                    "target": next_entity + 1,
                    "vector": list(vector),
                    "relevant": False,
                }
            )
            next_entity += 2

        order = [str(edge["relation_id"]) for edge in relation_edges]
        if presentation_order == "shuffled":
            rng.shuffle(order)
        canonical_problem = {
            "relations": relation_edges,
            "query": {"source": 0, "target": chain_length},
            "presentation_order": order,
            "entity_count": next_entity,
        }
        semantic_payload = {
            "relations": sorted(
                relation_edges, key=lambda item: str(item["relation_id"])
            ),
            "query": canonical_problem["query"],
            "entity_count": next_entity,
        }
        graph = DependencyGraph(
            nodes=tuple(graph_nodes),
            edges=tuple(graph_edges),
            output_node_id=graph_nodes[-1].node_id,
        )
        graph.validate()
        return GeneratedTask(
            canonical_problem=canonical_problem,
            dependency_graph=graph,
            task_side_trace=tuple(trace),
            canonical_target=list(offset),
            semantic_payload=semantic_payload,
            family_factors={},
        )

    @staticmethod
    def _sample_nonzero_path(
        rng: random.Random, chain_length: int
    ) -> list[tuple[int, int]]:
        for _ in range(1_000):
            vectors = [rng.choice(_DIRECTIONS) for _ in range(chain_length)]
            if sum(vector[0] for vector in vectors) != 0 or sum(
                vector[1] for vector in vectors
            ) != 0:
                return vectors
        raise RuntimeError("failed to sample a path with non-zero displacement")

    def solve(self, canonical_problem: Mapping[str, Any]) -> list[int]:
        adjacency: dict[int, list[tuple[int, tuple[int, int]]]] = {}
        for relation in canonical_problem["relations"]:
            source = int(relation["source"])
            target = int(relation["target"])
            vector_values = relation["vector"]
            vector = (int(vector_values[0]), int(vector_values[1]))
            adjacency.setdefault(source, []).append((target, vector))

        query = canonical_problem["query"]
        source = int(query["source"])
        target = int(query["target"])
        queue: deque[tuple[int, tuple[int, int]]] = deque([(source, (0, 0))])
        visited = {source}
        while queue:
            entity, offset = queue.popleft()
            if entity == target:
                return [offset[0], offset[1]]
            for next_entity, vector in sorted(adjacency.get(entity, [])):
                if next_entity not in visited:
                    visited.add(next_entity)
                    queue.append(
                        (
                            next_entity,
                            (offset[0] + vector[0], offset[1] + vector[1]),
                        )
                    )
        raise ValueError("query target is unreachable from query source")

    def render(
        self,
        task: GeneratedTask,
        *,
        template_id: str,
        vocabulary_id: str,
        answer_encoding: str,
    ) -> RenderedTask:
        self._validate_render_options(template_id, vocabulary_id, answer_encoding)
        problem = task.canonical_problem
        names = self._entity_names(vocabulary_id, int(problem["entity_count"]))
        relations = {
            str(item["relation_id"]): item for item in problem["relations"]
        }
        relation_lines: list[str] = []
        for relation_id in problem["presentation_order"]:
            relation = relations[str(relation_id)]
            source_name = names[int(relation["source"])]
            target_name = names[int(relation["target"])]
            vector_values = relation["vector"]
            vector = (int(vector_values[0]), int(vector_values[1]))
            phrase = self._direction_phrase(vocabulary_id, vector)
            if template_id == "compact":
                relation_lines.append(f"{target_name} {phrase} {source_name}")
            else:
                relation_lines.append(
                    f"{target_name} is located {phrase} {source_name}."
                )

        query = problem["query"]
        source_name = names[int(query["source"])]
        target_name = names[int(query["target"])]
        if template_id == "compact":
            prompt = (
                "Relations:\n"
                + "\n".join(relation_lines)
                + f"\nGive the displacement of {target_name} from {source_name}. "
                "Use x for east/west and y for north/south. Return only the vector."
            )
        else:
            prompt = (
                "Read these spatial statements:\n"
                + "\n".join(relation_lines)
                + f"\nWhat is the net displacement from {source_name} to "
                f"{target_name}? Positive x means east and positive y means north. "
                "Give only the answer."
            )

        dx, dy = (int(value) for value in task.canonical_target)
        target = f"({dx},{dy})" if answer_encoding == "vector" else f"x={dx};y={dy}"
        return RenderedTask(prompt=prompt, target=target)

    def _validate_render_options(
        self, template_id: str, vocabulary_id: str, answer_encoding: str
    ) -> None:
        for name, value, supported in (
            ("template", template_id, self.supported_templates),
            ("vocabulary", vocabulary_id, self.supported_vocabularies),
            ("answer encoding", answer_encoding, self.supported_answer_encodings),
        ):
            if value not in supported:
                raise ValueError(
                    f"unsupported {name} {value!r} for {self.family_name}; "
                    f"choose from {supported}"
                )

    @staticmethod
    def _entity_names(vocabulary_id: str, count: int) -> list[str]:
        roots = {
            "names_a": [
                "Ava",
                "Ben",
                "Cora",
                "Dion",
                "Esme",
                "Finn",
                "Gia",
                "Hugo",
                "Iris",
                "Jules",
                "Kira",
                "Leon",
            ],
            "names_b": [
                "Uma",
                "Vek",
                "Wren",
                "Xan",
                "Yara",
                "Zed",
                "Nilo",
                "Orin",
                "Pia",
                "Quin",
                "Rhea",
                "Sven",
            ],
            "neutral_entities": [f"entity_{index}" for index in range(64)],
        }
        bank = roots[vocabulary_id]
        if count > len(bank):
            raise ValueError(
                f"vocabulary {vocabulary_id!r} supports at most {len(bank)} entities"
            )
        return bank[:count]

    @staticmethod
    def _direction_phrase(vocabulary_id: str, vector: tuple[int, int]) -> str:
        phrase_banks = {
            "names_a": {
                (0, 1): "north of",
                (1, 0): "east of",
                (0, -1): "south of",
                (-1, 0): "west of",
            },
            "names_b": {
                (0, 1): "above",
                (1, 0): "to the right of",
                (0, -1): "below",
                (-1, 0): "to the left of",
            },
            "neutral_entities": {
                (0, 1): "at offset (0,1) from",
                (1, 0): "at offset (1,0) from",
                (0, -1): "at offset (0,-1) from",
                (-1, 0): "at offset (-1,0) from",
            },
        }
        return phrase_banks[vocabulary_id][vector]
