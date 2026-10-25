from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, fields, replace
from statistics import mean, median

from slotfit.domain import CandidatePlan, Scenario
from slotfit.evaluation import evaluate_generated_plan
from slotfit.generation import EvaluationSplit, RequestAuditSlice
from slotfit.longitudinal import (
    DebtAwareStrategy,
    LongitudinalRequestRecord,
    simulate_exposure_debt_rounds,
    simulate_opportunity_rounds,
)
from slotfit.multi_generation import (
    DEFAULT_MULTI_SLOT_CONFIG,
    MULTI_SLOT_SEEDS,
    generate_multi_slot_scenario,
)
from slotfit.optimizer import OptimizationResult, optimize_plan_with_exposure_debt
from slotfit.strategies import best_fit_plan, fifo_plan


Planner = Callable[[Scenario], CandidatePlan]


@dataclass(frozen=True, slots=True)
class ScenarioComparison:
    seed: int
    strategy: str
    recovered_minutes: int
    feasible_open_minutes: int
    recovered_utilization: float | None
    assignments: int
    hard_constraint_violations: int
    optimizer_status: str | None
    optimized: bool | None
    phase_statuses: tuple[str, ...] | None
    phase_objective_values: tuple[int | None, ...] | None
    solver_wall_time_seconds: float | None = field(compare=False)
    opaque_id_flip: bool = False
    input_order_flip: bool = False


@dataclass(frozen=True, slots=True)
class SliceComparison:
    dimension: str
    value: str
    support: int
    exposure_rate: float | None
    starvation_rate_k3: float | None
    exposure_gap_from_overall: float | None
    supported: bool


@dataclass(frozen=True, slots=True)
class StrategyComparison:
    strategy: str
    scenario_count: int
    mean_recovered_utilization: float
    median_recovered_utilization: float
    mean_requests_served: float
    hard_constraint_violations: int
    opaque_id_flips: int
    input_order_flips: int
    optimized_runs: int | None
    mean_solver_wall_time_seconds: float | None = field(compare=False)
    p90_solver_wall_time_seconds: float | None = field(compare=False)
    history_count: int
    median_compatible_misses: float
    p90_compatible_misses: int
    starvation_rate_k2: float
    starvation_rate_k3: float
    starvation_rate_k4: float
    overall_exposure_rate: float
    worst_supported_slice: str | None
    worst_supported_gap: float | None
    slices: tuple[SliceComparison, ...]


@dataclass(frozen=True, slots=True)
class GuardrailCheck:
    name: str
    observed_value: float
    limit: float
    passed: bool
    detail: str


@dataclass(frozen=True, slots=True)
class EngineeringComparison:
    schema_version: str
    split: EvaluationSplit
    generator_version: str
    distribution_config_id: str
    seed_count: int
    seed_registry_checksum: str
    opportunity_rounds: int
    starvation_k: int
    scenarios: tuple[ScenarioComparison, ...]
    strategies: tuple[StrategyComparison, ...]
    guardrails: tuple[GuardrailCheck, ...]
    candidate_accepted: bool


def _percentile_90(values: list[int]) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    return ordered[max(0, math.ceil(0.9 * len(ordered)) - 1)]


def _percentile_90_float(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(0.9 * len(ordered)) - 1)]


def _rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _slice_values(audit_slice: RequestAuditSlice) -> tuple[tuple[str, str], ...]:
    return tuple(
        (field.name, str(getattr(audit_slice, field.name)))
        for field in fields(RequestAuditSlice)
        if field.name != "request_id"
    )


def _slice_comparisons(
    histories: list[LongitudinalRequestRecord],
    overall_exposure_rate: float,
) -> tuple[SliceComparison, ...]:
    grouped: dict[tuple[str, str], list[LongitudinalRequestRecord]] = {}
    for history in histories:
        for dimension_and_value in _slice_values(history.audit_slice):
            grouped.setdefault(dimension_and_value, []).append(history)

    results: list[SliceComparison] = []
    for (dimension, value), records in sorted(grouped.items()):
        support = sum(record.eligible_opportunities for record in records)
        exposures = sum(record.plan_exposures for record in records)
        eligible_histories = [record for record in records if record.eligible_opportunities]
        starvation_events = sum(
            record.unselected_compatible_opportunities >= 3
            for record in eligible_histories
        )
        exposure_rate = _rate(exposures, support)
        results.append(
            SliceComparison(
                dimension=dimension,
                value=value,
                support=support,
                exposure_rate=exposure_rate,
                starvation_rate_k3=_rate(starvation_events, len(eligible_histories)),
                exposure_gap_from_overall=(
                    overall_exposure_rate - exposure_rate
                    if exposure_rate is not None
                    else None
                ),
                supported=support >= 30,
            )
        )
    return tuple(results)


def _strategy_summary(
    strategy: str,
    scenarios: list[ScenarioComparison],
    histories: list[LongitudinalRequestRecord],
) -> StrategyComparison:
    utilizations = [
        item.recovered_utilization
        for item in scenarios
        if item.recovered_utilization is not None
    ]
    eligible_histories = [item for item in histories if item.eligible_opportunities]
    misses = [item.unselected_compatible_opportunities for item in eligible_histories]
    total_opportunities = sum(item.eligible_opportunities for item in eligible_histories)
    total_exposures = sum(item.plan_exposures for item in eligible_histories)
    overall_exposure_rate = _rate(total_exposures, total_opportunities) or 0.0
    slice_results = _slice_comparisons(eligible_histories, overall_exposure_rate)
    supported_slices = [
        item
        for item in slice_results
        if item.supported and item.exposure_gap_from_overall is not None
    ]
    worst_slice = (
        max(supported_slices, key=lambda item: item.exposure_gap_from_overall or 0.0)
        if supported_slices
        else None
    )
    optimized_values = [item.optimized for item in scenarios if item.optimized is not None]
    solver_times = [
        item.solver_wall_time_seconds
        for item in scenarios
        if item.solver_wall_time_seconds is not None
    ]

    return StrategyComparison(
        strategy=strategy,
        scenario_count=len(scenarios),
        mean_recovered_utilization=mean(utilizations),
        median_recovered_utilization=median(utilizations),
        mean_requests_served=mean(item.assignments for item in scenarios),
        hard_constraint_violations=sum(
            item.hard_constraint_violations for item in scenarios
        ),
        opaque_id_flips=sum(item.opaque_id_flip for item in scenarios),
        input_order_flips=sum(item.input_order_flip for item in scenarios),
        optimized_runs=(
            sum(value is True for value in optimized_values)
            if optimized_values
            else None
        ),
        mean_solver_wall_time_seconds=(mean(solver_times) if solver_times else None),
        p90_solver_wall_time_seconds=_percentile_90_float(solver_times),
        history_count=len(eligible_histories),
        median_compatible_misses=median(misses) if misses else 0.0,
        p90_compatible_misses=_percentile_90(misses),
        starvation_rate_k2=_rate(
            sum(value >= 2 for value in misses),
            len(misses),
        )
        or 0.0,
        starvation_rate_k3=_rate(
            sum(value >= 3 for value in misses),
            len(misses),
        )
        or 0.0,
        starvation_rate_k4=_rate(
            sum(value >= 4 for value in misses),
            len(misses),
        )
        or 0.0,
        overall_exposure_rate=overall_exposure_rate,
        worst_supported_slice=(
            f"{worst_slice.dimension}={worst_slice.value}" if worst_slice else None
        ),
        worst_supported_gap=(
            worst_slice.exposure_gap_from_overall if worst_slice else None
        ),
        slices=slice_results,
    )


def _assignment_positions(scenario: Scenario, plan: CandidatePlan) -> frozenset[tuple[int, int]]:
    request_positions = {
        request.request_id: request.joined_order for request in scenario.wait_requests
    }
    interval_positions = {
        interval.interval_id: position
        for position, interval in enumerate(
            sorted(
                scenario.open_intervals,
                key=lambda item: (item.window.start, item.window.end),
            ),
            start=1,
        )
    }
    return frozenset(
        (
            request_positions[assignment.request_id],
            interval_positions[assignment.interval_id],
        )
        for assignment in plan.assignments
    )


def _counterfactual_flips(
    scenario: Scenario,
    planner: Planner,
    original_plan: CandidatePlan,
) -> tuple[bool, bool]:
    request_count = len(scenario.wait_requests)
    interval_count = len(scenario.open_intervals)
    renamed = replace(
        scenario,
        scenario_id=f"{scenario.scenario_id}-opaque-ids",
        wait_requests=tuple(
            replace(request, request_id=f"OPAQUE-R-{request_count - position + 1:03d}")
            for position, request in enumerate(scenario.wait_requests, start=1)
        ),
        open_intervals=tuple(
            replace(interval, interval_id=f"OPAQUE-I-{interval_count - position + 1:03d}")
            for position, interval in enumerate(scenario.open_intervals, start=1)
        ),
    )
    reordered = replace(
        scenario,
        wait_requests=tuple(reversed(scenario.wait_requests)),
        open_intervals=tuple(reversed(scenario.open_intervals)),
    )
    expected = _assignment_positions(scenario, original_plan)
    return (
        expected != _assignment_positions(renamed, planner(renamed)),
        expected != _assignment_positions(reordered, planner(reordered)),
    )


def _guardrail_checks(
    strategies: tuple[StrategyComparison, ...],
) -> tuple[GuardrailCheck, ...]:
    summaries = {item.strategy: item for item in strategies}
    candidate = summaries["cp-sat-exposure-debt@0.2.0"]
    baselines = (
        summaries["fifo-eligible@0.2.0"],
        summaries["local-best-fit@0.2.0"],
    )
    better_baseline_starvation = min(item.starvation_rate_k3 for item in baselines)

    baseline_slice_gaps: dict[tuple[str, str], float] = {}
    for slice_result in candidate.slices:
        if not slice_result.supported or slice_result.exposure_gap_from_overall is None:
            continue
        supported_gaps = [
            matching.exposure_gap_from_overall
            for baseline in baselines
            for matching in baseline.slices
            if matching.dimension == slice_result.dimension
            and matching.value == slice_result.value
            and matching.supported
            and matching.exposure_gap_from_overall is not None
        ]
        if supported_gaps:
            baseline_slice_gaps[(slice_result.dimension, slice_result.value)] = min(
                max(gap, 0.0) for gap in supported_gaps
            )
    degradations = [
        (
            max(slice_result.exposure_gap_from_overall, 0.0)
            - baseline_slice_gaps[(slice_result.dimension, slice_result.value)],
            f"{slice_result.dimension}={slice_result.value}",
        )
        for slice_result in candidate.slices
        if slice_result.supported
        and slice_result.exposure_gap_from_overall is not None
        and (slice_result.dimension, slice_result.value) in baseline_slice_gaps
    ]
    worst_degradation, worst_slice = max(degradations, default=(0.0, "none"))

    return (
        GuardrailCheck(
            name="hard-constraint-violations",
            observed_value=float(candidate.hard_constraint_violations),
            limit=0.0,
            passed=candidate.hard_constraint_violations == 0,
            detail="candidate violations across the development split",
        ),
        GuardrailCheck(
            name="opaque-id-flips",
            observed_value=float(candidate.opaque_id_flips),
            limit=0.0,
            passed=candidate.opaque_id_flips == 0,
            detail="assignment-position flips under opaque identifier renaming",
        ),
        GuardrailCheck(
            name="input-order-flips",
            observed_value=float(candidate.input_order_flips),
            limit=0.0,
            passed=candidate.input_order_flips == 0,
            detail="assignment-position flips under reversed input order",
        ),
        GuardrailCheck(
            name="starvation-rate-k3-degradation",
            observed_value=candidate.starvation_rate_k3 - better_baseline_starvation,
            limit=0.05,
            passed=(candidate.starvation_rate_k3 - better_baseline_starvation) <= 0.05,
            detail="candidate rate minus the lower development-baseline rate",
        ),
        GuardrailCheck(
            name="worst-supported-slice-gap-degradation",
            observed_value=worst_degradation,
            limit=0.10,
            passed=worst_degradation <= 0.10,
            detail=(
                "largest candidate-minus-supported-better-baseline exposure shortfall: "
                f"{worst_slice}; compared_slices={len(degradations)}"
            ),
        ),
    )


def compare_engineering_split(
    split: EvaluationSplit,
    *,
    opportunity_rounds: int = 5,
) -> EngineeringComparison:
    seeds = MULTI_SLOT_SEEDS[split]
    strategy_scenarios: dict[str, list[ScenarioComparison]] = {}
    strategy_histories: dict[str, list[LongitudinalRequestRecord]] = {}
    scenario_results: list[ScenarioComparison] = []

    def optimizer_planner(scenario: Scenario) -> CandidatePlan:
        return optimize_plan_with_exposure_debt(
            scenario,
            exposure_debt_by_request_id={},
        ).plan

    def debt_aware_optimizer_planner(
        scenario: Scenario,
        exposure_debt_by_request_id: Mapping[str, int],
    ) -> CandidatePlan:
        return optimize_plan_with_exposure_debt(
            scenario,
            exposure_debt_by_request_id=exposure_debt_by_request_id,
        ).plan

    planners: tuple[tuple[str, Planner, DebtAwareStrategy | None], ...] = (
        ("fifo-eligible@0.2.0", fifo_plan, None),
        ("local-best-fit@0.2.0", best_fit_plan, None),
        (
            "cp-sat-exposure-debt@0.2.0",
            optimizer_planner,
            debt_aware_optimizer_planner,
        ),
    )

    for seed in seeds:
        generated = generate_multi_slot_scenario(seed, split=split)
        for strategy_name, planner, debt_aware_planner in planners:
            optimization: OptimizationResult | None = None
            if debt_aware_planner is not None:
                optimization = optimize_plan_with_exposure_debt(
                    generated.scenario,
                    exposure_debt_by_request_id={},
                )
                plan = optimization.plan
            else:
                plan = planner(generated.scenario)
            evaluation = evaluate_generated_plan(generated, plan)
            opaque_id_flip, input_order_flip = _counterfactual_flips(
                generated.scenario,
                planner,
                plan,
            )
            scenario_result = ScenarioComparison(
                seed=seed,
                strategy=strategy_name,
                recovered_minutes=evaluation.recovered_minutes,
                feasible_open_minutes=evaluation.feasible_open_minutes,
                recovered_utilization=evaluation.recovered_utilization,
                assignments=len(plan.assignments),
                hard_constraint_violations=len(evaluation.hard_constraint_violations),
                optimizer_status=(str(optimization.status) if optimization else None),
                optimized=(optimization.optimized if optimization else None),
                phase_statuses=(
                    tuple(str(phase.status) for phase in optimization.phases)
                    if optimization
                    else None
                ),
                phase_objective_values=(
                    tuple(phase.objective_value for phase in optimization.phases)
                    if optimization
                    else None
                ),
                solver_wall_time_seconds=(
                    sum(phase.wall_time_seconds for phase in optimization.phases)
                    if optimization
                    else None
                ),
                opaque_id_flip=opaque_id_flip,
                input_order_flip=input_order_flip,
            )
            scenario_results.append(scenario_result)
            strategy_scenarios.setdefault(strategy_name, []).append(scenario_result)

            if debt_aware_planner is not None:
                longitudinal = simulate_exposure_debt_rounds(
                    generated,
                    debt_aware_planner,
                    rounds=opportunity_rounds,
                )
            else:
                longitudinal = simulate_opportunity_rounds(
                    generated,
                    planner,
                    rounds=opportunity_rounds,
                )
            strategy_histories.setdefault(strategy_name, []).extend(
                longitudinal.requests
            )

    strategy_results = tuple(
        _strategy_summary(
            strategy_name,
            strategy_scenarios[strategy_name],
            strategy_histories[strategy_name],
        )
        for strategy_name, _planner, _debt_aware_planner in planners
    )
    seed_payload = json.dumps(
        {"split": split.value, "seeds": seeds},
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    guardrails = _guardrail_checks(strategy_results)
    return EngineeringComparison(
        schema_version="1.0",
        split=split,
        generator_version=DEFAULT_MULTI_SLOT_CONFIG.generator_version,
        distribution_config_id=DEFAULT_MULTI_SLOT_CONFIG.distribution_config_id,
        seed_count=len(seeds),
        seed_registry_checksum=hashlib.sha256(seed_payload).hexdigest(),
        opportunity_rounds=opportunity_rounds,
        starvation_k=3,
        scenarios=tuple(scenario_results),
        strategies=strategy_results,
        guardrails=guardrails,
        candidate_accepted=all(check.passed for check in guardrails),
    )
