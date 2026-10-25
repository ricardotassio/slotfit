from __future__ import annotations

import unittest
from dataclasses import replace

from slotfit.domain import Assignment
from slotfit.eligibility import scheduled_window
from slotfit.evaluation import evaluate_generated_plan
from slotfit.generation import generate_scenario
from slotfit.strategies import best_fit_plan


class ScenarioEvaluationTests(unittest.TestCase):
    def test_evaluation_joins_audit_slices_after_planning(self) -> None:
        generated = generate_scenario(1400)
        plan = best_fit_plan(generated.scenario)

        result = evaluate_generated_plan(generated, plan)

        self.assertEqual(result.strategy, plan.strategy)
        self.assertEqual(result.decision_checksum, generated.manifest.decision_checksum)
        self.assertEqual(result.hard_constraint_violations, ())
        self.assertEqual(len(result.requests), len(generated.scenario.wait_requests))
        selected = next(record for record in result.requests if record.selected)
        self.assertTrue(selected.eligible_opportunity)
        self.assertTrue(selected.audit_slice.duration_band)

    def test_recovered_utilization_uses_only_factually_feasible_open_time(self) -> None:
        generated = generate_scenario(1400)
        plan = best_fit_plan(generated.scenario)

        result = evaluate_generated_plan(generated, plan)

        self.assertEqual(result.feasible_open_minutes, 90)
        self.assertEqual(
            result.recovered_utilization,
            plan.recovered_minutes / result.feasible_open_minutes,
        )

    def test_ineligible_assignment_is_reported_as_a_hard_constraint_violation(self) -> None:
        generated = generate_scenario(1400)
        plan = best_fit_plan(generated.scenario)
        ineligible = next(item for item in plan.evaluations if not item.eligible)
        interval = generated.scenario.open_intervals[0]
        request = next(
            item
            for item in generated.scenario.wait_requests
            if item.request_id == ineligible.request_id
        )
        invalid_assignment = Assignment(
            request_id=request.request_id,
            interval_id=interval.interval_id,
            scheduled_window=scheduled_window(interval, request),
        )
        invalid_plan = replace(
            plan,
            assignments=(invalid_assignment,),
            recovered_minutes=request.duration_minutes,
        )

        result = evaluate_generated_plan(generated, invalid_plan)

        self.assertEqual(len(result.hard_constraint_violations), 1)
        violation = result.hard_constraint_violations[0]
        self.assertEqual(violation.request_id, request.request_id)
        self.assertEqual(violation.reason_codes, ineligible.reason_codes)

    def test_manifest_must_have_exactly_one_audit_slice_per_request(self) -> None:
        generated = generate_scenario(1400)
        invalid_manifest = replace(
            generated.manifest,
            audit_slices=generated.manifest.audit_slices[:-1],
        )

        with self.assertRaisesRegex(ValueError, "audit slice request IDs"):
            evaluate_generated_plan(
                replace(generated, manifest=invalid_manifest),
                best_fit_plan(generated.scenario),
            )

    def test_manifest_checksum_must_match_decision_data(self) -> None:
        generated = generate_scenario(1400)
        invalid_manifest = replace(
            generated.manifest,
            decision_checksum="0" * 64,
        )

        with self.assertRaisesRegex(ValueError, "decision checksum"):
            evaluate_generated_plan(
                replace(generated, manifest=invalid_manifest),
                best_fit_plan(generated.scenario),
            )


if __name__ == "__main__":
    unittest.main()
