from __future__ import annotations

import unittest
from dataclasses import replace

from slotfit.optimizer import (
    SolverConfig,
    SolverStatus,
    optimize_plan,
    optimize_plan_with_bounded_recovery,
    optimize_plan_with_exposure_debt,
    optimize_plan_with_placement_scarcity,
)
from slotfit.application.scenarios import multi_slot_counterexample


def _assignment_positions(scenario, result) -> set[tuple[int, int]]:
    request_positions = {
        request.request_id: request.joined_order for request in scenario.wait_requests
    }
    interval_positions = {
        interval.interval_id: position
        for position, interval in enumerate(
            sorted(scenario.open_intervals, key=lambda item: item.window.start),
            start=1,
        )
    }
    return {
        (
            request_positions[assignment.request_id],
            interval_positions[assignment.interval_id],
        )
        for assignment in result.plan.assignments
    }


class CpSatOptimizerTests(unittest.TestCase):
    def test_optimizer_finds_the_global_120_minute_plan(self) -> None:
        result = optimize_plan(multi_slot_counterexample())

        self.assertEqual(result.status, SolverStatus.OPTIMAL)
        self.assertTrue(result.optimized)
        self.assertEqual(result.plan.recovered_minutes, 120)
        self.assertEqual(result.plan.remaining_gap_minutes, 0)
        self.assertEqual(
            {(item.request_id, item.interval_id) for item in result.plan.assignments},
            {("WR-CONSTRAINED", "OPEN-A"), ("WR-FLEXIBLE", "OPEN-B")},
        )

    def test_all_three_lexicographic_phases_are_optimal(self) -> None:
        result = optimize_plan(multi_slot_counterexample())

        self.assertEqual(
            [(phase.name, phase.status, phase.objective_value) for phase in result.phases],
            [
                ("recovered-minutes", SolverStatus.OPTIMAL, 120),
                ("requests-served", SolverStatus.OPTIMAL, 2),
                ("wait-age-score", SolverStatus.OPTIMAL, 3),
            ],
        )

    def test_optimizer_assigns_only_eligible_unique_pairs(self) -> None:
        result = optimize_plan(multi_slot_counterexample())
        eligible_pairs = {
            (item.request_id, item.interval_id)
            for item in result.plan.evaluations
            if item.eligible
        }
        selected_pairs = [
            (item.request_id, item.interval_id) for item in result.plan.assignments
        ]

        self.assertTrue(set(selected_pairs).issubset(eligible_pairs))
        self.assertEqual(
            len({request_id for request_id, _interval_id in selected_pairs}),
            len(selected_pairs),
        )
        self.assertEqual(
            len({interval_id for _request_id, interval_id in selected_pairs}),
            len(selected_pairs),
        )

    def test_opaque_identifiers_do_not_change_assignment_positions(self) -> None:
        scenario = multi_slot_counterexample()
        renamed_requests = tuple(
            replace(request, request_id=f"OPAQUE-R-{3 - position}")
            for position, request in enumerate(scenario.wait_requests, start=1)
        )
        renamed_intervals = tuple(
            replace(interval, interval_id=f"OPAQUE-I-{3 - position}")
            for position, interval in enumerate(scenario.open_intervals, start=1)
        )
        renamed = replace(
            scenario,
            scenario_id="renamed-multi-slot",
            wait_requests=renamed_requests,
            open_intervals=renamed_intervals,
        )

        self.assertEqual(
            _assignment_positions(scenario, optimize_plan(scenario)),
            _assignment_positions(renamed, optimize_plan(renamed)),
        )

    def test_input_order_does_not_change_assignment_positions(self) -> None:
        scenario = multi_slot_counterexample()
        reordered = replace(
            scenario,
            wait_requests=tuple(reversed(scenario.wait_requests)),
            open_intervals=tuple(reversed(scenario.open_intervals)),
        )

        self.assertEqual(
            _assignment_positions(scenario, optimize_plan(scenario)),
            _assignment_positions(reordered, optimize_plan(reordered)),
        )

    def test_deterministic_limit_is_reported_without_a_fallback(self) -> None:
        result = optimize_plan(
            multi_slot_counterexample(),
            config=SolverConfig(max_deterministic_time=1e-9),
        )

        self.assertEqual(result.status, SolverStatus.UNKNOWN)
        self.assertFalse(result.optimized)
        self.assertEqual(len(result.phases), 1)
        self.assertEqual(result.phases[0].status, SolverStatus.UNKNOWN)
        self.assertEqual(result.plan.strategy, "cp-sat-lexicographic@0.1.0")
        self.assertEqual(result.plan.assignments, ())

    def test_exposure_debt_changes_only_the_residual_choice(self) -> None:
        scenario = multi_slot_counterexample()
        one_interval = replace(
            scenario,
            scenario_id="exposure-debt-residual-choice",
            open_intervals=(scenario.open_intervals[0],),
        )

        result = optimize_plan_with_exposure_debt(
            one_interval,
            exposure_debt_by_request_id={"WR-CONSTRAINED": 2},
        )

        self.assertEqual(result.plan.recovered_minutes, 60)
        self.assertEqual(len(result.plan.assignments), 1)
        self.assertEqual(result.plan.assignments[0].request_id, "WR-CONSTRAINED")
        self.assertEqual(
            [(phase.name, phase.objective_value) for phase in result.phases],
            [
                ("recovered-minutes", 60),
                ("requests-served", 1),
                ("exposure-debt-score", 2),
                ("wait-age-score", 1),
            ],
        )

    def test_exposure_debt_defaults_missing_active_requests_to_zero(self) -> None:
        result = optimize_plan_with_exposure_debt(
            multi_slot_counterexample(),
            exposure_debt_by_request_id={},
        )

        self.assertTrue(result.optimized)
        self.assertEqual(result.phases[2].objective_value, 0)

    def test_exposure_debt_rejects_negative_and_unknown_values(self) -> None:
        scenario = multi_slot_counterexample()

        with self.assertRaisesRegex(ValueError, "non-negative"):
            optimize_plan_with_exposure_debt(
                scenario,
                exposure_debt_by_request_id={"WR-FLEXIBLE": -1},
            )
        with self.assertRaisesRegex(ValueError, "unknown request"):
            optimize_plan_with_exposure_debt(
                scenario,
                exposure_debt_by_request_id={"NOT-IN-SCENARIO": 1},
            )
        with self.assertRaisesRegex(ValueError, "non-negative integers"):
            optimize_plan_with_exposure_debt(
                scenario,
                exposure_debt_by_request_id={"WR-FLEXIBLE": 1.5},
            )

    def test_exposure_debt_replays_the_same_decision_and_objectives(self) -> None:
        scenario = multi_slot_counterexample()
        debt = {"WR-FLEXIBLE": 1, "WR-CONSTRAINED": 2}

        first = optimize_plan_with_exposure_debt(
            scenario,
            exposure_debt_by_request_id=debt,
        )
        second = optimize_plan_with_exposure_debt(
            scenario,
            exposure_debt_by_request_id=debt,
        )

        self.assertEqual(first.plan, second.plan)
        self.assertEqual(
            [(phase.name, phase.status, phase.objective_value) for phase in first.phases],
            [(phase.name, phase.status, phase.objective_value) for phase in second.phases],
        )

    def test_placement_scarcity_prefers_two_constrained_residual_choices(self) -> None:
        scenario = multi_slot_counterexample()
        constrained_b = replace(
            scenario.wait_requests[1],
            request_id="WR-CONSTRAINED-B",
            joined_order=3,
            availability_windows=(scenario.open_intervals[1].window,),
        )
        three_requests = replace(
            scenario,
            scenario_id="placement-scarcity-residual-choice",
            wait_requests=scenario.wait_requests + (constrained_b,),
        )

        result = optimize_plan_with_placement_scarcity(
            three_requests,
            exposure_debt_by_request_id={},
        )

        self.assertEqual(result.plan.recovered_minutes, 120)
        self.assertEqual(len(result.plan.assignments), 2)
        self.assertEqual(
            {assignment.request_id for assignment in result.plan.assignments},
            {"WR-CONSTRAINED", "WR-CONSTRAINED-B"},
        )
        self.assertEqual(
            [(phase.name, phase.objective_value) for phase in result.phases],
            [
                ("recovered-minutes", 120),
                ("requests-served", 2),
                ("exposure-debt-score", 0),
                ("placement-scarcity-score", 4),
                ("wait-age-score", 3),
            ],
        )

    def test_bounded_recovery_allows_debt_choice_only_above_floor(self) -> None:
        scenario = multi_slot_counterexample()
        one_interval = replace(
            scenario,
            scenario_id="bounded-recovery-choice",
            open_intervals=(scenario.open_intervals[0],),
            wait_requests=(
                scenario.wait_requests[0],
                replace(scenario.wait_requests[1], duration_minutes=54),
            ),
        )

        result = optimize_plan_with_bounded_recovery(
            one_interval,
            exposure_debt_by_request_id={"WR-CONSTRAINED": 2},
            minimum_recovered_ratio=0.90,
        )

        self.assertEqual(result.plan.recovered_minutes, 54)
        self.assertEqual(result.plan.assignments[0].request_id, "WR-CONSTRAINED")
        self.assertEqual(
            [(phase.name, phase.objective_value) for phase in result.phases],
            [
                ("recovered-minutes-ceiling", 60),
                ("requests-served", 1),
                ("exposure-debt-score", 2),
                ("placement-scarcity-score", 1),
                ("wait-age-score", 1),
            ],
        )

    def test_bounded_recovery_rejects_invalid_floor(self) -> None:
        for invalid in (0.0, -0.1, 1.01):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "within"):
                    optimize_plan_with_bounded_recovery(
                        multi_slot_counterexample(),
                        exposure_debt_by_request_id={},
                        minimum_recovered_ratio=invalid,
                    )


if __name__ == "__main__":
    unittest.main()
