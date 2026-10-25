from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from types import MappingProxyType
from typing import Mapping
from zoneinfo import ZoneInfo

from slotfit.domain import OpenInterval, Scenario, TimeWindow, WaitRequest
from slotfit.generation import (
    EvaluationSplit,
    GeneratedScenario,
    RequestAuditSlice,
    ScenarioManifest,
    decision_checksum,
    deterministic_choice,
    deterministic_int,
    duration_band,
    notice_band,
    wait_age_band,
)


@dataclass(frozen=True, slots=True)
class MultiSlotGenerationConfig:
    schema_version: str = "1.0"
    generator_version: str = "slotfit-multislot-v1"
    distribution_config_id: str = "multislot-operational-v1"
    request_count: int = 10
    interval_count: int = 3
    challenge_property: str = "global-assignment-conflict-with-operational-variation"

    def __post_init__(self) -> None:
        if self.request_count < 4:
            raise ValueError("request_count must be at least 4")
        if self.interval_count != 3:
            raise ValueError("multislot-operational-v1 requires exactly 3 intervals")


DEFAULT_MULTI_SLOT_CONFIG = MultiSlotGenerationConfig()

MULTI_SLOT_SEEDS: Mapping[EvaluationSplit, tuple[int, ...]] = MappingProxyType(
    {
        EvaluationSplit.DEVELOPMENT: tuple(range(1201, 1241)),
        EvaluationSplit.CALIBRATION: tuple(range(2201, 2241)),
        EvaluationSplit.REGRESSION: tuple(range(3201, 3221)),
        EvaluationSplit.CHALLENGE: tuple(range(4201, 4211)),
    }
)


def _build_intervals(
    seed: int,
    config: MultiSlotGenerationConfig,
) -> tuple[OpenInterval, ...]:
    timezone = ZoneInfo("America/Toronto")
    first_start = datetime(2026, 11, 5, 14, 0, tzinfo=timezone)
    conflict_duration = deterministic_choice(
        (45, 60),
        seed=seed,
        index=0,
        field_name="conflict-duration",
        version=config.generator_version,
    )
    third_duration = deterministic_choice(
        (30, 45, 60),
        seed=seed,
        index=2,
        field_name="interval-duration",
        version=config.generator_version,
    )
    durations = (conflict_duration, conflict_duration, third_duration)
    starts = (
        first_start,
        first_start + timedelta(minutes=90),
        first_start + timedelta(minutes=180),
    )
    return tuple(
        OpenInterval(
            interval_id=f"OPEN-{position + 1:03d}",
            provider_id="PROVIDER-001",
            room_id="ROOM-A",
            window=TimeWindow(
                start=start,
                end=start + timedelta(minutes=durations[position]),
            ),
        )
        for position, start in enumerate(starts)
    )


def _availability(
    profile: str,
    intervals: tuple[OpenInterval, ...],
    *,
    seed: int,
    index: int,
    version: str,
) -> tuple[TimeWindow, ...]:
    if profile == "broad":
        return tuple(interval.window for interval in intervals)
    if profile == "first-only":
        return (intervals[0].window,)
    if profile == "later":
        return tuple(interval.window for interval in intervals[1:])
    interval = deterministic_choice(
        intervals,
        seed=seed,
        index=index,
        field_name="single-interval",
        version=version,
    )
    return (interval.window,)


def generate_multi_slot_scenario(
    seed: int,
    *,
    split: EvaluationSplit = EvaluationSplit.DEVELOPMENT,
    config: MultiSlotGenerationConfig = DEFAULT_MULTI_SLOT_CONFIG,
) -> GeneratedScenario:
    """Generate a deterministic multi-slot scenario with audit-only slices."""

    intervals = _build_intervals(seed, config)
    conflict_duration = intervals[0].window.duration_minutes
    remaining_indices = tuple(range(2, config.request_count))
    shuffled_indices = tuple(
        sorted(
            remaining_indices,
            key=lambda index: deterministic_int(
                seed,
                index,
                "joined-order",
                config.generator_version,
            ),
        )
    )
    joined_orders = {0: 1, 1: 2}
    joined_orders.update(
        {index: position for position, index in enumerate(shuffled_indices, start=3)}
    )

    requests: list[WaitRequest] = []
    audit_slices: list[RequestAuditSlice] = []
    for index in range(config.request_count):
        request_id = f"MS-WR-{index + 1:03d}"
        if index == 0:
            duration = conflict_duration
            provider_ids = ("PROVIDER-001",)
            required_room_id = None
            minimum_notice = 60
            has_consent = True
            availability_profile = "broad"
            availability = tuple(interval.window for interval in intervals[:2])
        elif index == 1:
            duration = conflict_duration
            provider_ids = ("PROVIDER-001",)
            required_room_id = None
            minimum_notice = 60
            has_consent = True
            availability_profile = "first-only"
            availability = (intervals[0].window,)
        else:
            duration = deterministic_choice(
                (30, 45, 60, 75),
                seed=seed,
                index=index,
                field_name="duration",
                version=config.generator_version,
            )
            provider_ids = deterministic_choice(
                (
                    ("PROVIDER-001",),
                    ("PROVIDER-001",),
                    ("PROVIDER-001",),
                    ("PROVIDER-002",),
                ),
                seed=seed,
                index=index,
                field_name="provider",
                version=config.generator_version,
            )
            required_room_id = deterministic_choice(
                (None, None, "ROOM-A", "ROOM-B"),
                seed=seed,
                index=index,
                field_name="room",
                version=config.generator_version,
            )
            minimum_notice = deterministic_choice(
                (30, 60, 180, 300),
                seed=seed,
                index=index,
                field_name="notice",
                version=config.generator_version,
            )
            has_consent = bool(
                deterministic_choice(
                    (1, 1, 1, 1, 0),
                    seed=seed,
                    index=index,
                    field_name="consent",
                    version=config.generator_version,
                )
            )
            availability_profile = deterministic_choice(
                ("broad", "broad", "first-only", "later", "single"),
                seed=seed,
                index=index,
                field_name="availability",
                version=config.generator_version,
            )
            availability = _availability(
                availability_profile,
                intervals,
                seed=seed,
                index=index,
                version=config.generator_version,
            )

        joined_order = joined_orders[index]
        requests.append(
            WaitRequest(
                request_id=request_id,
                duration_minutes=duration,
                joined_order=joined_order,
                eligible_provider_ids=provider_ids,
                availability_windows=availability,
                minimum_notice_minutes=minimum_notice,
                communication_consent=has_consent,
                required_room_id=required_room_id,
            )
        )
        audit_slices.append(
            RequestAuditSlice(
                request_id=request_id,
                duration_band=duration_band(duration),
                availability_band=availability_profile,
                resource_band="scarce" if required_room_id == "ROOM-B" else "common",
                wait_age_band=wait_age_band(joined_order, config.request_count),
                notice_band=notice_band(minimum_notice),
            )
        )

    scenario = Scenario(
        scenario_id=f"multislot-{split.value}-{seed}",
        seed=seed,
        now=datetime(2026, 11, 5, 10, 0, tzinfo=ZoneInfo("America/Toronto")),
        open_intervals=intervals,
        wait_requests=tuple(requests),
        available_room_ids=("ROOM-A",),
    )
    manifest = ScenarioManifest(
        schema_version=config.schema_version,
        generator_version=config.generator_version,
        distribution_config_id=config.distribution_config_id,
        split=split,
        seed=seed,
        challenge_property=config.challenge_property,
        decision_checksum=decision_checksum(scenario),
        audit_slices=tuple(audit_slices),
    )
    return GeneratedScenario(scenario=scenario, manifest=manifest)
