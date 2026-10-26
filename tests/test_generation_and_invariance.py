from __future__ import annotations

import unittest
from dataclasses import fields, replace

from slotfit.domain.model import Scenario
from slotfit.evaluation import evaluate_generated_plan
from slotfit.generation import EvaluationSplit, SPLIT_SEEDS, generate_scenario
from slotfit.strategies import best_fit_plan, fifo_plan


def _selected_joined_order(scenario: Scenario, strategy: str) -> int:
    plan = fifo_plan(scenario) if strategy == "fifo" else best_fit_plan(scenario)
    selected_id = plan.assignments[0].request_id
    return next(
        request.joined_order
        for request in scenario.wait_requests
        if request.request_id == selected_id
    )


class GeneratedScenarioTests(unittest.TestCase):
    def test_same_seed_and_split_replay_identically(self) -> None:
        self.assertEqual(
            generate_scenario(1400, split=EvaluationSplit.DEVELOPMENT),
            generate_scenario(1400, split=EvaluationSplit.DEVELOPMENT),
        )

    def test_different_seeds_change_decision_content(self) -> None:
        first = generate_scenario(1400).scenario.wait_requests
        second = generate_scenario(1401).scenario.wait_requests

        self.assertNotEqual(first, second)

    def test_manifest_records_version_split_and_checksum(self) -> None:
        generated = generate_scenario(1400, split=EvaluationSplit.CHALLENGE)

        self.assertEqual(generated.manifest.seed, 1400)
        self.assertEqual(generated.manifest.split, EvaluationSplit.CHALLENGE)
        self.assertTrue(generated.manifest.generator_version)
        self.assertEqual(len(generated.manifest.decision_checksum), 64)

    def test_registered_split_seeds_are_disjoint(self) -> None:
        seed_sets = [set(seeds) for seeds in SPLIT_SEEDS.values()]

        for index, seed_set in enumerate(seed_sets):
            other_seeds = set().union(*(seed_sets[:index] + seed_sets[index + 1 :]))
            self.assertTrue(seed_set.isdisjoint(other_seeds))

    def test_audit_slices_are_not_part_of_strategy_input(self) -> None:
        generated = generate_scenario(1400)
        scenario_fields = {field.name for field in fields(Scenario)}

        self.assertNotIn("audit_slices", scenario_fields)
        self.assertFalse(hasattr(generated.scenario, "audit_slices"))
        self.assertEqual(
            len(generated.manifest.audit_slices),
            len(generated.scenario.wait_requests),
        )
        dimension_values = generated.manifest.audit_slices[0].dimension_values()
        self.assertEqual(
            tuple(dimension for dimension, _value in dimension_values),
            (
                "duration_band",
                "availability_band",
                "resource_band",
                "wait_age_band",
                "notice_band",
            ),
        )

    def test_opaque_identifiers_do_not_change_selected_position(self) -> None:
        scenario = generate_scenario(1400).scenario
        renamed_requests = tuple(
            replace(
                request,
                request_id=f"OPAQUE-{len(scenario.wait_requests) - index + 1:03d}",
            )
            for index, request in enumerate(scenario.wait_requests, start=1)
        )
        renamed_intervals = tuple(
            replace(interval, interval_id=f"INTERVAL-{index:03d}")
            for index, interval in enumerate(scenario.open_intervals, start=1)
        )
        renamed = replace(
            scenario,
            scenario_id="opaque-scenario",
            wait_requests=renamed_requests,
            open_intervals=renamed_intervals,
        )

        for strategy in ("fifo", "best-fit"):
            with self.subTest(strategy=strategy):
                self.assertEqual(
                    _selected_joined_order(scenario, strategy),
                    _selected_joined_order(renamed, strategy),
                )

        # Mutation sentinel: a deliberately broken lexical-ID policy changes its
        # decision under this exact counterfactual, proving the fixture can expose
        # identifier leakage.
        broken_original = min(
            scenario.wait_requests,
            key=lambda request: request.request_id,
        ).joined_order
        broken_renamed = min(
            renamed.wait_requests,
            key=lambda request: request.request_id,
        ).joined_order
        self.assertNotEqual(broken_original, broken_renamed)

    def test_input_order_does_not_change_selected_request(self) -> None:
        scenario = generate_scenario(1400).scenario
        reversed_scenario = replace(
            scenario,
            wait_requests=tuple(reversed(scenario.wait_requests)),
        )

        for strategy in (fifo_plan, best_fit_plan):
            with self.subTest(strategy=strategy.__name__):
                original = strategy(scenario)
                reordered = strategy(reversed_scenario)
                self.assertEqual(original.assignments, reordered.assignments)
                self.assertEqual(original.recovered_minutes, reordered.recovered_minutes)

    def test_ineligible_request_does_not_change_assignments(self) -> None:
        scenario = generate_scenario(1400).scenario
        added = replace(
            scenario.wait_requests[0],
            request_id="INELIGIBLE-REQUEST",
            joined_order=max(item.joined_order for item in scenario.wait_requests) + 1,
            communication_consent=False,
        )
        extended = replace(
            scenario,
            wait_requests=scenario.wait_requests + (added,),
        )

        for strategy in (fifo_plan, best_fit_plan):
            with self.subTest(strategy=strategy.__name__):
                self.assertEqual(
                    strategy(scenario).assignments,
                    strategy(extended).assignments,
                )

    def test_duplicate_request_identity_is_rejected(self) -> None:
        scenario = generate_scenario(1400).scenario

        with self.assertRaisesRegex(ValueError, "request_id values must be unique"):
            replace(
                scenario,
                wait_requests=scenario.wait_requests + (scenario.wait_requests[0],),
            )

    def test_every_registered_seed_runs_both_baselines(self) -> None:
        for split, seeds in SPLIT_SEEDS.items():
            for seed in seeds:
                with self.subTest(split=split, seed=seed):
                    generated = generate_scenario(seed, split=split)
                    scenario = generated.scenario
                    for strategy in (fifo_plan, best_fit_plan):
                        plan = strategy(scenario)
                        evaluation = evaluate_generated_plan(generated, plan)
                        self.assertEqual(len(plan.assignments), 1)
                        self.assertEqual(evaluation.hard_constraint_violations, ())
                        selected_id = plan.assignments[0].request_id
                        selected_evaluation = next(
                            item for item in plan.evaluations if item.request_id == selected_id
                        )
                        self.assertTrue(selected_evaluation.eligible)
                        self.assertTrue(
                            all(
                                evaluation.reason_codes
                                for evaluation in plan.evaluations
                                if not evaluation.eligible
                            )
                        )


if __name__ == "__main__":
    unittest.main()
