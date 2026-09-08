from __future__ import annotations

import random
import unittest

from reasoning_role.tasks.function_composition import FunctionCompositionTask


class FunctionCompositionTaskTest(unittest.TestCase):
    def setUp(self) -> None:
        self.family = FunctionCompositionTask()

    def test_solver_and_trace_across_parameters(self) -> None:
        for seed in range(10):
            for length in (1, 2, 4):
                with self.subTest(seed=seed, length=length):
                    task = self.family.generate(
                        random.Random(seed),
                        chain_length=length,
                        distractor_count=2,
                        presentation_order="shuffled",
                        settings={"domain_size": 7},
                    )
                    task.dependency_graph.validate()
                    self.assertEqual(
                        self.family.solve(task.canonical_problem),
                        task.canonical_target,
                    )
                    self.assertEqual(len(task.task_side_trace), length)
                    for step in task.task_side_trace:
                        self.assertNotEqual(
                            step.input_state["symbol"], step.output_state["symbol"]
                        )

    def test_presentation_order_does_not_change_semantic_payload(self) -> None:
        canonical = self.family.generate(
            random.Random(12),
            chain_length=3,
            distractor_count=2,
            presentation_order="canonical",
            settings={"domain_size": 6},
        )
        shuffled = self.family.generate(
            random.Random(12),
            chain_length=3,
            distractor_count=2,
            presentation_order="shuffled",
            settings={"domain_size": 6},
        )
        self.assertEqual(canonical.semantic_payload, shuffled.semantic_payload)
        self.assertNotEqual(
            canonical.canonical_problem["presentation_order"],
            shuffled.canonical_problem["presentation_order"],
        )

    def test_renderer_hides_trace_fields(self) -> None:
        task = self.family.generate(
            random.Random(3),
            chain_length=3,
            distractor_count=1,
            presentation_order="canonical",
            settings={"domain_size": 6},
        )
        rendered = self.family.render(
            task,
            template_id="compact",
            vocabulary_id="latin",
            answer_encoding="symbol",
        )
        self.assertNotIn("task_side_trace", rendered.prompt)
        self.assertNotIn("input_state", rendered.prompt)
        self.assertNotIn("output_state", rendered.prompt)

    def test_unknown_render_option_fails(self) -> None:
        task = self.family.generate(
            random.Random(1),
            chain_length=2,
            distractor_count=0,
            presentation_order="canonical",
            settings={},
        )
        with self.assertRaisesRegex(ValueError, "unsupported template"):
            self.family.render(
                task,
                template_id="unknown",
                vocabulary_id="latin",
                answer_encoding="symbol",
            )


if __name__ == "__main__":
    unittest.main()
