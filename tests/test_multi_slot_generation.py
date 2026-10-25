from __future__ import annotations

import unittest

from slotfit.evaluation import evaluate_generated_plan
from slotfit.generation import EvaluationSplit
from slotfit.multi_generation import MULTI_SLOT_SEEDS, generate_multi_slot_scenario
from slotfit.optimizer import SolverStatus, optimize_plan
from slotfit.strategies import best_fit_plan, fifo_plan


class MultiSlotGenerationTests(unittest.TestCase):
    def test_engineering_seed_registries_have_declared_sizes_and_are_disjoint(self) -> None:
        self.assertEqual(len(MULTI_SLOT_SEEDS[EvaluationSplit.DEVELOPMENT]), 40)
        self.assertEqual(len(MULTI_SLOT_SEEDS[EvaluationSplit.CALIBRATION]), 40)
        self.assertEqual(len(MULTI_SLOT_SEEDS[EvaluationSplit.REGRESSION]), 20)
        seed_sets = [set(seeds) for seeds in MULTI_SLOT_SEEDS.values()]

        for index, seed_set in enumerate(seed_sets):
            others = set().union(*(seed_sets[:index] + seed_sets[index + 1 :]))
            self.assertTrue(seed_set.isdisjoint(others))

    def test_same_seed_replays_and_different_seed_varies(self) -> None:
        first = generate_multi_slot_scenario(1201)

        self.assertEqual(first, generate_multi_slot_scenario(1201))
        self.assertNotEqual(first.scenario, generate_multi_slot_scenario(1202).scenario)

    def test_manifest_and_scenario_have_the_declared_shape(self) -> None:
        generated = generate_multi_slot_scenario(1201)

        self.assertEqual(len(generated.scenario.open_intervals), 3)
        self.assertEqual(len(generated.scenario.wait_requests), 10)
        self.assertEqual(len(generated.manifest.audit_slices), 10)
        self.assertEqual(generated.manifest.generator_version, "slotfit-multislot-v1")
        self.assertEqual(generated.manifest.distribution_config_id, "multislot-operational-v1")

    def test_every_development_seed_runs_all_strategies_without_violations(self) -> None:
        for seed in MULTI_SLOT_SEEDS[EvaluationSplit.DEVELOPMENT]:
            with self.subTest(seed=seed):
                generated = generate_multi_slot_scenario(seed)
                plans = [fifo_plan(generated.scenario), best_fit_plan(generated.scenario)]
                optimized = optimize_plan(generated.scenario)
                self.assertEqual(optimized.status, SolverStatus.OPTIMAL)
                self.assertTrue(optimized.optimized)
                plans.append(optimized.plan)

                for plan in plans:
                    evaluation = evaluate_generated_plan(generated, plan)
                    self.assertEqual(evaluation.hard_constraint_violations, ())


if __name__ == "__main__":
    unittest.main()
