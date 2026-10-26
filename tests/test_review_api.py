from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from slotfit.adapters.api.routes import get_review_repository
from slotfit.adapters.persistence.sqlite_review_repository import SQLiteReviewRepository
from slotfit.composition import app


class ReviewApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        repository = SQLiteReviewRepository(
            Path(self.temporary_directory.name) / "reviews.db"
        )
        app.dependency_overrides[get_review_repository] = lambda: repository
        self.addCleanup(app.dependency_overrides.clear)
        self.client = TestClient(app)
        self.payload = {
            "schema_version": "1.0",
            "idempotency_key": "demo-review-001",
            "scenario_id": "multi-slot-1500",
            "strategy": "fifo-eligible@0.2.0",
            "plan_checksum": "a" * 64,
            "decision": "accept",
            "rationale": "Controlled synthetic review.",
        }

    def test_create_replay_and_get_review_event(self) -> None:
        created = self.client.post("/api/v1/reviews", json=self.payload)
        replayed = self.client.post("/api/v1/reviews", json=self.payload)
        fetched = self.client.get(
            f"/api/v1/reviews/{created.json()['event']['event_id']}"
        )

        self.assertEqual(created.status_code, 201)
        self.assertTrue(created.json()["created"])
        self.assertFalse(created.json()["replayed"])
        self.assertEqual(replayed.status_code, 200)
        self.assertTrue(replayed.json()["replayed"])
        self.assertEqual(replayed.json()["event"], created.json()["event"])
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(fetched.json()["external_action"], "none")

    def test_conflicting_replay_returns_versioned_409(self) -> None:
        self.client.post("/api/v1/reviews", json=self.payload)
        conflict_payload = {**self.payload, "decision": "reject"}

        response = self.client.post("/api/v1/reviews", json=conflict_payload)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["schema_version"], "1.1")
        self.assertEqual(response.json()["error"]["code"], "idempotency_conflict")

    def test_missing_review_returns_versioned_404(self) -> None:
        response = self.client.get("/api/v1/reviews/missing-event")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "review_not_found")

    def test_invalid_command_returns_stable_validation_error(self) -> None:
        invalid_payload = {**self.payload, "plan_checksum": "not-a-checksum"}

        response = self.client.post("/api/v1/reviews", json=invalid_payload)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {
                "schema_version": "1.1",
                "error": {
                    "code": "validation_error",
                    "message": "The request does not match the API contract.",
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
