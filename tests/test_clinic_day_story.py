from __future__ import annotations

import unittest
from pathlib import Path

from slotfit.application.scenarios import clinic_day_story, multi_slot_counterexample
from slotfit.application.strategies import best_fit_plan, fifo_plan
from slotfit.domain.eligibility import evaluate_request
from slotfit.domain.model import TimeWindow
from slotfit.research.generation import SPLIT_SEEDS
from slotfit.research.multi_generation import MULTI_SLOT_SEEDS
from slotfit.solver.optimizer import optimize_plan

PACKAGE_ROOT = Path(__file__).parents[1] / "src" / "slotfit"
DECISION_MODULES = (
    "domain/model.py",
    "domain/eligibility.py",
    "application/strategies.py",
    "solver/optimizer.py",
)


def _disjoint(left: TimeWindow, right: TimeWindow) -> bool:
    return left.end <= right.start or right.end <= left.start


class ClinicDayStoryTests(unittest.TestCase):
    def test_story_is_deterministic(self) -> None:
        self.assertEqual(clinic_day_story(), clinic_day_story())

    def test_story_extends_the_global_conflict_fixture(self) -> None:
        scenario, _context = clinic_day_story()
        base = multi_slot_counterexample(seed=1500)

        self.assertEqual(scenario.open_intervals, base.open_intervals)
        self.assertEqual(scenario.wait_requests[:2], base.wait_requests)
        self.assertEqual(len(scenario.wait_requests), 3)
        self.assertEqual(scenario.wait_requests[2].required_room_id, "ROOM-B")

    def test_third_request_is_ineligible_only_because_room_b_is_closed(self) -> None:
        scenario, _context = clinic_day_story()
        room_b_request = scenario.wait_requests[2]

        for interval in scenario.open_intervals:
            with self.subTest(interval=interval.interval_id):
                evaluation = evaluate_request(scenario, interval, room_b_request)
                self.assertFalse(evaluation.eligible)
                self.assertEqual(evaluation.reason_codes, ("REQUIRED_ROOM_UNAVAILABLE",))

    def test_plans_reproduce_the_counterexample_numbers(self) -> None:
        scenario, _context = clinic_day_story()

        self.assertEqual(fifo_plan(scenario).recovered_minutes, 60)
        self.assertEqual(best_fit_plan(scenario).recovered_minutes, 60)
        result = optimize_plan(scenario)
        self.assertEqual(result.plan.recovered_minutes, 120)
        self.assertEqual([phase.status for phase in result.phases], ["OPTIMAL"] * 3)
        for plan in (fifo_plan(scenario), best_fit_plan(scenario), result.plan):
            eligible_pairs = {
                (item.request_id, item.interval_id) for item in plan.evaluations if item.eligible
            }
            for assignment in plan.assignments:
                self.assertIn((assignment.request_id, assignment.interval_id), eligible_pairs)

    def test_booked_appointments_never_overlap_an_opening(self) -> None:
        scenario, context = clinic_day_story()

        for booked in context.booked:
            self.assertTrue(context.day_window.contains(booked.window))
            for interval in scenario.open_intervals:
                self.assertTrue(_disjoint(booked.window, interval.window), booked.label)
        for interval in scenario.open_intervals:
            self.assertTrue(context.day_window.contains(interval.window))
        self.assertEqual(
            {item.interval_id for item in context.cancellations},
            {item.interval_id for item in scenario.open_intervals},
        )
        self.assertEqual(context.closed_room_ids, ("ROOM-B",))

    def test_story_seed_belongs_to_no_evaluation_registry(self) -> None:
        scenario, _context = clinic_day_story()
        registered: set[int] = set()
        for registry in (SPLIT_SEEDS, MULTI_SLOT_SEEDS):
            for seeds in registry.values():
                registered.update(seeds)

        self.assertEqual(scenario.seed, 1600)
        self.assertNotIn(scenario.seed, registered)

    def test_decision_modules_never_import_the_display_context(self) -> None:
        for filename in DECISION_MODULES:
            source = (PACKAGE_ROOT / filename).read_text(encoding="utf-8")
            self.assertNotIn("day_context", source, filename)


if __name__ == "__main__":
    unittest.main()
