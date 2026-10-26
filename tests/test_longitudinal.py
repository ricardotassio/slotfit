from __future__ import annotations

import unittest
from collections.abc import Mapping

from slotfit.generation import generate_scenario
from slotfit.longitudinal import (
    simulate_exposure_debt_rounds,
    simulate_opportunity_rounds,
)
from slotfit.solver.optimizer import optimize_plan_with_exposure_debt
from slotfit.application.strategies import best_fit_plan, fifo_plan


class LongitudinalSimulationTests(unittest.TestCase):
    def test_same_input_and_strategy_replay_identically(self) -> None:
        generated = generate_scenario(1400)

        self.assertEqual(
            simulate_opportunity_rounds(generated, fifo_plan, rounds=4),
            simulate_opportunity_rounds(generated, fifo_plan, rounds=4),
        )

    def test_selected_requests_are_removed_from_later_rounds(self) -> None:
        result = simulate_opportunity_rounds(
            generate_scenario(1400),
            best_fit_plan,
            rounds=4,
        )
        selected_ids = [
            record.request_id
            for round_result in result.rounds
            for record in round_result.evaluation.requests
            if record.selected
        ]

        self.assertEqual(len(selected_ids), len(set(selected_ids)))

    def test_history_emits_waiting_and_starvation_inputs_without_a_threshold(self) -> None:
        generated = generate_scenario(1400)

        result = simulate_opportunity_rounds(generated, best_fit_plan, rounds=4)

        self.assertEqual(
            {item.request_id for item in result.requests},
            {item.request_id for item in generated.scenario.wait_requests},
        )
        self.assertTrue(
            any(item.unselected_compatible_opportunities > 0 for item in result.requests)
        )
        self.assertFalse(hasattr(result, "starvation_threshold"))
        self.assertFalse(hasattr(result.requests[0], "starved"))

    def test_round_count_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "rounds must be positive"):
            simulate_opportunity_rounds(
                generate_scenario(1400),
                fifo_plan,
                rounds=0,
            )

    def test_debt_aware_rounds_pass_prior_compatible_misses_to_planner(self) -> None:
        observed_debts: list[dict[str, int]] = []

        def debt_planner(scenario, debt: Mapping[str, int]):
            observed_debts.append(dict(debt))
            return optimize_plan_with_exposure_debt(
                scenario,
                exposure_debt_by_request_id=debt,
            ).plan

        result = simulate_exposure_debt_rounds(
            generate_scenario(1400),
            debt_planner,
            rounds=3,
        )

        self.assertEqual(set(observed_debts[0].values()), {0})
        self.assertTrue(any(value > 0 for value in observed_debts[1].values()))
        self.assertEqual(result.strategy, "cp-sat-exposure-debt@0.2.0")


if __name__ == "__main__":
    unittest.main()
