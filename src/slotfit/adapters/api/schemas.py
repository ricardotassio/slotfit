from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthResponse(ApiModel):
    status: Literal["ok"]
    application_version: str
    schema_version: str


class TimeWindowResponse(ApiModel):
    start: datetime
    end: datetime
    duration_minutes: int


class OpenIntervalResponse(ApiModel):
    interval_id: str
    provider_id: str
    room_id: str
    window: TimeWindowResponse


class WaitRequestResponse(ApiModel):
    request_id: str
    duration_minutes: int
    joined_order: int
    minimum_notice_minutes: int
    communication_consent: bool
    required_room_id: str | None


class AssignmentResponse(ApiModel):
    request_id: str
    interval_id: str
    scheduled_window: TimeWindowResponse


class CandidateEvaluationResponse(ApiModel):
    request_id: str
    interval_id: str
    eligible: bool
    reason_codes: list[str]
    explanations: list[str]


class PlanResponse(ApiModel):
    strategy: str
    assignments: list[AssignmentResponse]
    recovered_minutes: int
    remaining_gap_minutes: int
    evaluations: list[CandidateEvaluationResponse]


class SolverPhaseResponse(ApiModel):
    name: str
    status: str
    objective_value: int | None


class OptimizerEvidenceResponse(ApiModel):
    status: str
    optimized: bool
    engine_version: str
    phases: list[SolverPhaseResponse]
    research_candidate_accepted: bool


class BookedAppointmentResponse(ApiModel):
    label: str
    provider_id: str
    room_id: str
    window: TimeWindowResponse


class CancellationResponse(ApiModel):
    interval_id: str
    cancelled_at: datetime


class DayContextResponse(ApiModel):
    day_window: TimeWindowResponse
    booked: list[BookedAppointmentResponse]
    cancellations: list[CancellationResponse]
    closed_room_ids: list[str]


class DemoResponse(ApiModel):
    schema_version: str
    scenario_id: str
    synthetic: Literal[True]
    automatic_action: Literal["none"]
    intervals: list[OpenIntervalResponse]
    requests: list[WaitRequestResponse]
    plans: list[PlanResponse]
    optimizer_evidence: OptimizerEvidenceResponse | None
    day_context: DayContextResponse | None
    disclosure: str


class ErrorDetail(ApiModel):
    code: str
    message: str


class ErrorResponse(ApiModel):
    schema_version: str
    error: ErrorDetail


class CandidateDecisionResponse(ApiModel):
    candidate: str
    idea: str
    mean_utilization_percent: float
    worst_supported_degradation_percentage_points: float
    decision: Literal["reject"]


class GuardrailResponse(ApiModel):
    name: str
    limit_percentage_points: float
    direction: Literal["maximum"]


class DevelopmentDecisionResponse(ApiModel):
    schema_version: str
    split: Literal["development"]
    seed_count: int
    candidate_accepted: Literal[False]
    calibration_open: Literal[False]
    final_frozen_set_exists: Literal[False]
    guardrail: GuardrailResponse
    candidates: list[CandidateDecisionResponse]
    decision: str
    evidence_boundary: str


class ReviewCommandRequest(ApiModel):
    schema_version: Literal["1.0"]
    idempotency_key: Annotated[
        str,
        StringConstraints(pattern=r"^[!-~]{1,64}$"),
    ]
    scenario_id: Annotated[str, StringConstraints(min_length=1, max_length=128)]
    strategy: Annotated[str, StringConstraints(min_length=1, max_length=128)]
    plan_checksum: Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
    decision: Literal["accept", "reject", "request_alternative"]
    rationale: Annotated[str, StringConstraints(max_length=500)] | None = None


class ReviewEventResponse(ApiModel):
    event_id: str
    created_at: datetime
    idempotency_key: str
    scenario_id: str
    strategy: str
    plan_checksum: str
    decision: Literal["accept", "reject", "request_alternative"]
    rationale: str | None
    external_action: Literal["none"]


class RecordReviewResponse(ApiModel):
    schema_version: str
    event: ReviewEventResponse
    created: bool
    replayed: bool
