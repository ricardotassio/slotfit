from __future__ import annotations

from collections.abc import Callable

from slotfit.domain.eligibility import evaluate_request, scheduled_window
from slotfit.domain.model import Assignment, CandidatePlan, OpenInterval, Scenario, WaitRequest

SortKey = Callable[[WaitRequest, OpenInterval], tuple[int, ...]]


def _greedy_plan(scenario: Scenario, strategy: str, sort_key: SortKey) -> CandidatePlan:
    intervals = tuple(
        sorted(
            scenario.open_intervals,
            key=lambda item: (
                item.window.start,
                item.window.end,
                item.window.duration_minutes,
            ),
        )
    )
    evaluations = tuple(
        evaluate_request(scenario, interval, request)
        for interval in intervals
        for request in scenario.wait_requests
    )
    eligible_keys = {
        (evaluation.request_id, evaluation.interval_id)
        for evaluation in evaluations
        if evaluation.eligible
    }
    assigned_request_ids: set[str] = set()
    assignments: list[Assignment] = []

    for interval in intervals:
        eligible = [
            request
            for request in scenario.wait_requests
            if request.request_id not in assigned_request_ids
            and (request.request_id, interval.interval_id) in eligible_keys
        ]
        if not eligible:
            continue

        selected = min(eligible, key=lambda request: sort_key(request, interval))
        assignments.append(
            Assignment(
                request_id=selected.request_id,
                interval_id=interval.interval_id,
                scheduled_window=scheduled_window(interval, selected),
            )
        )
        assigned_request_ids.add(selected.request_id)

    recovered_minutes = sum(
        assignment.scheduled_window.duration_minutes for assignment in assignments
    )
    open_minutes = sum(interval.window.duration_minutes for interval in intervals)
    return CandidatePlan(
        strategy=strategy,
        assignments=tuple(assignments),
        recovered_minutes=recovered_minutes,
        remaining_gap_minutes=open_minutes - recovered_minutes,
        evaluations=evaluations,
    )


def fifo_plan(scenario: Scenario) -> CandidatePlan:
    return _greedy_plan(
        scenario,
        strategy="fifo-eligible@0.2.0",
        sort_key=lambda request, _interval: (request.joined_order,),
    )


def best_fit_plan(scenario: Scenario) -> CandidatePlan:
    return _greedy_plan(
        scenario,
        strategy="local-best-fit@0.2.0",
        sort_key=lambda request, interval: (
            interval.window.duration_minutes - request.duration_minutes,
            request.joined_order,
        ),
    )
