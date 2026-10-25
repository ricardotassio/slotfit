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

