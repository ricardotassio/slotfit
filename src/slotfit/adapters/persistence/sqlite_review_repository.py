from __future__ import annotations

import re
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal


ReviewDecision = Literal["accept", "reject", "request_alternative"]


class IdempotencyConflict(Exception):
    """The key already belongs to a different semantic command."""


@dataclass(frozen=True, slots=True)
class ReviewCommand:
    idempotency_key: str
    scenario_id: str
    strategy: str
    plan_checksum: str
    decision: ReviewDecision
    rationale: str | None = None

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[!-~]{1,64}", self.idempotency_key):
            raise ValueError("idempotency_key must contain 1..64 visible ASCII characters")
        for field_name, value in (
            ("scenario_id", self.scenario_id),
            ("strategy", self.strategy),
        ):
            if not value or len(value) > 128:
                raise ValueError(f"{field_name} must contain 1..128 characters")
        if not re.fullmatch(r"[0-9a-f]{64}", self.plan_checksum):
            raise ValueError("plan_checksum must be a lowercase SHA-256 value")
        if self.decision not in {"accept", "reject", "request_alternative"}:
            raise ValueError("decision is not supported")
        if self.rationale is not None and len(self.rationale) > 500:
            raise ValueError("rationale cannot exceed 500 characters")


@dataclass(frozen=True, slots=True)
class ReviewEvent:
    event_id: str
    created_at: datetime
    idempotency_key: str
    scenario_id: str
    strategy: str
    plan_checksum: str
    decision: ReviewDecision
    rationale: str | None
    external_action: Literal["none"] = "none"


@dataclass(frozen=True, slots=True)
class RecordReviewResult:
    event: ReviewEvent
    created: bool
    replayed: bool


_MIGRATION = """
CREATE TABLE IF NOT EXISTS review_events (
    event_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    scenario_id TEXT NOT NULL,
    strategy TEXT NOT NULL,
    plan_checksum TEXT NOT NULL,
    decision TEXT NOT NULL CHECK (
        decision IN ('accept', 'reject', 'request_alternative')
    ),
    rationale TEXT,
    external_action TEXT NOT NULL DEFAULT 'none' CHECK (external_action = 'none')
);

CREATE TRIGGER IF NOT EXISTS review_events_no_update
BEFORE UPDATE ON review_events
BEGIN
    SELECT RAISE(ABORT, 'review_events are append-only');
END;

CREATE TRIGGER IF NOT EXISTS review_events_no_delete
BEFORE DELETE ON review_events
BEGIN
    SELECT RAISE(ABORT, 'review_events are append-only');
END;
"""


class SQLiteReviewRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path, timeout=5.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(_MIGRATION)

    def record(self, command: ReviewCommand) -> RecordReviewResult:
        self.initialize()
        event = ReviewEvent(
            event_id=str(uuid.uuid4()),
            created_at=datetime.now(UTC),
            idempotency_key=command.idempotency_key,
            scenario_id=command.scenario_id,
            strategy=command.strategy,
            plan_checksum=command.plan_checksum,
            decision=command.decision,
            rationale=command.rationale,
        )
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                INSERT INTO review_events (
                    event_id, created_at, idempotency_key, scenario_id, strategy,
                    plan_checksum, decision, rationale, external_action
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.created_at.isoformat(),
                    event.idempotency_key,
                    event.scenario_id,
                    event.strategy,
                    event.plan_checksum,
                    event.decision,
                    event.rationale,
                    event.external_action,
                ),
            )
            connection.commit()
            return RecordReviewResult(event=event, created=True, replayed=False)
        except sqlite3.IntegrityError:
            connection.rollback()
            existing = self._get_by_idempotency_key(connection, command.idempotency_key)
            if existing is None:
                raise
            if self._same_command(existing, command):
                return RecordReviewResult(event=existing, created=False, replayed=True)
            raise IdempotencyConflict(command.idempotency_key) from None
        finally:
            connection.close()

    def get(self, event_id: str) -> ReviewEvent | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM review_events WHERE event_id = ?",
                (event_id,),
            ).fetchone()
        return self._event(row) if row is not None else None

    def count(self) -> int:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) AS count FROM review_events").fetchone()
        assert row is not None
        return int(row["count"])

    @staticmethod
    def _get_by_idempotency_key(
        connection: sqlite3.Connection,
        idempotency_key: str,
    ) -> ReviewEvent | None:
        row = connection.execute(
            "SELECT * FROM review_events WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
        return SQLiteReviewRepository._event(row) if row is not None else None

    @staticmethod
    def _event(row: sqlite3.Row) -> ReviewEvent:
        return ReviewEvent(
            event_id=str(row["event_id"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            idempotency_key=str(row["idempotency_key"]),
            scenario_id=str(row["scenario_id"]),
            strategy=str(row["strategy"]),
            plan_checksum=str(row["plan_checksum"]),
            decision=str(row["decision"]),  # type: ignore[arg-type]
            rationale=(str(row["rationale"]) if row["rationale"] is not None else None),
            external_action="none",
        )

    @staticmethod
    def _same_command(event: ReviewEvent, command: ReviewCommand) -> bool:
        return (
            event.idempotency_key,
            event.scenario_id,
            event.strategy,
            event.plan_checksum,
            event.decision,
            event.rationale,
        ) == (
            command.idempotency_key,
            command.scenario_id,
            command.strategy,
            command.plan_checksum,
            command.decision,
            command.rationale,
        )

