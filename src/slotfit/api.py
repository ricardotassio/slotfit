from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from slotfit.api_schemas import (
    DemoResponse,
    DevelopmentDecisionResponse,
    ErrorResponse,
    HealthResponse,
    RecordReviewResponse,
    ReviewCommandRequest,
    ReviewEventResponse,
)
from slotfit.api_service import SCHEMA_VERSION, get_demo, get_development_decision
from slotfit.persistence import (
    IdempotencyConflict,
    ReviewCommand,
    SQLiteReviewRepository,
)


APPLICATION_VERSION = "0.1.0"

app = FastAPI(
    title="SlotFit synthetic experiment API",
    version=APPLICATION_VERSION,
    description="Read-only local boundary for synthetic scheduling evidence.",
)

_default_review_repository = SQLiteReviewRepository(
    Path("artifacts/reviews/slotfit.db")
)


def get_review_repository() -> SQLiteReviewRepository:
    return _default_review_repository


def _error(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "schema_version": SCHEMA_VERSION,
            "error": {"code": code, "message": message},
        },
    )


@app.exception_handler(RequestValidationError)
def validation_error(
    _request: Request,
    _exception: RequestValidationError,
) -> JSONResponse:
    return _error(
        422,
        "validation_error",
        "The request does not match the API contract.",
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        application_version=APPLICATION_VERSION,
        schema_version=SCHEMA_VERSION,
    )


@app.get(
    "/api/v1/demos/{demo_id}",
    response_model=DemoResponse,
    responses={404: {"model": ErrorResponse}},
)
def demo(demo_id: str) -> DemoResponse | JSONResponse:
    result = get_demo(demo_id)
    if result is not None:
        return result
    return JSONResponse(
        status_code=404,
        content={
            "schema_version": SCHEMA_VERSION,
            "error": {
                "code": "demo_not_found",
                "message": "The requested synthetic demo does not exist.",
            },
        },
    )


@app.get(
    "/api/v1/research/development-decision",
    response_model=DevelopmentDecisionResponse,
)
def development_decision() -> DevelopmentDecisionResponse:
    return get_development_decision()


@app.post(
    "/api/v1/reviews",
    response_model=RecordReviewResponse,
    status_code=201,
    responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
def record_review(
    payload: ReviewCommandRequest,
    repository: SQLiteReviewRepository = Depends(get_review_repository),
) -> RecordReviewResponse | JSONResponse:
    command = ReviewCommand(
        idempotency_key=payload.idempotency_key,
        scenario_id=payload.scenario_id,
        strategy=payload.strategy,
        plan_checksum=payload.plan_checksum,
        decision=payload.decision,
        rationale=payload.rationale,
    )
    try:
        result = repository.record(command)
    except IdempotencyConflict:
        return _error(
            409,
            "idempotency_conflict",
            "The idempotency key is already associated with a different review.",
        )
    response = RecordReviewResponse(
        schema_version=SCHEMA_VERSION,
        event=ReviewEventResponse.model_validate(result.event, from_attributes=True),
        created=result.created,
        replayed=result.replayed,
    )
    if result.replayed:
        return JSONResponse(status_code=200, content=response.model_dump(mode="json"))
    return response


@app.get(
    "/api/v1/reviews/{event_id}",
    response_model=ReviewEventResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_review(
    event_id: str,
    repository: SQLiteReviewRepository = Depends(get_review_repository),
) -> ReviewEventResponse | JSONResponse:
    event = repository.get(event_id)
    if event is None:
        return _error(404, "review_not_found", "The review event does not exist.")
    return ReviewEventResponse.model_validate(event, from_attributes=True)
