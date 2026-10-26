from __future__ import annotations

import unittest
from dataclasses import fields, replace

from slotfit.research.alternative_diagnostic import (
    diagnose_development_alternatives,
    enumerate_primary_optimal_plans,
)
from slotfit.domain.model import Scenario
from slotfit.application.scenarios import multi_slot_counterexample


class AlternativeDiagnosticTests(unittest.TestCase):
    def test_enumerator_accepts_decision_scenario_without_audit_metadata(self) -> None:
        self.assertNotIn("audit_slices", {field.name for field in fields(Scenario)})

        scenario = multi_slot_counterexample()
        plans = enumerate_primary_optimal_plans(scenario)

        self.assertTrue(plans)
        self.assertTrue(all(plan.recovered_minutes == 120 for plan in plans))
        self.assertTrue(all(len(plan.assignments) == 2 for plan in plans))

    def test_enumerator_keeps_both_primary_optimal_residual_choices(self) -> None:
        scenario = multi_slot_counterexample()
        one_interval = replace(
            scenario,
            scenario_id="two-primary-optimal-choices",
            open_intervals=(scenario.open_intervals[0],),
        )

        plans = enumerate_primary_optimal_plans(one_interval)

        self.assertEqual(len(plans), 2)
        self.assertEqual(
            {plan.assignments[0].request_id for plan in plans},
            {"WR-FLEXIBLE", "WR-CONSTRAINED"},
        )
        self.assertTrue(all(plan.recovered_minutes == 60 for plan in plans))

    def test_development_diagnostic_is_deterministic_and_covers_all_rounds(self) -> None:
        first = diagnose_development_alternatives()
        second = diagnose_development_alternatives()

        self.assertEqual(first, second)
        self.assertEqual(first.seed_count, 40)
        self.assertGreater(first.round_count, 0)
        self.assertLessEqual(first.round_count, 200)
        self.assertGreaterEqual(first.rounds_with_multiple_primary_plans, 0)
        self.assertTrue(first.slices)

    def test_every_v2_round_is_primary_optimal(self) -> None:
        report = diagnose_development_alternatives()

        self.assertEqual(report.non_primary_optimal_v2_rounds, 0)

    def test_failing_slice_has_efficiency_equivalent_local_alternatives(self) -> None:
        report = diagnose_development_alternatives()
        moderate_notice = next(
            item
            for item in report.slices
            if item.dimension == "notice_band" and item.value == "moderate"
        )

        self.assertEqual(report.round_count, 200)
        self.assertEqual(report.rounds_with_multiple_primary_plans, 34)
        self.assertTrue(moderate_notice.supported)
        self.assertEqual(moderate_notice.rounds_with_improving_alternative, 8)
        self.assertEqual(moderate_notice.additional_exposure_capacity, 9)


if __name__ == "__main__":
    unittest.main()
