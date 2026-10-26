from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product

from slotfit.domain.model import Assignment, CandidatePlan, Scenario
from slotfit.domain.eligibility import evaluate_request, scheduled_window
from slotfit.generation import EvaluationSplit
from slotfit.multi_generation import MULTI_SLOT_SEEDS, generate_multi_slot_scenario
from slotfit.optimizer import optimize_plan_with_exposure_debt
from slotfit.thresholds import SUPPORT_THRESHOLD


@dataclass(frozen=True, slots=True)
class SliceAlternativeDiagnostic:
    dimension: str
    value: str
    eligible_opportunities: int
    actual_exposures: int
    rounds_with_improving_alternative: int
    additional_exposure_capacity: int
    supported: bool


@dataclass(frozen=True, slots=True)
class AlternativeDiagnosticReport:
    schema_version: str
    split: EvaluationSplit
    seed_count: int
    requested_rounds_per_seed: int
    round_count: int
    rounds_with_multiple_primary_plans: int
    non_primary_optimal_v2_rounds: int
    slices: tuple[SliceAlternativeDiagnostic, ...]


@dataclass(slots=True)
class _MutableSliceDiagnostic:
    eligible_opportunities: int = 0
    actual_exposures: int = 0
    rounds_with_improving_alternative: int = 0
    additional_exposure_capacity: int = 0


def enumerate_feasible_plans(
    scenario: Scenario,
    *,
    max_combinations: int = 100_000,
) -> tuple[CandidatePlan, ...]:
    """Enumerate every feasible plan for a bounded synthetic scenario.

    This diagnostic consumes decision data only. Its bounded exhaustive search is
    intentionally limited to small synthetic POC scenarios.
    """

    if max_combinations <= 0:
        raise ValueError("max_combinations must be positive")

    intervals = tuple(
        sorted(scenario.open_intervals, key=lambda item: (item.window.start, item.window.end))
    )
    requests = tuple(sorted(scenario.wait_requests, key=lambda item: item.joined_order))
    request_by_id = {request.request_id: request for request in requests}
    evaluations = tuple(
        evaluate_request(scenario, interval, request)
        for interval in intervals
        for request in requests
    )
    eligible_by_interval = {
        interval.interval_id: tuple(
            request.request_id
            for request in requests
            if any(
                evaluation.interval_id == interval.interval_id
                and evaluation.request_id == request.request_id
                and evaluation.eligible
                for evaluation in evaluations
            )
        )
        for interval in intervals
    }
    option_sets = tuple(
        (None, *eligible_by_interval[interval.interval_id]) for interval in intervals
    )
    combination_count = 1
    for options in option_sets:
        combination_count *= len(options)
    if combination_count > max_combinations:
        raise ValueError(
            f"diagnostic combination limit exceeded: {combination_count} > {max_combinations}"
        )

    feasible_choices: list[tuple[str | None, ...]] = []
    for choices in product(*option_sets):
        selected_ids = tuple(request_id for request_id in choices if request_id is not None)
        if len(selected_ids) != len(set(selected_ids)):
            continue
        feasible_choices.append(choices)

    open_minutes = sum(interval.window.duration_minutes for interval in intervals)
    return tuple(
        CandidatePlan(
            strategy="primary-optimal-enumerator@0.1.0",
            assignments=tuple(
                Assignment(
                    request_id=request_id,
                    interval_id=interval.interval_id,
                    scheduled_window=scheduled_window(
                        interval,
                        request_by_id[request_id],
                    ),
                )
                for interval, request_id in zip(intervals, choices, strict=True)
                if request_id is not None
            ),
            recovered_minutes=sum(
                request_by_id[request_id].duration_minutes
                for request_id in choices
                if request_id is not None
            ),
            remaining_gap_minutes=(
                open_minutes
                - sum(
                    request_by_id[request_id].duration_minutes
                    for request_id in choices
                    if request_id is not None
                )
            ),
            evaluations=evaluations,
        )
        for choices in feasible_choices
    )


def enumerate_primary_optimal_plans(
    scenario: Scenario,
    *,
    max_combinations: int = 100_000,
) -> tuple[CandidatePlan, ...]:
    """Enumerate plans tied on recovered minutes and requests served."""

    plans = enumerate_feasible_plans(scenario, max_combinations=max_combinations)
    best_score = max(
        (plan.recovered_minutes, len(plan.assignments)) for plan in plans
    )
    return tuple(
        plan
        for plan in plans
        if (plan.recovered_minutes, len(plan.assignments)) == best_score
    )


def diagnose_development_alternatives(
    *,
    rounds: int = 5,
) -> AlternativeDiagnosticReport:
    if rounds <= 0:
        raise ValueError("rounds must be positive")

    slice_totals: dict[tuple[str, str], _MutableSliceDiagnostic] = {}
    round_count = 0
    multiple_plan_rounds = 0
    non_primary_optimal_v2_rounds = 0

    for seed in MULTI_SLOT_SEEDS[EvaluationSplit.DEVELOPMENT]:
        generated = generate_multi_slot_scenario(
            seed,
            split=EvaluationSplit.DEVELOPMENT,
        )
        active_request_ids = {
            request.request_id for request in generated.scenario.wait_requests
        }
        debt = {request_id: 0 for request_id in active_request_ids}
        audit_by_request = {
            audit_slice.request_id: audit_slice
            for audit_slice in generated.manifest.audit_slices
        }

        for round_number in range(1, rounds + 1):
            if not active_request_ids:
                break
            scenario = replace(
                generated.scenario,
                scenario_id=(
                    f"{generated.scenario.scenario_id}-diagnostic-round-{round_number:02d}"
                ),
                wait_requests=tuple(
                    request
                    for request in generated.scenario.wait_requests
                    if request.request_id in active_request_ids
                ),
            )
            v2_plan = optimize_plan_with_exposure_debt(
                scenario,
                exposure_debt_by_request_id={
                    request_id: debt[request_id] for request_id in active_request_ids
                },
            ).plan
            alternatives = enumerate_primary_optimal_plans(scenario)
            round_count += 1
            multiple_plan_rounds += len(alternatives) > 1

            primary_score = (
                alternatives[0].recovered_minutes,
                len(alternatives[0].assignments),
            )
            if (v2_plan.recovered_minutes, len(v2_plan.assignments)) != primary_score:
                non_primary_optimal_v2_rounds += 1

            eligible_request_ids = {
                evaluation.request_id
                for evaluation in v2_plan.evaluations
                if evaluation.eligible
            }
            selected_request_ids = {
                assignment.request_id for assignment in v2_plan.assignments
            }
            alternative_selected_ids = tuple(
                {assignment.request_id for assignment in plan.assignments}
                for plan in alternatives
            )

            round_slice_keys = {
                slice_key
                for request_id in eligible_request_ids
                for slice_key in audit_by_request[request_id].dimension_values()
            }
            for slice_key in round_slice_keys:
                totals = slice_totals.setdefault(slice_key, _MutableSliceDiagnostic())
                eligible_ids_in_slice = {
                    request_id
                    for request_id in eligible_request_ids
                    if slice_key in audit_by_request[request_id].dimension_values()
                }
                actual_exposure_count = len(
                    selected_request_ids & eligible_ids_in_slice
                )
                best_alternative_count = max(
                    len(alternative_ids & eligible_ids_in_slice)
                    for alternative_ids in alternative_selected_ids
                )
                improvement = max(0, best_alternative_count - actual_exposure_count)
                totals.eligible_opportunities += len(eligible_ids_in_slice)
                totals.actual_exposures += actual_exposure_count
                totals.rounds_with_improving_alternative += improvement > 0
                totals.additional_exposure_capacity += improvement

            for request_id in eligible_request_ids - selected_request_ids:
                debt[request_id] += 1
            active_request_ids.difference_update(selected_request_ids)

    return AlternativeDiagnosticReport(
        schema_version="1.0",
        split=EvaluationSplit.DEVELOPMENT,
        seed_count=len(MULTI_SLOT_SEEDS[EvaluationSplit.DEVELOPMENT]),
        requested_rounds_per_seed=rounds,
        round_count=round_count,
        rounds_with_multiple_primary_plans=multiple_plan_rounds,
        non_primary_optimal_v2_rounds=non_primary_optimal_v2_rounds,
        slices=tuple(
            SliceAlternativeDiagnostic(
                dimension=dimension,
                value=value,
                eligible_opportunities=totals.eligible_opportunities,
                actual_exposures=totals.actual_exposures,
                rounds_with_improving_alternative=(
                    totals.rounds_with_improving_alternative
                ),
                additional_exposure_capacity=totals.additional_exposure_capacity,
                supported=totals.eligible_opportunities >= SUPPORT_THRESHOLD,
            )
            for (dimension, value), totals in sorted(slice_totals.items())
        ),
    )
