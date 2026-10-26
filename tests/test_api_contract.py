from __future__ import annotations

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from slotfit.api import app
from slotfit.api_service import DEMO_BUILDERS


class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_health_is_versioned_and_read_only(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "application_version": "0.1.0", "schema_version": "1.1"},
        )

    def test_single_opening_demo_exposes_two_explainable_plans(self) -> None:
        response = self.client.get("/api/v1/demos/single-opening")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["synthetic"])
        self.assertEqual(payload["automatic_action"], "none")
        self.assertEqual(len(payload["plans"]), 2)
        self.assertEqual(
            [plan["strategy"] for plan in payload["plans"]],
            ["fifo-eligible@0.2.0", "local-best-fit@0.2.0"],
        )
        self.assertTrue(
            all(
                evaluation["reason_codes"] is not None
                for plan in payload["plans"]
                for evaluation in plan["evaluations"]
            )
        )

    def test_global_conflict_demo_exposes_optimizer_evidence_and_disclosure(self) -> None:
        response = self.client.get("/api/v1/demos/global-conflict")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["plans"]), 3)
        self.assertEqual(payload["optimizer_evidence"]["status"], "OPTIMAL")
        self.assertEqual(
            [phase["status"] for phase in payload["optimizer_evidence"]["phases"]],
            ["OPTIMAL", "OPTIMAL", "OPTIMAL"],
        )
        self.assertFalse(payload["optimizer_evidence"]["research_candidate_accepted"])
        self.assertIn("controlled counterexample", payload["disclosure"].lower())
        self.assertEqual(
            payload,
            self.client.get("/api/v1/demos/global-conflict").json(),
        )

    def test_clinic_day_demo_adds_display_context_and_explanations(self) -> None:
        response = self.client.get("/api/v1/demos/clinic-day")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["scenario_id"], "clinic-day-story-1600")
        self.assertEqual(len(payload["plans"]), 3)
        self.assertEqual(
            [plan["recovered_minutes"] for plan in payload["plans"]], [60, 60, 120]
        )
        self.assertEqual(payload["optimizer_evidence"]["status"], "OPTIMAL")
        context = payload["day_context"]
        self.assertEqual(len(context["booked"]), 7)
        self.assertEqual(context["closed_room_ids"], ["ROOM-B"])
        self.assertEqual(len(context["cancellations"]), 2)
        for plan in payload["plans"]:
            for evaluation in plan["evaluations"]:
                self.assertTrue(evaluation["explanations"])
                self.assertTrue(all(text.endswith(".") for text in evaluation["explanations"]))
        self.assertEqual(payload, self.client.get("/api/v1/demos/clinic-day").json())

    def test_other_demos_have_no_display_context(self) -> None:
        for demo_id in ("single-opening", "global-conflict"):
            with self.subTest(demo_id=demo_id):
                payload = self.client.get(f"/api/v1/demos/{demo_id}").json()
                self.assertIsNone(payload["day_context"])

    def test_demo_catalogue_is_exactly_the_three_synthetic_demos(self) -> None:
        self.assertEqual(
            set(DEMO_BUILDERS),
            {"single-opening", "global-conflict", "clinic-day"},
        )
        for demo_id in DEMO_BUILDERS:
            self.assertEqual(self.client.get(f"/api/v1/demos/{demo_id}").status_code, 200)

    def test_unknown_demo_uses_stable_versioned_error(self) -> None:
        self.assertNotIn("not-a-demo", DEMO_BUILDERS)
        response = self.client.get("/api/v1/demos/not-a-demo")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "schema_version": "1.1",
                "error": {
                    "code": "demo_not_found",
                    "message": "The requested synthetic demo does not exist.",
                },
            },
        )

    def test_research_decision_reports_terminal_no_go(self) -> None:
        response = self.client.get("/api/v1/research/development-decision")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertFalse(payload["candidate_accepted"])
        self.assertFalse(payload["calibration_open"])
        self.assertFalse(payload["final_frozen_set_exists"])
        self.assertEqual(len(payload["candidates"]), 4)
        self.assertTrue(
            all(candidate["decision"] == "reject" for candidate in payload["candidates"])
        )
        self.assertEqual(payload["guardrail"]["limit_percentage_points"], 10.0)

    def test_openapi_exposes_only_declared_operations(self) -> None:
        schema = self.client.get("/openapi.json").json()

        self.assertEqual(
            {path: set(item) for path, item in schema["paths"].items()},
            {
                "/health": {"get"},
                "/api/v1/demos/{demo_id}": {"get"},
                "/api/v1/research/development-decision": {"get"},
                "/api/v1/reviews": {"post"},
                "/api/v1/reviews/{event_id}": {"get"},
            },
        )

    def test_domain_and_strategies_do_not_import_transport_frameworks(self) -> None:
        package_root = Path(__file__).parents[1] / "src" / "slotfit"

        for filename in ("domain/model.py", "domain/eligibility.py", "strategies.py"):
            source = (package_root / filename).read_text(encoding="utf-8")
            self.assertNotIn("fastapi", source)
            self.assertNotIn("pydantic", source)


if __name__ == "__main__":
    unittest.main()
