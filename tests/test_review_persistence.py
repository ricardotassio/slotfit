from __future__ import annotations

import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from slotfit.persistence import (
    IdempotencyConflict,
    ReviewCommand,
    SQLiteReviewRepository,
)


def _command(*, decision: str = "accept") -> ReviewCommand:
    return ReviewCommand(
        idempotency_key="demo-review-001",
        scenario_id="multi-slot-1500",
        strategy="fifo-eligible@0.2.0",
        plan_checksum="a" * 64,
        decision=decision,
        rationale="Controlled synthetic review.",
    )


class ReviewPersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.database_path = Path(self.temporary_directory.name) / "reviews.db"
        self.repository = SQLiteReviewRepository(self.database_path)

    def test_schema_migration_is_repeatable(self) -> None:
        self.repository.initialize()
        self.repository.initialize()

        with sqlite3.connect(self.database_path) as connection:
            tables = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        self.assertIn(("review_events",), tables)

    def test_first_write_creates_an_immutable_event(self) -> None:
        result = self.repository.record(_command())

        self.assertTrue(result.created)
        self.assertFalse(result.replayed)
        self.assertEqual(result.event.external_action, "none")
        self.assertEqual(self.repository.get(result.event.event_id), result.event)

    def test_equivalent_replay_returns_the_original_event(self) -> None:
        first = self.repository.record(_command())
        second = self.repository.record(_command())

        self.assertEqual(second.event, first.event)
        self.assertFalse(second.created)
        self.assertTrue(second.replayed)
        self.assertEqual(self.repository.count(), 1)

    def test_conflicting_replay_fails_without_adding_a_row(self) -> None:
        self.repository.record(_command())

        with self.assertRaises(IdempotencyConflict):
            self.repository.record(_command(decision="reject"))

        self.assertEqual(self.repository.count(), 1)

    def test_database_rejects_update_and_delete(self) -> None:
        event = self.repository.record(_command()).event

        with sqlite3.connect(self.database_path) as connection:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "UPDATE review_events SET decision = 'reject' WHERE event_id = ?",
                    (event.event_id,),
                )
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "DELETE FROM review_events WHERE event_id = ?",
                    (event.event_id,),
                )

    def test_two_connections_cannot_create_duplicate_idempotency_rows(self) -> None:
        self.repository.initialize()
        repositories = (
            SQLiteReviewRepository(self.database_path),
            SQLiteReviewRepository(self.database_path),
        )

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda repo: repo.record(_command()), repositories))

        self.assertEqual(sum(result.created for result in results), 1)
        self.assertEqual(sum(result.replayed for result in results), 1)
        self.assertEqual(results[0].event.event_id, results[1].event.event_id)
        self.assertEqual(self.repository.count(), 1)


if __name__ == "__main__":
    unittest.main()

