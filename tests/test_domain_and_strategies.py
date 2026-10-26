from __future__ import annotations

import unittest
from dataclasses import replace

from slotfit.application.scenarios import demo_scenario
from slotfit.application.strategies import best_fit_plan, fifo_plan


class DemoScenarioTests(unittest.TestCase):
    def test_demo_scenario_is_deterministic(self) -> None:
        self.assertEqual(demo_scenario(1400), demo_scenario(1400))
        self.assertNotEqual(demo_scenario(1400).scenario_id, demo_scenario(1401).scenario_id)

    def test_fifo_selects_oldest_eligible_request(self) -> None:
        plan = fifo_plan(demo_scenario())

        self.assertEqual(plan.assignments[0].request_id, "WR-001")
        self.assertEqual(plan.recovered_minutes, 30)
        self.assertEqual(plan.remaining_gap_minutes, 60)

    def test_best_fit_selects_request_with_smallest_remaining_gap(self) -> None:
        plan = best_fit_plan(demo_scenario())

        self.assertEqual(plan.assignments[0].request_id, "WR-002")
        self.assertEqual(plan.recovered_minutes, 75)
        self.assertEqual(plan.remaining_gap_minutes, 15)

    def test_unavailable_required_room_has_an_explicit_reason(self) -> None:
        plan = best_fit_plan(demo_scenario())
        wr003 = next(item for item in plan.evaluations if item.request_id == "WR-003")

        self.assertFalse(wr003.eligible)
        self.assertEqual(wr003.reason_codes, ("REQUIRED_ROOM_UNAVAILABLE",))

    def test_request_without_consent_is_never_selected(self) -> None:
        scenario = demo_scenario()
        requests = tuple(
            replace(request, communication_consent=False)
            if request.request_id == "WR-001"
            else request
            for request in scenario.wait_requests
        )
        plan = fifo_plan(replace(scenario, wait_requests=requests))

        self.assertEqual(plan.assignments[0].request_id, "WR-002")
        wr001 = next(item for item in plan.evaluations if item.request_id == "WR-001")
        self.assertIn("NO_COMMUNICATION_CONSENT", wr001.reason_codes)


if __name__ == "__main__":
    unittest.main()

