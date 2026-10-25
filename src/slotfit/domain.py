from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class TimeWindow:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        _require_aware(self.start, "start")
        _require_aware(self.end, "end")
        if self.end <= self.start:
            raise ValueError("end must be after start")

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)

    def contains(self, other: TimeWindow) -> bool:
        return self.start <= other.start and other.end <= self.end


@dataclass(frozen=True, slots=True)
class OpenInterval:
    interval_id: str
    provider_id: str
    room_id: str
    window: TimeWindow


@dataclass(frozen=True, slots=True)
class WaitRequest:
    request_id: str
    duration_minutes: int
    joined_order: int
    eligible_provider_ids: tuple[str, ...]
    availability_windows: tuple[TimeWindow, ...]
    minimum_notice_minutes: int
    communication_consent: bool
    required_room_id: str | None = None

    def __post_init__(self) -> None:
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be positive")
        if self.joined_order <= 0:
            raise ValueError("joined_order must be positive")
        if self.minimum_notice_minutes < 0:
            raise ValueError("minimum_notice_minutes cannot be negative")


@dataclass(frozen=True, slots=True)
class Scenario:
    scenario_id: str
    seed: int
    now: datetime
    open_intervals: tuple[OpenInterval, ...]
    wait_requests: tuple[WaitRequest, ...]
    available_room_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_aware(self.now, "now")


@dataclass(frozen=True, slots=True)
class CandidateEvaluation:
    request_id: str
    interval_id: str
    eligible: bool
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Assignment:
    request_id: str
    interval_id: str
    scheduled_window: TimeWindow


@dataclass(frozen=True, slots=True)
class CandidatePlan:
    strategy: str
    assignments: tuple[Assignment, ...]
    recovered_minutes: int
    remaining_gap_minutes: int
    evaluations: tuple[CandidateEvaluation, ...]

