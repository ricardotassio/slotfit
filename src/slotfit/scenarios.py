from datetime import datetime
from zoneinfo import ZoneInfo

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
            end=datetime(2026, 11, 4, 16, 0, tzinfo=timezone),
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
                duration_minutes=30,
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
