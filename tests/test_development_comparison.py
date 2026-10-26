from __future__ import annotations

import unittest

from slotfit.research.comparison import compare_engineering_split
from slotfit.research.generation import EvaluationSplit


class DevelopmentComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = compare_engineering_split(EvaluationSplit.DEVELOPMENT)

    def test_report_contains_all_development_seeds_and_strategies(self) -> None:
        self.assertEqual(self.report.seed_count, 40)
        self.assertEqual(len(self.report.scenarios), 120)
        self.assertEqual(
            {summary.strategy for summary in self.report.strategies},
            {
                "fifo-eligible@0.2.0",
                "local-best-fit@0.2.0",
                "cp-sat-bounded-recovery@0.4.0",
            },
        )

    def test_all_development_plans_preserve_hard_constraints(self) -> None:
        self.assertTrue(
            all(item.hard_constraint_violations == 0 for item in self.report.scenarios)
        )

    def test_all_development_counterfactuals_are_stable(self) -> None:
        self.assertTrue(all(not item.opaque_id_flip for item in self.report.scenarios))
        self.assertTrue(all(not item.input_order_flip for item in self.report.scenarios))

    def test_optimizer_is_optimal_and_not_less_efficient_than_baselines(self) -> None:
        summaries = {item.strategy: item for item in self.report.strategies}
        optimized = summaries["cp-sat-bounded-recovery@0.4.0"]

        self.assertEqual(optimized.optimized_runs, 40)
        self.assertGreaterEqual(
            optimized.mean_recovered_utilization,
            summaries["fifo-eligible@0.2.0"].mean_recovered_utilization,
        )
        self.assertGreaterEqual(
            optimized.mean_recovered_utilization,
            summaries["local-best-fit@0.2.0"].mean_recovered_utilization,
        )

    def test_candidate_records_the_exposure_debt_and_scarcity_phases(self) -> None:
        candidate_records = [
            item
            for item in self.report.scenarios
            if item.strategy == "cp-sat-bounded-recovery@0.4.0"
        ]

        self.assertEqual(len(candidate_records), 40)
        self.assertTrue(
            all(
                item.phase_statuses
                == ("OPTIMAL", "OPTIMAL", "OPTIMAL", "OPTIMAL", "OPTIMAL")
                for item in candidate_records
            )
        )

    def test_report_keeps_efficiency_and_exclusion_metrics_separate(self) -> None:
        for summary in self.report.strategies:
            self.assertGreater(summary.history_count, 0)
            self.assertGreaterEqual(summary.starvation_rate_k3, 0.0)
            self.assertLessEqual(summary.starvation_rate_k3, 1.0)
            self.assertTrue(summary.slices)
            self.assertTrue(
                all(slice_result.support >= 0 for slice_result in summary.slices)
            )

    def test_candidate_is_rejected_when_a_slice_guardrail_fails(self) -> None:
        checks = {item.name: item for item in self.report.guardrails}

        self.assertFalse(self.report.candidate_accepted)
        self.assertEqual(self.report.starvation_k, 3)
        self.assertEqual(checks["starvation-rate-k3-degradation"].limit, 0.05)
        self.assertEqual(checks["worst-supported-slice-gap-degradation"].limit, 0.10)
        self.assertTrue(checks["hard-constraint-violations"].passed)
        self.assertTrue(checks["opaque-id-flips"].passed)
        self.assertTrue(checks["input-order-flips"].passed)
        self.assertTrue(checks["starvation-rate-k3-degradation"].passed)
        self.assertFalse(checks["worst-supported-slice-gap-degradation"].passed)
        self.assertGreater(
            checks["worst-supported-slice-gap-degradation"].observed_value,
            checks["worst-supported-slice-gap-degradation"].limit,
        )
        self.assertAlmostEqual(
            checks["worst-supported-slice-gap-degradation"].observed_value,
            0.10801758425790253,
        )
        self.assertIn(
            "duration_band=short",
            checks["worst-supported-slice-gap-degradation"].detail,
        )

    def test_report_is_deterministic(self) -> None:
        self.assertEqual(
            self.report,
            compare_engineering_split(EvaluationSplit.DEVELOPMENT),
        )


if __name__ == "__main__":
    unittest.main()
