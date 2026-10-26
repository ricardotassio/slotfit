from __future__ import annotations

from dataclasses import dataclass

from slotfit.domain.eligibility import scheduled_window
from slotfit.domain.model import CandidatePlan
from slotfit.research.generation import (
    EvaluationSplit,
    GeneratedScenario,
    RequestAuditSlice,
    decision_checksum,
)


@dataclass(frozen=True, slots=True)
class HardConstraintViolation:
    request_id: str
    interval_id: str
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RequestEvaluationRecord:
    request_id: str
    interval_id: str
    eligible_opportunity: bool
    selected: bool
    reason_codes: tuple[str, ...]
    audit_slice: RequestAuditSlice


@dataclass(frozen=True, slots=True)
class ScenarioEvaluation:
    scenario_id: str
    seed: int
    split: EvaluationSplit
    generator_version: str
    distribution_config_id: str
    decision_checksum: str
    strategy: str
    recovered_minutes: int
    feasible_open_minutes: int
    recovered_utilization: float | None
    hard_constraint_violations: tuple[HardConstraintViolation, ...]
    requests: tuple[RequestEvaluationRecord, ...]


def evaluate_generated_plan(
    generated: GeneratedScenario,
    plan: CandidatePlan,
) -> ScenarioEvaluation:
    """Create evaluator-only evidence after a strategy has produced a plan.

    Waiting time and starvation are intentionally absent: neither can be measured
    honestly from a single event.
    """

    scenario = generated.scenario
    if generated.manifest.seed != scenario.seed:
        raise ValueError("manifest seed must match scenario seed")
    if generated.manifest.decision_checksum != decision_checksum(scenario):
        raise ValueError("manifest decision checksum must match scenario decision data")

    request_ids = {request.request_id for request in scenario.wait_requests}
    slice_ids = [audit_slice.request_id for audit_slice in generated.manifest.audit_slices]
    if len(slice_ids) != len(set(slice_ids)) or set(slice_ids) != request_ids:
        raise ValueError("audit slice request IDs must match scenario request IDs exactly")

    audit_by_request = {
        audit_slice.request_id: audit_slice
        for audit_slice in generated.manifest.audit_slices
    }
    evaluation_by_key = {
        (evaluation.request_id, evaluation.interval_id): evaluation
        for evaluation in plan.evaluations
    }
    if len(evaluation_by_key) != len(plan.evaluations):
        raise ValueError("candidate evaluations must be unique per request and interval")

    selected_keys = {
        (assignment.request_id, assignment.interval_id)
        for assignment in plan.assignments
    }
    interval_by_id = {
        interval.interval_id: interval for interval in scenario.open_intervals
    }
    request_by_id = {
        request.request_id: request for request in scenario.wait_requests
    }

    violations: list[HardConstraintViolation] = []
    for assignment in plan.assignments:
        key = (assignment.request_id, assignment.interval_id)
        candidate = evaluation_by_key.get(key)
        reasons: list[str] = []
        if candidate is None:
            reasons.append("MISSING_ELIGIBILITY_EVALUATION")
        elif not candidate.eligible:
            reasons.extend(candidate.reason_codes)

        request = request_by_id.get(assignment.request_id)
        interval = interval_by_id.get(assignment.interval_id)
        if request is None:
            reasons.append("UNKNOWN_REQUEST")
        if interval is None:
            reasons.append("UNKNOWN_INTERVAL")
        if request is not None and interval is not None:
            if assignment.scheduled_window != scheduled_window(interval, request):
                reasons.append("INVALID_SCHEDULED_WINDOW")

        if reasons:
            violations.append(
                HardConstraintViolation(
                    request_id=assignment.request_id,
                    interval_id=assignment.interval_id,
                    reason_codes=tuple(dict.fromkeys(reasons)),
                )
            )

    records = tuple(
        RequestEvaluationRecord(
            request_id=evaluation.request_id,
            interval_id=evaluation.interval_id,
            eligible_opportunity=evaluation.eligible,
            selected=(evaluation.request_id, evaluation.interval_id) in selected_keys,
            reason_codes=evaluation.reason_codes,
            audit_slice=audit_by_request[evaluation.request_id],
        )
        for evaluation in plan.evaluations
    )
    feasible_interval_ids = {
        record.interval_id for record in records if record.eligible_opportunity
    }
    feasible_open_minutes = sum(
        interval_by_id[interval_id].window.duration_minutes
        for interval_id in feasible_interval_ids
    )
    recovered_utilization = (
        plan.recovered_minutes / feasible_open_minutes
        if feasible_open_minutes
        else None
    )

    return ScenarioEvaluation(
        scenario_id=scenario.scenario_id,
        seed=generated.manifest.seed,
        split=generated.manifest.split,
        generator_version=generated.manifest.generator_version,
        distribution_config_id=generated.manifest.distribution_config_id,
        decision_checksum=generated.manifest.decision_checksum,
        strategy=plan.strategy,
        recovered_minutes=plan.recovered_minutes,
        feasible_open_minutes=feasible_open_minutes,
        recovered_utilization=recovered_utilization,
        hard_constraint_violations=tuple(violations),
        requests=records,
    )
