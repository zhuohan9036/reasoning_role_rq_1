from __future__ import annotations

import unittest

from reasoning_role.tasks.schema import (
    SCHEMA_VERSION,
    CanonicalInstance,
    DependencyEdge,
    DependencyGraph,
    DependencyNode,
    TaskSideTraceStep,
)


def make_instance() -> CanonicalInstance:
    graph = DependencyGraph(
        nodes=(
            DependencyNode("step_0", "op", {}),
            DependencyNode("step_1", "op", {}),
        ),
        edges=(DependencyEdge("step_0", "step_1"),),
        output_node_id="step_1",
    )
    return CanonicalInstance(
        schema_version=SCHEMA_VERSION,
        instance_id="example:1",
        family="example",
        generator_version="1.0",
        canonical_problem={"value": 1},
        prompt="Question",
        target="Answer",
        dependency_graph=graph,
        task_side_trace=(
            TaskSideTraceStep("trace_0", "step_0", "op", {"v": 0}, {"v": 1}),
            TaskSideTraceStep("trace_1", "step_1", "op", {"v": 1}, {"v": 2}),
        ),
        candidate_operations=("op",),
        nuisance_factors={"length": 2},
        split="train",
        group_keys={
            "semantic_id": "semantic:1",
            "canonical_problem_hash": "canonical:1",
            "prompt_hash": "prompt:1",
        },
    )


class DependencyGraphTest(unittest.TestCase):
    def test_valid_graph_and_round_trip(self) -> None:
        instance = make_instance()
        instance.validate()
        restored = CanonicalInstance.from_dict(instance.to_dict())
        restored.validate()
        self.assertEqual(restored.to_dict(), instance.to_dict())

    def test_cycle_is_rejected(self) -> None:
        graph = DependencyGraph(
            nodes=(
                DependencyNode("a", "op", {}),
                DependencyNode("b", "op", {}),
            ),
            edges=(DependencyEdge("a", "b"), DependencyEdge("b", "a")),
            output_node_id="b",
        )
        with self.assertRaisesRegex(ValueError, "acyclic"):
            graph.validate()

    def test_non_contributing_node_is_rejected(self) -> None:
        graph = DependencyGraph(
            nodes=(
                DependencyNode("a", "op", {}),
                DependencyNode("b", "op", {}),
            ),
            edges=(),
            output_node_id="b",
        )
        with self.assertRaisesRegex(ValueError, "non-contributing"):
            graph.validate()

    def test_trace_order_is_checked(self) -> None:
        instance = make_instance()
        invalid = CanonicalInstance(
            **{
                **instance.__dict__,
                "task_side_trace": tuple(reversed(instance.task_side_trace)),
            }
        )
        with self.assertRaisesRegex(ValueError, "dependency order"):
            invalid.validate()


if __name__ == "__main__":
    unittest.main()
