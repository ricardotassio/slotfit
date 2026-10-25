from __future__ import annotations

import unittest

from slotfit.generation import generate_scenario
from slotfit.longitudinal import simulate_opportunity_rounds
from slotfit.strategies import best_fit_plan, fifo_plan


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


if __name__ == "__main__":
    unittest.main()
