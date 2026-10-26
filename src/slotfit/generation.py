from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timedelta
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping
from zoneinfo import ZoneInfo

from slotfit.domain import OpenInterval, Scenario, TimeWindow, WaitRequest


class EvaluationSplit(StrEnum):
    DEVELOPMENT = "development"
    CALIBRATION = "calibration"
    REGRESSION = "regression"
    CHALLENGE = "challenge"


@dataclass(frozen=True, slots=True)
class GenerationConfig:
    schema_version: str = "1.0"
    generator_version: str = "slotfit-synthetic-v1"
    distribution_config_id: str = "mixed-operational-v1"
    request_count: int = 8
    interval_minutes: int = 90
    challenge_property: str = "mixed-feasibility-and-operational-slices"

    def __post_init__(self) -> None:
        if self.request_count < 3:
            raise ValueError("request_count must be at least 3")
        if self.interval_minutes <= 0:
            raise ValueError("interval_minutes must be positive")


@dataclass(frozen=True, slots=True)
class RequestAuditSlice:
    request_id: str
    duration_band: str
    availability_band: str
    resource_band: str
    wait_age_band: str
    notice_band: str

    def dimension_values(self) -> tuple[tuple[str, str], ...]:
        """Return every audit dimension with its value, excluding the request id."""

        return tuple(
            (field.name, str(getattr(self, field.name)))
            for field in fields(RequestAuditSlice)
            if field.name != "request_id"
        )


@dataclass(frozen=True, slots=True)
class ScenarioManifest:
    schema_version: str
    generator_version: str
    distribution_config_id: str
    split: EvaluationSplit
    seed: int
    challenge_property: str
    decision_checksum: str
    audit_slices: tuple[RequestAuditSlice, ...]


@dataclass(frozen=True, slots=True)
class GeneratedScenario:
    scenario: Scenario
    manifest: ScenarioManifest


DEFAULT_GENERATION_CONFIG = GenerationConfig()

SPLIT_SEEDS: Mapping[EvaluationSplit, tuple[int, ...]] = MappingProxyType(
    {
        EvaluationSplit.DEVELOPMENT: (1101, 1102, 1103, 1104),
        EvaluationSplit.CALIBRATION: (2101, 2102),
        EvaluationSplit.REGRESSION: (3101, 3102, 3103, 3104),
        EvaluationSplit.CHALLENGE: (4101, 4102, 4103, 4104),
    }
)


def deterministic_int(seed: int, index: int, field_name: str, version: str) -> int:
    payload = f"{version}|{seed}|{index}|{field_name}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def deterministic_choice[T](
    values: tuple[T, ...],
    *,
    seed: int,
    index: int,
    field_name: str,
    version: str,
) -> T:
    position = deterministic_int(seed, index, field_name, version) % len(values)
    return values[position]


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"cannot serialize {type(value).__name__}")


def decision_checksum(scenario: Scenario) -> str:
    payload = json.dumps(
        asdict(scenario),
        default=_json_default,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def duration_band(duration_minutes: int) -> str:
    if duration_minutes <= 30:
        return "short"
    if duration_minutes <= 60:
        return "medium"
    return "long"


def wait_age_band(joined_order: int, request_count: int) -> str:
    if joined_order <= max(1, request_count // 3):
        return "older"
    if joined_order <= max(2, (request_count * 2) // 3):
        return "middle"
    return "recent"


def notice_band(minimum_notice_minutes: int) -> str:
    if minimum_notice_minutes <= 60:
        return "short"
    if minimum_notice_minutes <= 180:
        return "moderate"
    return "long"


def generate_scenario(
    seed: int,
    *,
    split: EvaluationSplit = EvaluationSplit.DEVELOPMENT,
    config: GenerationConfig = DEFAULT_GENERATION_CONFIG,
) -> GeneratedScenario:
    """Generate deterministic decision data and a separate audit manifest."""

    timezone = ZoneInfo("America/Toronto")
    now = datetime(2026, 11, 3, 10, 0, tzinfo=timezone)
    interval_start = datetime(2026, 11, 3, 14, 0, tzinfo=timezone)
    interval = OpenInterval(
        interval_id="OPEN-001",
        provider_id="PROVIDER-001",
        room_id="ROOM-A",
        window=TimeWindow(
            start=interval_start,
            end=interval_start + timedelta(minutes=config.interval_minutes),
        ),
    )

    order = sorted(
        range(config.request_count),
        key=lambda index: deterministic_int(
            seed,
            index,
            "joined-order",
            config.generator_version,
        ),
    )
    joined_orders = {index: position + 1 for position, index in enumerate(order)}

    requests: list[WaitRequest] = []
    audit_slices: list[RequestAuditSlice] = []

    for index in range(config.request_count):
        request_id = f"WR-{index + 1:03d}"
        duration_options = (30, 45, 60, 75) if index < 2 else (30, 45, 60, 75, 120)
        duration = deterministic_choice(
            duration_options,
            seed=seed,
            index=index,
            field_name="duration",
            version=config.generator_version,
        )

        if index < 2:
            provider_ids = ("PROVIDER-001",)
            required_room_id = None if index == 0 else "ROOM-A"
            minimum_notice = 60
            has_consent = True
            availability_profile = "broad"
        else:
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
                ("broad", "broad", "narrow", "offset"),
                seed=seed,
                index=index,
                field_name="availability",
                version=config.generator_version,
            )

        if availability_profile == "broad":
            availability = (interval.window,)
        elif availability_profile == "narrow":
            availability = (
                TimeWindow(
                    start=interval.window.start,
                    end=interval.window.start + timedelta(minutes=duration),
                ),
            )
        else:
            availability = (
                TimeWindow(
                    start=interval.window.start + timedelta(minutes=15),
                    end=interval.window.end + timedelta(minutes=15),
                ),
            )

        joined_order = joined_orders[index]
        request = WaitRequest(
            request_id=request_id,
            duration_minutes=duration,
            joined_order=joined_order,
            eligible_provider_ids=provider_ids,
            availability_windows=availability,
            minimum_notice_minutes=minimum_notice,
            communication_consent=has_consent,
            required_room_id=required_room_id,
        )
        requests.append(request)
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
        scenario_id=f"{split.value}-{seed}",
        seed=seed,
        now=now,
        open_intervals=(interval,),
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
