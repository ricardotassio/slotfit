from datetime import datetime
from zoneinfo import ZoneInfo

from slotfit.day_context import BookedAppointment, Cancellation, DayContext
from slotfit.domain import OpenInterval, Scenario, TimeWindow, WaitRequest


def demo_scenario(seed: int = 1400) -> Scenario:
    timezone = ZoneInfo("America/Toronto")
    interval = OpenInterval(
        interval_id="OPEN-001",
        provider_id="PROVIDER-001",
        room_id="ROOM-A",
        window=TimeWindow(
            start=datetime(2026, 11, 3, 14, 0, tzinfo=timezone),
            end=datetime(2026, 11, 3, 15, 30, tzinfo=timezone),
        ),
    )
    available = (TimeWindow(interval.window.start, interval.window.end),)

    return Scenario(
        scenario_id=f"demo-{seed}",
        seed=seed,
        now=datetime(2026, 11, 3, 10, 0, tzinfo=timezone),
        open_intervals=(interval,),
        wait_requests=(
            WaitRequest(
                request_id="WR-001",
                duration_minutes=30,
                joined_order=1,
                eligible_provider_ids=("PROVIDER-001",),
                availability_windows=available,
                minimum_notice_minutes=60,
                communication_consent=True,
            ),
            WaitRequest(
                request_id="WR-002",
                duration_minutes=75,
                joined_order=3,
                eligible_provider_ids=("PROVIDER-001",),
                availability_windows=available,
                minimum_notice_minutes=60,
                communication_consent=True,
            ),
            WaitRequest(
                request_id="WR-003",
                duration_minutes=60,
                joined_order=2,
                eligible_provider_ids=("PROVIDER-001",),
                availability_windows=available,
                minimum_notice_minutes=60,
                communication_consent=True,
                required_room_id="ROOM-B",
            ),
        ),
        available_room_ids=("ROOM-A",),
    )


def multi_slot_counterexample(seed: int = 1500) -> Scenario:
    """Expose the global assignment trade-off without real clinic data."""

    timezone = ZoneInfo("America/Toronto")
    open_a = OpenInterval(
        interval_id="OPEN-A",
        provider_id="PROVIDER-001",
        room_id="ROOM-A",
        window=TimeWindow(
            start=datetime(2026, 11, 4, 14, 0, tzinfo=timezone),
            end=datetime(2026, 11, 4, 15, 0, tzinfo=timezone),
        ),
    )
    open_b = OpenInterval(
        interval_id="OPEN-B",
        provider_id="PROVIDER-001",
        room_id="ROOM-A",
        window=TimeWindow(
            start=datetime(2026, 11, 4, 15, 30, tzinfo=timezone),
            end=datetime(2026, 11, 4, 16, 30, tzinfo=timezone),
        ),
    )
    return Scenario(
        scenario_id=f"multi-slot-counterexample-{seed}",
        seed=seed,
        now=datetime(2026, 11, 4, 10, 0, tzinfo=timezone),
        open_intervals=(open_a, open_b),
        wait_requests=(
            WaitRequest(
                request_id="WR-FLEXIBLE",
                duration_minutes=60,
                joined_order=1,
                eligible_provider_ids=("PROVIDER-001",),
                availability_windows=(open_a.window, open_b.window),
                minimum_notice_minutes=60,
                communication_consent=True,
            ),
            WaitRequest(
                request_id="WR-CONSTRAINED",
                duration_minutes=60,
                joined_order=2,
                eligible_provider_ids=("PROVIDER-001",),
                availability_windows=(open_a.window,),
                minimum_notice_minutes=60,
                communication_consent=True,
            ),
        ),
        available_room_ids=("ROOM-A",),
    )


def clinic_day_story(seed: int = 1600) -> tuple[Scenario, DayContext]:
    """Story superset of the global-conflict fixture plus display-only context.

    The decision scenario reuses the two openings and two requests of
    ``multi_slot_counterexample`` and adds a request that needs the closed Room B,
    so every reason code shown in the story comes from the engine. Seed 1600 is
    hand-built and belongs to no evaluation registry.
    """

    timezone = ZoneInfo("America/Toronto")
    base = multi_slot_counterexample(seed=1500)
    day = datetime(2026, 11, 4, tzinfo=timezone)

    def at(hour: int, minute: int = 0) -> datetime:
        return day.replace(hour=hour, minute=minute)

    room_b_request = WaitRequest(
        request_id="WR-ROOM-B",
        duration_minutes=45,
        joined_order=3,
        eligible_provider_ids=("PROVIDER-001",),
        availability_windows=tuple(interval.window for interval in base.open_intervals),
        minimum_notice_minutes=60,
        communication_consent=True,
        required_room_id="ROOM-B",
    )
    scenario = Scenario(
        scenario_id=f"clinic-day-story-{seed}",
        seed=seed,
        now=at(10, 15),
        open_intervals=base.open_intervals,
        wait_requests=(*base.wait_requests, room_b_request),
        available_room_ids=("ROOM-A",),
    )

    booked_blocks = (
        ("Booked", 8, 0, 9, 0),
        ("Booked", 9, 0, 9, 45),
        ("Booked", 10, 0, 11, 0),
        ("Booked", 11, 0, 12, 0),
        ("Booked", 13, 0, 14, 0),
        ("Booked", 15, 0, 15, 30),
        ("Booked", 16, 30, 17, 0),
    )
    context = DayContext(
        day_window=TimeWindow(start=at(8), end=at(17)),
        booked=tuple(
            BookedAppointment(
                label=label,
                provider_id="PROVIDER-001",
                room_id="ROOM-A",
                window=TimeWindow(start=at(start_hour, start_minute), end=at(end_hour, end_minute)),
            )
            for label, start_hour, start_minute, end_hour, end_minute in booked_blocks
        ),
        cancellations=(
            Cancellation(interval_id="OPEN-A", cancelled_at=at(9, 40)),
            Cancellation(interval_id="OPEN-B", cancelled_at=at(10, 12)),
        ),
        closed_room_ids=("ROOM-B",),
    )
    return scenario, context
