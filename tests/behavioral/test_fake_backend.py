from __future__ import annotations

import unittest

from reasoning_role.behavioral.backends.fake import FakeBackend
from reasoning_role.behavioral.parsing import score_completion
from reasoning_role.behavioral.schema import InferenceRequest


def request(
    expected: str = "A",
    family: str = "function_composition",
    encoding: str = "symbol",
) -> InferenceRequest:
    return InferenceRequest(
        request_id="request:1",
        instance_id="instance:1",
        prompt="Return an answer.",
        expected_answer=expected,
        family=family,
        answer_encoding=encoding,
        nuisance_factors={"chain_length": 2},
    )


def outcome_config(outcome: str) -> dict[str, object]:
    percentages = {name: 0 for name in ("correct", "wrong", "invalid", "failure")}
    percentages[outcome] = 100
    return {"prompt_mode": "plain", "outcome_percentages": percentages}


class FakeBackendTest(unittest.TestCase):
    def test_every_outcome_mode(self) -> None:
        for outcome in ("correct", "wrong", "invalid", "failure"):
            with self.subTest(outcome=outcome):
                backend = FakeBackend(outcome_config(outcome))
                result = backend.generate([request()])[0]
                result.validate()
                if outcome == "failure":
                    self.assertIsNotNone(result.error_code)
                    continue
                score = score_completion(
                    expected="A",
                    completion=result.completion,
                    family="function_composition",
                    answer_encoding="symbol",
                )
                if outcome == "correct":
                    self.assertTrue(score["trimmed_exact"])
                elif outcome == "wrong":
                    self.assertTrue(score["format_valid"])
                    self.assertFalse(score["parsed_exact"])
                else:
                    self.assertFalse(score["format_valid"])
                    self.assertTrue(score["extra_text"])

    def test_valid_wrong_vector(self) -> None:
        backend = FakeBackend(outcome_config("wrong"))
        item = request("(-2,3)", "relational_path", "vector")
        result = backend.generate([item])[0]
        score = score_completion(
            expected=item.expected_answer,
            completion=result.completion,
            family=item.family,
            answer_encoding=item.answer_encoding,
        )
        self.assertTrue(score["format_valid"])
        self.assertFalse(score["parsed_exact"])

    def test_results_are_deterministic(self) -> None:
        backend = FakeBackend(
            {
                "outcome_percentages": {
                    "correct": 25,
                    "wrong": 25,
                    "invalid": 25,
                    "failure": 25,
                }
            }
        )
        requests = [
            InferenceRequest(
                request_id=f"request:{index}",
                instance_id=f"instance:{index}",
                prompt="Prompt",
                expected_answer="A",
                family="function_composition",
                answer_encoding="symbol",
                nuisance_factors={},
            )
            for index in range(20)
        ]
        self.assertEqual(backend.generate(requests), backend.generate(requests))

    def test_request_has_no_task_trace_field(self) -> None:
        self.assertFalse(hasattr(request(), "task_side_trace"))


if __name__ == "__main__":
    unittest.main()
