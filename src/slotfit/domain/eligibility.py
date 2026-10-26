from __future__ import annotations

from datetime import timedelta

from slotfit.domain.model import (
    CandidateEvaluation,
    OpenInterval,
    Scenario,
    TimeWindow,
    WaitRequest,
)


def scheduled_window(interval: OpenInterval, request: WaitRequest) -> TimeWindow:
    return TimeWindow(
        start=interval.window.start,
        end=interval.window.start + timedelta(minutes=request.duration_minutes),
    )


def evaluate_request(
    scenario: Scenario,
    interval: OpenInterval,
    request: WaitRequest,
) -> CandidateEvaluation:
    reasons: list[str] = []

    if not request.communication_consent:
        reasons.append("NO_COMMUNICATION_CONSENT")
    if interval.provider_id not in request.eligible_provider_ids:
        reasons.append("PROVIDER_NOT_ELIGIBLE")
    if request.required_room_id and request.required_room_id not in scenario.available_room_ids:
        reasons.append("REQUIRED_ROOM_UNAVAILABLE")
    if request.duration_minutes > interval.window.duration_minutes:
        reasons.append("DURATION_EXCEEDS_INTERVAL")

    notice = interval.window.start - scenario.now
    if notice < timedelta(minutes=request.minimum_notice_minutes):
        reasons.append("INSUFFICIENT_NOTICE")

    if request.duration_minutes <= interval.window.duration_minutes:
        proposed = scheduled_window(interval, request)
        if not any(window.contains(proposed) for window in request.availability_windows):
            reasons.append("REQUEST_NOT_AVAILABLE")

    return CandidateEvaluation(
        request_id=request.request_id,
        interval_id=interval.interval_id,
        eligible=not reasons,
        reason_codes=tuple(reasons),
    )

