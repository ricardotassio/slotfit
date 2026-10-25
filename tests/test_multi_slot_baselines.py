from __future__ import annotations

import unittest
from dataclasses import replace

from slotfit.scenarios import multi_slot_counterexample
from slotfit.strategies import best_fit_plan, fifo_plan


class MultiSlotBaselineTests(unittest.TestCase):
    def test_fifo_exposes_the_local_choice_failure(self) -> None:
        plan = fifo_plan(multi_slot_counterexample())

        self.assertEqual(len(plan.assignments), 1)
        self.assertEqual(plan.assignments[0].request_id, "WR-FLEXIBLE")
        self.assertEqual(plan.assignments[0].interval_id, "OPEN-A")
        self.assertEqual(plan.recovered_minutes, 60)
        self.assertEqual(plan.remaining_gap_minutes, 60)

    def test_best_fit_exposes_the_same_local_tie_failure(self) -> None:
        plan = best_fit_plan(multi_slot_counterexample())

        self.assertEqual(len(plan.assignments), 1)
        self.assertEqual(plan.assignments[0].request_id, "WR-FLEXIBLE")
        self.assertEqual(plan.assignments[0].interval_id, "OPEN-A")
        self.assertEqual(plan.recovered_minutes, 60)
        self.assertEqual(plan.remaining_gap_minutes, 60)

    def test_request_is_never_assigned_twice(self) -> None:
        for strategy in (fifo_plan, best_fit_plan):
            with self.subTest(strategy=strategy.__name__):
                plan = strategy(multi_slot_counterexample())
                request_ids = [item.request_id for item in plan.assignments]
                interval_ids = [item.interval_id for item in plan.assignments]
                self.assertEqual(len(request_ids), len(set(request_ids)))
                self.assertEqual(len(interval_ids), len(set(interval_ids)))

    def test_interval_input_order_does_not_change_the_plan(self) -> None:
        scenario = multi_slot_counterexample()
        reversed_scenario = replace(
            scenario,
            open_intervals=tuple(reversed(scenario.open_intervals)),
        )

        for strategy in (fifo_plan, best_fit_plan):
            with self.subTest(strategy=strategy.__name__):
                self.assertEqual(
                    strategy(scenario).assignments,
                    strategy(reversed_scenario).assignments,
                )

    def test_every_request_interval_pair_has_an_explanation(self) -> None:
        scenario = multi_slot_counterexample()

        for strategy in (fifo_plan, best_fit_plan):
            with self.subTest(strategy=strategy.__name__):
                plan = strategy(scenario)
                self.assertEqual(
                    len(plan.evaluations),
                    len(scenario.wait_requests) * len(scenario.open_intervals),
                )
                self.assertTrue(
                    all(item.eligible or item.reason_codes for item in plan.evaluations)
                )


if __name__ == "__main__":
    unittest.main()
