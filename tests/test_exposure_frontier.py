from __future__ import annotations

import unittest

from slotfit.research.exposure_frontier import build_local_exposure_frontier


class ExposureFrontierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.frontier = build_local_exposure_frontier()

    def test_frontier_is_deterministic_and_uses_predeclared_floors(self) -> None:
        self.assertEqual(self.frontier, build_local_exposure_frontier())
        self.assertEqual(
            tuple(point.minimum_recovered_ratio for point in self.frontier.points),
            (1.0, 0.95, 0.9, 0.8),
        )
        self.assertEqual(self.frontier.target_dimension, "duration_band")
        self.assertEqual(self.frontier.target_value, "short")

    def test_every_point_respects_its_local_recovered_floor(self) -> None:
        for point in self.frontier.points:
            with self.subTest(floor=point.minimum_recovered_ratio):
                self.assertGreaterEqual(
                    point.recovered_ratio + 1e-12,
                    point.minimum_recovered_ratio,
                )
                self.assertEqual(point.hard_constraint_violations, 0)

    def test_frontier_reports_target_guardrail_outcome(self) -> None:
        self.assertGreater(self.frontier.target_eligible_opportunities, 0)
        self.assertIsInstance(self.frontier.highest_passing_floor, float | None)
        self.assertTrue(
            all(point.target_guardrail_limit == 0.10 for point in self.frontier.points)
        )
        self.assertEqual(self.frontier.highest_passing_floor, 0.9)
        points = {
            point.minimum_recovered_ratio: point for point in self.frontier.points
        }
        self.assertFalse(points[0.95].target_guardrail_passed)
        self.assertTrue(points[0.9].target_guardrail_passed)
        self.assertEqual(points[0.9].optimal_recovered_minutes, 7950)
        self.assertEqual(points[0.9].recovered_minutes, 7905)
        self.assertAlmostEqual(points[0.9].recovered_ratio, 0.9943396226415094)


if __name__ == "__main__":
    unittest.main()
