"""Display-only context for the clinic-day story.

Nothing here is a decision input. Strategies and the optimizer receive only a
``Scenario``; this module exists so the story can show a full day without
putting booked appointments or cancellation times into the decision data.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from slotfit.domain.model import TimeWindow


def _disjoint(left: TimeWindow, right: TimeWindow) -> bool:
    return left.end <= right.start or right.end <= left.start


@dataclass(frozen=True, slots=True)
class BookedAppointment:
    label: str
    provider_id: str
    room_id: str
    window: TimeWindow


@dataclass(frozen=True, slots=True)
class Cancellation:
    interval_id: str
    cancelled_at: datetime

    def __post_init__(self) -> None:
        if self.cancelled_at.tzinfo is None:
            raise ValueError("cancelled_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class DayContext:
    day_window: TimeWindow
    booked: tuple[BookedAppointment, ...]
    cancellations: tuple[Cancellation, ...]
    closed_room_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for index, item in enumerate(self.booked):
            if not self.day_window.contains(item.window):
                raise ValueError(f"booked appointment {item.label!r} is outside the day")
            for other in self.booked[index + 1 :]:
                if item.room_id == other.room_id and not _disjoint(item.window, other.window):
                    raise ValueError(
                        f"booked appointments {item.label!r} and {other.label!r} overlap"
                    )
        interval_ids = [item.interval_id for item in self.cancellations]
        if len(interval_ids) != len(set(interval_ids)):
            raise ValueError("cancellation interval_id values must be unique")
