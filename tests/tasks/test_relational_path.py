from __future__ import annotations

import random
import unittest

from reasoning_role.tasks.relational_path import RelationalPathTask


class RelationalPathTaskTest(unittest.TestCase):
    def setUp(self) -> None:
        self.family = RelationalPathTask()

    def test_solver_and_trace_across_parameters(self) -> None:
        for seed in range(12):
            for length in (1, 2, 5):
                with self.subTest(seed=seed, length=length):
                    task = self.family.generate(
                        random.Random(seed),
                        chain_length=length,
                        distractor_count=2,
                        presentation_order="shuffled",
                        settings={},
                    )
                    task.dependency_graph.validate()
                    self.assertEqual(
                        self.family.solve(task.canonical_problem),
                        task.canonical_target,
                    )
                    self.assertNotEqual(task.canonical_target, [0, 0])
                    self.assertEqual(len(task.task_side_trace), length)

    def test_solver_ignores_stored_relevance_flag(self) -> None:
        task = self.family.generate(
            random.Random(9),
            chain_length=3,
            distractor_count=2,
            presentation_order="canonical",
            settings={},
        )
        altered = {
            **task.canonical_problem,
            "relations": [
                {**relation, "relevant": not relation["relevant"]}
                for relation in task.canonical_problem["relations"]
            ],
        }
        self.assertEqual(self.family.solve(altered), task.canonical_target)

    def test_renderer_hides_trace_fields(self) -> None:
        task = self.family.generate(
            random.Random(4),
            chain_length=3,
            distractor_count=1,
            presentation_order="canonical",
            settings={},
        )
        rendered = self.family.render(
            task,
            template_id="prose",
            vocabulary_id="names_a",
            answer_encoding="vector",
        )
        self.assertNotIn("task_side_trace", rendered.prompt)
        self.assertNotIn("offset", rendered.prompt)
        self.assertRegex(rendered.target, r"^\(-?\d+,-?\d+\)$")

    def test_unreachable_query_fails(self) -> None:
        task = self.family.generate(
            random.Random(5),
            chain_length=2,
            distractor_count=0,
            presentation_order="canonical",
            settings={},
        )
        broken = {
            **task.canonical_problem,
            "query": {"source": 0, "target": 99},
        }
        with self.assertRaisesRegex(ValueError, "unreachable"):
            self.family.solve(broken)


if __name__ == "__main__":
    unittest.main()
