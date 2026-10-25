from __future__ import annotations

from slotfit.api_schemas import (
    AssignmentResponse,
    CandidateDecisionResponse,
    CandidateEvaluationResponse,
    DemoResponse,
    DevelopmentDecisionResponse,
    GuardrailResponse,
    OpenIntervalResponse,
    OptimizerEvidenceResponse,
    PlanResponse,
    SolverPhaseResponse,
    TimeWindowResponse,
    WaitRequestResponse,
)
from slotfit.domain import CandidatePlan, Scenario, TimeWindow
from slotfit.optimizer import OptimizationResult, optimize_plan
from slotfit.scenarios import demo_scenario, multi_slot_counterexample
from slotfit.strategies import best_fit_plan, fifo_plan


SCHEMA_VERSION = "1.0"


def _window(value: TimeWindow) -> TimeWindowResponse:
    return TimeWindowResponse(
        start=value.start,
        end=value.end,
        duration_minutes=value.duration_minutes,
    )


def _plan(value: CandidatePlan) -> PlanResponse:
    return PlanResponse(
        strategy=value.strategy,
        assignments=[
            AssignmentResponse(
                request_id=item.request_id,
                interval_id=item.interval_id,
                scheduled_window=_window(item.scheduled_window),
            )
            for item in value.assignments
        ],
        recovered_minutes=value.recovered_minutes,
        remaining_gap_minutes=value.remaining_gap_minutes,
        evaluations=[
            CandidateEvaluationResponse(
                request_id=item.request_id,
                interval_id=item.interval_id,
                eligible=item.eligible,
                reason_codes=list(item.reason_codes),
            )
            for item in value.evaluations
        ],
    )


def _optimizer_evidence(value: OptimizationResult) -> OptimizerEvidenceResponse:
    return OptimizerEvidenceResponse(
        status=value.status,
        optimized=value.optimized,
        engine_version=value.engine_version,
        phases=[
            SolverPhaseResponse(
                name=phase.name,
                status=phase.status,
                objective_value=phase.objective_value,
            )
            for phase in value.phases
        ],
        research_candidate_accepted=False,
    )


def _demo_response(
    scenario: Scenario,
    plans: tuple[CandidatePlan, ...],
    *,
    optimizer_result: OptimizationResult | None,
    disclosure: str,
) -> DemoResponse:
    return DemoResponse(
        schema_version=SCHEMA_VERSION,
        scenario_id=scenario.scenario_id,
        synthetic=True,
        automatic_action="none",
        intervals=[
            OpenIntervalResponse(
                interval_id=item.interval_id,
                provider_id=item.provider_id,
                room_id=item.room_id,
                window=_window(item.window),
            )
            for item in scenario.open_intervals
        ],
        requests=[
            WaitRequestResponse(
                request_id=item.request_id,
                duration_minutes=item.duration_minutes,
                joined_order=item.joined_order,
                minimum_notice_minutes=item.minimum_notice_minutes,
                communication_consent=item.communication_consent,
                required_room_id=item.required_room_id,
            )
            for item in scenario.wait_requests
        ],
        plans=[_plan(item) for item in plans],
        optimizer_evidence=(
            _optimizer_evidence(optimizer_result) if optimizer_result is not None else None
        ),
        disclosure=disclosure,
    )


def get_demo(demo_id: str) -> DemoResponse | None:
    if demo_id == "single-opening":
        scenario = demo_scenario(seed=1400)
        return _demo_response(
            scenario,
            (fifo_plan(scenario), best_fit_plan(scenario)),
            optimizer_result=None,
            disclosure=(
                "Synthetic local-choice demonstration only; every simulated decision remains "
                "human-owned."
            ),
        )
    if demo_id == "global-conflict":
        scenario = multi_slot_counterexample(seed=1500)
        optimizer_result = optimize_plan(scenario)
        return _demo_response(
            scenario,
            (fifo_plan(scenario), best_fit_plan(scenario), optimizer_result.plan),
            optimizer_result=optimizer_result,
            disclosure=(
                "This controlled counterexample demonstrates global assignment capability. "
                "It does not make the rejected longitudinal research candidate acceptable."
            ),
        )
    return None


def get_development_decision() -> DevelopmentDecisionResponse:
    observations = (
        ("V1", "static lexicographic optimum", 96.81, 12.58),
        ("V2", "prior compatible-opportunity debt", 96.81, 12.58),
        ("V3", "label-free placement scarcity", 96.81, 12.35),
        ("V4", "90% per-round recovered-minute floor", 95.71, 10.80),
    )
    return DevelopmentDecisionResponse(
        schema_version=SCHEMA_VERSION,
        split="development",
        seed_count=40,
        candidate_accepted=False,
        calibration_open=False,
        final_frozen_set_exists=False,
        guardrail=GuardrailResponse(
            name="worst_supported_slice_degradation",
            limit_percentage_points=10.0,
            direction="maximum",
        ),
        candidates=[
            CandidateDecisionResponse(
                candidate=candidate,
                idea=idea,
                mean_utilization_percent=utilization,
                worst_supported_degradation_percentage_points=degradation,
                decision="reject",
            )
            for candidate, idea, utilization, degradation in observations
        ],
        decision=(
            "Terminal no-go: all four candidates failed the unchanged development guardrail."
        ),
        evidence_boundary=(
            "Controlled synthetic observations only; no clinical, access, financial, "
            "demographic-fairness or production-readiness claim."
        ),
    )

