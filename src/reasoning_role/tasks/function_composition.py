"""Controlled symbolic function-composition tasks."""

from __future__ import annotations

import random
from typing import Any, Mapping

from .base import GeneratedTask, RenderedTask
from .schema import DependencyEdge, DependencyGraph, DependencyNode, TaskSideTraceStep


class FunctionCompositionTask:
    family_name = "function_composition"
    generator_version = "1.0"
    candidate_operations = ("apply_function",)
    supported_templates = ("compact", "prose")
    supported_vocabularies = ("latin", "greek_names", "neutral_tokens")
    supported_answer_encodings = ("symbol", "bracketed")

    def generate(
        self,
        rng: random.Random,
        *,
        chain_length: int,
        distractor_count: int,
        presentation_order: str,
        settings: Mapping[str, Any],
    ) -> GeneratedTask:
        domain_size = int(settings.get("domain_size", 6))
        if domain_size < 3:
            raise ValueError("function_composition domain_size must be at least 3")
        if chain_length < 1:
            raise ValueError("chain_length must be positive")
        if distractor_count < 0:
            raise ValueError("distractor_count must be non-negative")
        if presentation_order not in {"canonical", "shuffled"}:
            raise ValueError(
                "presentation_order must be 'canonical' or 'shuffled'"
            )

        start = rng.randrange(domain_size)
        current = start
        functions: list[dict[str, Any]] = []
        relevant_ids: list[str] = []
        nodes: list[DependencyNode] = []
        edges: list[DependencyEdge] = []
        trace: list[TaskSideTraceStep] = []

        for index in range(chain_length):
            function_id = f"fn_{index}"
            mapping = self._sample_mapping(rng, domain_size, must_move=current)
            next_value = mapping[current]
            functions.append(
                {"function_id": function_id, "mapping": mapping, "relevant": True}
            )
            relevant_ids.append(function_id)
            node_id = f"step_{index}"
            nodes.append(
                DependencyNode(
                    node_id=node_id,
                    operation="apply_function",
                    parameters={"function_id": function_id},
                )
            )
            if index:
                edges.append(DependencyEdge(f"step_{index - 1}", node_id))
            trace.append(
                TaskSideTraceStep(
                    step_id=f"trace_{index}",
                    node_id=node_id,
                    operation="apply_function",
                    input_state={"symbol": current},
                    output_state={"symbol": next_value},
                )
            )
            current = next_value

        for index in range(distractor_count):
            functions.append(
                {
                    "function_id": f"distractor_fn_{index}",
                    "mapping": self._sample_mapping(rng, domain_size),
                    "relevant": False,
                }
            )

        order = [str(item["function_id"]) for item in functions]
        if presentation_order == "shuffled":
            rng.shuffle(order)

        canonical_problem = {
            "domain_size": domain_size,
            "functions": functions,
            "query": {"start": start, "composition": relevant_ids},
            "presentation_order": order,
        }
        semantic_payload = {
            "domain_size": domain_size,
            "functions": sorted(functions, key=lambda item: str(item["function_id"])),
            "query": canonical_problem["query"],
        }
        graph = DependencyGraph(
            nodes=tuple(nodes),
            edges=tuple(edges),
            output_node_id=nodes[-1].node_id,
        )
        graph.validate()
        return GeneratedTask(
            canonical_problem=canonical_problem,
            dependency_graph=graph,
            task_side_trace=tuple(trace),
            canonical_target=current,
            semantic_payload=semantic_payload,
            family_factors={"domain_size": domain_size},
        )

    @staticmethod
    def _sample_mapping(
        rng: random.Random, domain_size: int, must_move: int | None = None
    ) -> list[int]:
        base = list(range(domain_size))
        for _ in range(1_000):
            mapping = rng.sample(base, len(base))
            if mapping != base and (
                must_move is None or mapping[must_move] != must_move
            ):
                return mapping
        raise RuntimeError("failed to sample a non-trivial function mapping")

    def solve(self, canonical_problem: Mapping[str, Any]) -> int:
        functions = {
            str(item["function_id"]): [int(value) for value in item["mapping"]]
            for item in canonical_problem["functions"]
        }
        query = canonical_problem["query"]
        current = int(query["start"])
        for function_id in query["composition"]:
            mapping = functions[str(function_id)]
            if current < 0 or current >= len(mapping):
                raise ValueError("function input is outside the declared domain")
            current = mapping[current]
        return current

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
        domain_size = int(problem["domain_size"])
        symbols = self._symbols(vocabulary_id, domain_size)
        functions = {
            str(item["function_id"]): item for item in problem["functions"]
        }
        ordered_ids = [str(value) for value in problem["presentation_order"]]
        name_by_id = {
            function_id: self._function_name(vocabulary_id, index)
            for index, function_id in enumerate(sorted(functions))
        }

        rule_lines: list[str] = []
        for function_id in ordered_ids:
            item = functions[function_id]
            mapping = [int(value) for value in item["mapping"]]
            pairs = ", ".join(
                f"{symbols[source]}->{symbols[target]}"
                for source, target in enumerate(mapping)
            )
            rule_lines.append(f"{name_by_id[function_id]}: {pairs}")

        query = problem["query"]
        composition = [name_by_id[str(value)] for value in query["composition"]]
        start = symbols[int(query["start"])]
        if template_id == "compact":
            prompt = (
                "Functions:\n"
                + "\n".join(rule_lines)
                + f"\nStart: {start}\n"
                + "Apply in order: "
                + " -> ".join(composition)
                + "\nReturn only the final symbol."
            )
        else:
            prompt = (
                "The following functions map each symbol to another symbol.\n"
                + "\n".join(rule_lines)
                + f"\nBeginning with {start}, apply "
                + ", then ".join(composition)
                + ". What symbol is obtained? Give only the answer."
            )
        target_symbol = symbols[int(task.canonical_target)]
        target = (
            target_symbol
            if answer_encoding == "symbol"
            else f"[{target_symbol}]"
        )
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
    def _symbols(vocabulary_id: str, count: int) -> list[str]:
        banks = {
            "latin": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "greek_names": [
                "alpha",
                "beta",
                "gamma",
                "delta",
                "epsilon",
                "zeta",
                "eta",
                "theta",
                "iota",
                "kappa",
                "lambda",
                "mu",
            ],
            "neutral_tokens": [f"token_{index}" for index in range(64)],
        }
        bank = banks[vocabulary_id]
        if count > len(bank):
            raise ValueError(
                f"vocabulary {vocabulary_id!r} supports at most {len(bank)} symbols"
            )
        return bank[:count]

    @staticmethod
    def _function_name(vocabulary_id: str, index: int) -> str:
        if vocabulary_id == "latin":
            return f"f{index}"
        if vocabulary_id == "greek_names":
            return f"map_{index + 11}"
        return f"operator_{index}"
