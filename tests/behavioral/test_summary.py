from __future__ import annotations

import hashlib
import unittest

from reasoning_role.behavioral.schema import EvaluationRecord
from reasoning_role.behavioral.summary import metric_summary, summarize, wilson_interval


def record(index: int, outcome: str) -> EvaluationRecord:
    correct = outcome == "correct"
    invalid = outcome == "invalid"
    failure = outcome == "failure"
    value = EvaluationRecord(
        schema_version="1.0",
        run_id="run:1",
        request_id=f"request:{index}",
        instance_id=f"instance:{index}",
        family="function_composition",
        split="train",
        nuisance_factors={"chain_length": 2, "answer_encoding": "symbol"},
        dataset_sha256="dataset",
        model_id="fake",
        model_revision="1",
        tokenizer_id="fake-tokenizer",
        tokenizer_revision="1",
        prompt_mode="plain",
        input_text="Prompt",
        input_sha256=hashlib.sha256(b"Prompt").hexdigest(),
        expected_answer="A",
        raw_completion=None if failure else ("A" if correct else ("Answer: A" if invalid else "B")),
        prompt_tokens=1,
        completion_tokens=None if failure else 1,
        latency_ms=0.0,
        error_code="failure" if failure else None,
        error_message="failure" if failure else None,
        raw_exact=correct,
        trimmed_exact=correct,
        format_valid=not invalid and not failure,
        parsed_answer="A" if correct else ("B" if outcome == "wrong" else None),
        parsed_exact=correct,
        empty_output=False,
        extra_text=invalid,
    )
    value.validate()
    return value


class SummaryTest(unittest.TestCase):
    def test_all_failures_remain_in_denominator(self) -> None:
        records = [record(0, "correct"), record(1, "wrong"), record(2, "invalid"), record(3, "failure")]
        metrics = metric_summary(records)
        self.assertEqual(metrics["attempted"], 4)
        self.assertEqual(metrics["trimmed_exact_rate"], 0.25)
        self.assertEqual(metrics["failure_rate"], 0.25)
        self.assertEqual(metrics["invalid_or_failure_rate"], 0.5)

    def test_wilson_interval_contains_observed_rate(self) -> None:
        low, high = wilson_interval(7, 10)
        self.assertLess(low, 0.7)
        self.assertGreater(high, 0.7)

    def test_eligibility_is_explicitly_non_claim_supporting(self) -> None:
        records = [record(index, "correct") for index in range(10)]
        summary = summarize(
            records,
            strata=["family", "chain_length"],
            eligibility={
                "overall_trimmed_exact_min": 0.8,
                "each_chain_length_trimmed_exact_min": 0.6,
                "invalid_or_inference_failure_max": 0.05,
            },
        )
        decision = summary["eligibility"]["function_composition"]
        self.assertTrue(decision["passed_provisional_gate"])
        self.assertFalse(decision["paper_claim_supported"])


if __name__ == "__main__":
    unittest.main()
