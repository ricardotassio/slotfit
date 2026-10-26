from __future__ import annotations

from collections.abc import Callable, Mapping
from types import MappingProxyType

from slotfit.adapters.api.schemas import (
    AssignmentResponse,
    BookedAppointmentResponse,
    CancellationResponse,
    CandidateDecisionResponse,
    CandidateEvaluationResponse,
    DayContextResponse,
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
from slotfit.domain.day_context import DayContext
from slotfit.domain.model import CandidatePlan, Scenario, TimeWindow
from slotfit.domain.explanations import explain_evaluation
from slotfit.solver.optimizer import OptimizationResult, optimize_plan
from slotfit.application.scenarios import clinic_day_story, demo_scenario, multi_slot_counterexample
from slotfit.application.strategies import best_fit_plan, fifo_plan


SCHEMA_VERSION = "1.1"


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
                explanations=list(explain_evaluation(item)),
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


def _day_context(value: DayContext) -> DayContextResponse:
    return DayContextResponse(
        day_window=_window(value.day_window),
        booked=[
            BookedAppointmentResponse(
                label=item.label,
                provider_id=item.provider_id,
                room_id=item.room_id,
                window=_window(item.window),
            )
            for item in value.booked
        ],
        cancellations=[
            CancellationResponse(interval_id=item.interval_id, cancelled_at=item.cancelled_at)
            for item in value.cancellations
        ],
        closed_room_ids=list(value.closed_room_ids),
    )


COUNTEREXAMPLE_DISCLOSURE = (
    "This controlled counterexample demonstrates global assignment capability. "
    "It does not make the rejected longitudinal research candidate acceptable."
)


def _demo_response(
    scenario: Scenario,
    plans: tuple[CandidatePlan, ...],
    *,
    optimizer_result: OptimizationResult | None,
    disclosure: str,
    day_context: DayContext | None = None,
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
        day_context=_day_context(day_context) if day_context is not None else None,
        disclosure=disclosure,
    )


def _single_opening_demo() -> DemoResponse:
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


def _global_conflict_demo() -> DemoResponse:
    scenario = multi_slot_counterexample(seed=1500)
    optimizer_result = optimize_plan(scenario)
    return _demo_response(
        scenario,
        (fifo_plan(scenario), best_fit_plan(scenario), optimizer_result.plan),
        optimizer_result=optimizer_result,
        disclosure=COUNTEREXAMPLE_DISCLOSURE,
    )


def _clinic_day_demo() -> DemoResponse:
    scenario, context = clinic_day_story(seed=1600)
    optimizer_result = optimize_plan(scenario)
    return _demo_response(
        scenario,
        (fifo_plan(scenario), best_fit_plan(scenario), optimizer_result.plan),
        optimizer_result=optimizer_result,
        disclosure=COUNTEREXAMPLE_DISCLOSURE,
        day_context=context,
    )


DEMO_BUILDERS: Mapping[str, Callable[[], DemoResponse]] = MappingProxyType(
    {
        "single-opening": _single_opening_demo,
        "global-conflict": _global_conflict_demo,
        "clinic-day": _clinic_day_demo,
    }
)


def get_demo(demo_id: str) -> DemoResponse | None:
    builder = DEMO_BUILDERS.get(demo_id)
    return builder() if builder is not None else None


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

