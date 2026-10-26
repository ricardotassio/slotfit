from __future__ import annotations

import re
import unittest
from pathlib import Path

from slotfit.domain.model import CandidateEvaluation
from slotfit.domain.explanations import (
    ELIGIBLE_EXPLANATION,
    REASON_CODES,
    explain,
    explain_evaluation,
)


ELIGIBILITY_SOURCE = Path(__file__).parents[1] / "src" / "slotfit" / "domain/eligibility.py"
AUDIT_BAND_VOCABULARY = ("scarce", "narrow", "aging", "band", "slice")


class ExplanationTests(unittest.TestCase):
    def test_every_reason_code_emitted_by_eligibility_has_an_explanation(self) -> None:
        source = ELIGIBILITY_SOURCE.read_text(encoding="utf-8")
        emitted = set(re.findall(r'reasons\.append\("([A-Z_]+)"\)', source))

        self.assertEqual(emitted, set(REASON_CODES))
        for code in REASON_CODES:
            with self.subTest(code=code):
                self.assertTrue(explain(code).endswith("."))

    def test_unknown_code_is_rejected_instead_of_guessed(self) -> None:
        with self.assertRaises(KeyError):
            explain("NOT_A_REASON")

    def test_eligible_evaluation_returns_the_eligible_sentence(self) -> None:
        evaluation = CandidateEvaluation(
            request_id="WR-1", interval_id="OPEN-A", eligible=True, reason_codes=()
        )

        self.assertEqual(explain_evaluation(evaluation), (ELIGIBLE_EXPLANATION,))

    def test_ineligible_evaluation_returns_one_sentence_per_code(self) -> None:
        evaluation = CandidateEvaluation(
            request_id="WR-1",
            interval_id="OPEN-A",
            eligible=False,
            reason_codes=("REQUIRED_ROOM_UNAVAILABLE", "INSUFFICIENT_NOTICE"),
        )

        self.assertEqual(
            explain_evaluation(evaluation),
            (explain("REQUIRED_ROOM_UNAVAILABLE"), explain("INSUFFICIENT_NOTICE")),
        )

    def test_explanations_never_use_audit_band_vocabulary(self) -> None:
        texts = [ELIGIBLE_EXPLANATION, *(explain(code) for code in REASON_CODES)]

        for text in texts:
            for word in AUDIT_BAND_VOCABULARY:
                self.assertNotIn(word, text.lower(), text)


if __name__ == "__main__":
    unittest.main()
