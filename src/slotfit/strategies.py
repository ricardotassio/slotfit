from __future__ import annotations

from collections.abc import Callable

from slotfit.domain import Assignment, CandidatePlan, OpenInterval, Scenario, WaitRequest
from slotfit.eligibility import evaluate_request, scheduled_window


SortKey = Callable[[WaitRequest, OpenInterval], tuple[int, ...]]


def _single_interval_plan(scenario: Scenario, strategy: str, sort_key: SortKey) -> CandidatePlan:
    if not scenario.open_intervals:
        return CandidatePlan(strategy, (), 0, 0, ())

    interval = scenario.open_intervals[0]
    evaluations = tuple(
        evaluate_request(scenario, interval, request) for request in scenario.wait_requests
    )
    eligible_ids = {evaluation.request_id for evaluation in evaluations if evaluation.eligible}
    eligible = [request for request in scenario.wait_requests if request.request_id in eligible_ids]

    if not eligible:
        return CandidatePlan(
            strategy=strategy,
            assignments=(),
            recovered_minutes=0,
            remaining_gap_minutes=interval.window.duration_minutes,
            evaluations=evaluations,
        )

    selected = min(eligible, key=lambda request: sort_key(request, interval))
    assignment = Assignment(
        request_id=selected.request_id,
        interval_id=interval.interval_id,
        scheduled_window=scheduled_window(interval, selected),
    )
    return CandidatePlan(
        strategy=strategy,
        assignments=(assignment,),
        recovered_minutes=selected.duration_minutes,
        remaining_gap_minutes=interval.window.duration_minutes - selected.duration_minutes,
        evaluations=evaluations,
    )


def fifo_plan(scenario: Scenario) -> CandidatePlan:
    return _single_interval_plan(
        scenario,
        strategy="fifo-eligible@0.1.0",
        sort_key=lambda request, _interval: (request.joined_order,),
    )


def best_fit_plan(scenario: Scenario) -> CandidatePlan:
    return _single_interval_plan(
        scenario,
        strategy="local-best-fit@0.1.0",
        sort_key=lambda request, interval: (
            interval.window.duration_minutes - request.duration_minutes,
            request.joined_order,
        ),
    )

