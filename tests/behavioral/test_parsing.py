from __future__ import annotations

import unittest

from reasoning_role.behavioral.parsing import parse_complete, score_completion


class ParsingTest(unittest.TestCase):
    def test_function_symbol_requires_whole_ascii_token(self) -> None:
        self.assertEqual(parse_complete("alpha", "function_composition", "symbol"), "alpha")
        self.assertIsNone(
            parse_complete("The answer is alpha.", "function_composition", "symbol")
        )
        self.assertIsNone(parse_complete("Α", "function_composition", "symbol"))

    def test_bracketed_symbol(self) -> None:
        self.assertEqual(
            parse_complete("[token_3]", "function_composition", "bracketed"),
            "token_3",
        )
        self.assertIsNone(parse_complete("token_3", "function_composition", "bracketed"))

    def test_vectors_are_canonical_and_complete(self) -> None:
        self.assertEqual(parse_complete("(-2,3)", "relational_path", "vector"), (-2, 3))
        for invalid in ("(-2, 3)", "(-02,3)", "(-0,3)", "answer=(-2,3)"):
            with self.subTest(invalid=invalid):
                self.assertIsNone(parse_complete(invalid, "relational_path", "vector"))
        self.assertEqual(
            parse_complete("x=-2;y=3", "relational_path", "labeled_vector"),
            (-2, 3),
        )

    def test_outer_whitespace_is_diagnostic_not_raw_exact(self) -> None:
        score = score_completion(
            expected="A",
            completion="  A\n",
            family="function_composition",
            answer_encoding="symbol",
        )
        self.assertFalse(score["raw_exact"])
        self.assertTrue(score["trimmed_exact"])
        self.assertTrue(score["format_valid"])
        self.assertTrue(score["parsed_exact"])

    def test_embedded_correct_answer_is_invalid_extra_text(self) -> None:
        score = score_completion(
            expected="(1,0)",
            completion="The answer is (1,0).",
            family="relational_path",
            answer_encoding="vector",
        )
        self.assertFalse(score["trimmed_exact"])
        self.assertFalse(score["format_valid"])
        self.assertFalse(score["parsed_exact"])
        self.assertTrue(score["extra_text"])

    def test_failure_remains_incorrect(self) -> None:
        score = score_completion(
            expected="A",
            completion=None,
            family="function_composition",
            answer_encoding="symbol",
            error_code="inference_failure",
        )
        self.assertFalse(any(score.values()))


if __name__ == "__main__":
    unittest.main()
