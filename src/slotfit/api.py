from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from slotfit.api_schemas import (
    DemoResponse,
    DevelopmentDecisionResponse,
    ErrorResponse,
    HealthResponse,
)
from slotfit.api_service import SCHEMA_VERSION, get_demo, get_development_decision


APPLICATION_VERSION = "0.1.0"

app = FastAPI(
    title="SlotFit synthetic experiment API",
    version=APPLICATION_VERSION,
    description="Read-only local boundary for synthetic scheduling evidence.",
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

