from __future__ import annotations

import math
from dataclasses import dataclass, replace

from slotfit.alternative_diagnostic import enumerate_feasible_plans
from slotfit.comparison import compare_engineering_split
from slotfit.domain import CandidatePlan, Scenario
from slotfit.generation import EvaluationSplit
from slotfit.multi_generation import MULTI_SLOT_SEEDS, generate_multi_slot_scenario
from slotfit.optimizer import optimize_plan_with_placement_scarcity


@dataclass(frozen=True, slots=True)
class LocalExposureFrontierPoint:
    minimum_recovered_ratio: float
    recovered_minutes: int
    optimal_recovered_minutes: int
    recovered_ratio: float
    requests_served: int
    overall_eligible_opportunities: int
    overall_exposures: int
    overall_exposure_rate: float
    target_exposures: int
    target_exposure_rate: float
    target_exposure_shortfall: float
    supported_better_baseline_shortfall: float
    target_shortfall_degradation: float
    target_guardrail_limit: float
    target_guardrail_passed: bool
    hard_constraint_violations: int


@dataclass(frozen=True, slots=True)
class LocalExposureFrontier:
    schema_version: str
    split: EvaluationSplit
    target_dimension: str
    target_value: str
    target_eligible_opportunities: int
    round_count: int
    local_path_assumption: str
    points: tuple[LocalExposureFrontierPoint, ...]
    highest_passing_floor: float | None


@dataclass(slots=True)
class _MutableFrontierPoint:
    recovered_minutes: int = 0
    optimal_recovered_minutes: int = 0
    requests_served: int = 0
    overall_eligible_opportunities: int = 0
    overall_exposures: int = 0
    target_eligible_opportunities: int = 0
    target_exposures: int = 0


def _assignment_position_signature(
    scenario: Scenario,
    plan: CandidatePlan,
) -> tuple[tuple[int, int], ...]:
    request_position = {
        request.request_id: request.joined_order for request in scenario.wait_requests
    }
    interval_position = {
        interval.interval_id: index
        for index, interval in enumerate(
            sorted(scenario.open_intervals, key=lambda item: item.window.start),
            start=1,
        )
    }
    return tuple(
        sorted(
            (
                request_position[assignment.request_id],
                interval_position[assignment.interval_id],
            )
            for assignment in plan.assignments
        )
    )


def _choose_local_oracle_plan(
    scenario: Scenario,
    plans: tuple[CandidatePlan, ...],
    target_request_ids: set[str],
    minimum_recovered_minutes: int,
) -> CandidatePlan:
    eligible_plans = tuple(
        plan for plan in plans if plan.recovered_minutes >= minimum_recovered_minutes
    )
    if not eligible_plans:
        raise ValueError("no feasible plan satisfies the declared recovered-minute floor")
    request_count = len(scenario.wait_requests)

    def order_key(plan: CandidatePlan) -> tuple[object, ...]:
        selected_ids = {assignment.request_id for assignment in plan.assignments}
        wait_age_score = sum(
            request_count + 1 - request.joined_order
            for request in scenario.wait_requests
            if request.request_id in selected_ids
        )
        return (
            -len(selected_ids & target_request_ids),
            -plan.recovered_minutes,
            -len(plan.assignments),
            -wait_age_score,
            _assignment_position_signature(scenario, plan),
        )

    return min(eligible_plans, key=order_key)


def _supported_baseline_shortfall(dimension: str, value: str) -> float:
    comparison = compare_engineering_split(EvaluationSplit.DEVELOPMENT)
    baseline_names = {"fifo-eligible@0.2.0", "local-best-fit@0.2.0"}
    gaps = [
        max(slice_result.exposure_gap_from_overall or 0.0, 0.0)
        for strategy in comparison.strategies
        if strategy.strategy in baseline_names
        for slice_result in strategy.slices
        if slice_result.dimension == dimension
        and slice_result.value == value
        and slice_result.supported
    ]
    if not gaps:
        raise ValueError("target slice has no supported baseline reference")
    return min(gaps)


def build_local_exposure_frontier(
    *,
    floors: tuple[float, ...] = (1.0, 0.95, 0.9, 0.8),
    target_dimension: str = "duration_band",
    target_value: str = "short",
    rounds: int = 5,
) -> LocalExposureFrontier:
    if not floors or any(floor <= 0 or floor > 1 for floor in floors):
        raise ValueError("frontier floors must be within (0, 1]")
    if tuple(sorted(floors, reverse=True)) != floors:
        raise ValueError("frontier floors must be declared in descending order")
    if rounds <= 0:
        raise ValueError("rounds must be positive")

    totals = {floor: _MutableFrontierPoint() for floor in floors}
    round_count = 0

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
                scenario_id=f"{generated.scenario.scenario_id}-frontier-{round_number:02d}",
                wait_requests=tuple(
                    request
                    for request in generated.scenario.wait_requests
                    if request.request_id in active_request_ids
                ),
            )
            v3_plan = optimize_plan_with_placement_scarcity(
                scenario,
                exposure_debt_by_request_id={
                    request_id: debt[request_id] for request_id in active_request_ids
                },
            ).plan
            feasible_plans = enumerate_feasible_plans(scenario)
            optimal_recovered = max(plan.recovered_minutes for plan in feasible_plans)
            eligible_request_ids = {
                evaluation.request_id
                for evaluation in v3_plan.evaluations
                if evaluation.eligible
            }
            target_request_ids = {
                request_id
                for request_id in eligible_request_ids
                if str(getattr(audit_by_request[request_id], target_dimension))
                == target_value
            }

            for floor in floors:
                minimum_minutes = math.ceil(optimal_recovered * floor)
                chosen = _choose_local_oracle_plan(
                    scenario,
                    feasible_plans,
                    target_request_ids,
                    minimum_minutes,
                )
                selected_ids = {
                    assignment.request_id for assignment in chosen.assignments
                }
                point = totals[floor]
                point.recovered_minutes += chosen.recovered_minutes
                point.optimal_recovered_minutes += optimal_recovered
                point.requests_served += len(chosen.assignments)
                point.overall_eligible_opportunities += len(eligible_request_ids)
                point.overall_exposures += len(selected_ids)
                point.target_eligible_opportunities += len(target_request_ids)
                point.target_exposures += len(selected_ids & target_request_ids)

            selected_v3_ids = {
                assignment.request_id for assignment in v3_plan.assignments
            }
            for request_id in eligible_request_ids - selected_v3_ids:
                debt[request_id] += 1
            active_request_ids.difference_update(selected_v3_ids)
            round_count += 1

    baseline_shortfall = _supported_baseline_shortfall(
        target_dimension,
        target_value,
    )
    points: list[LocalExposureFrontierPoint] = []
    for floor in floors:
        total = totals[floor]
        recovered_ratio = (
            total.recovered_minutes / total.optimal_recovered_minutes
            if total.optimal_recovered_minutes
            else 1.0
        )
        overall_rate = total.overall_exposures / total.overall_eligible_opportunities
        target_rate = total.target_exposures / total.target_eligible_opportunities
        shortfall = max(overall_rate - target_rate, 0.0)
        degradation = shortfall - baseline_shortfall
        points.append(
            LocalExposureFrontierPoint(
                minimum_recovered_ratio=floor,
                recovered_minutes=total.recovered_minutes,
                optimal_recovered_minutes=total.optimal_recovered_minutes,
                recovered_ratio=recovered_ratio,
                requests_served=total.requests_served,
                overall_eligible_opportunities=total.overall_eligible_opportunities,
                overall_exposures=total.overall_exposures,
                overall_exposure_rate=overall_rate,
                target_exposures=total.target_exposures,
                target_exposure_rate=target_rate,
                target_exposure_shortfall=shortfall,
                supported_better_baseline_shortfall=baseline_shortfall,
                target_shortfall_degradation=degradation,
                target_guardrail_limit=0.10,
                target_guardrail_passed=degradation <= 0.10,
                hard_constraint_violations=0,
            )
        )

    passing_floors = [
        point.minimum_recovered_ratio
        for point in points
        if point.target_guardrail_passed
    ]
    return LocalExposureFrontier(
        schema_version="1.0",
        split=EvaluationSplit.DEVELOPMENT,
        target_dimension=target_dimension,
        target_value=target_value,
        target_eligible_opportunities=totals[floors[0]].target_eligible_opportunities,
        round_count=round_count,
        local_path_assumption=(
            "each oracle choice is evaluated on the unchanged subsequent V3 cohort path"
        ),
        points=tuple(points),
        highest_passing_floor=max(passing_floors) if passing_floors else None,
    )
