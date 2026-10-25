from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


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


class DemoResponse(ApiModel):
    schema_version: str
    scenario_id: str
    synthetic: Literal[True]
    automatic_action: Literal["none"]
    intervals: list[OpenIntervalResponse]
    requests: list[WaitRequestResponse]
    plans: list[PlanResponse]
    optimizer_evidence: OptimizerEvidenceResponse | None
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

