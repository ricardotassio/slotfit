# SF-004 — Read-only HTTP boundary

- Status: Ready
- AI-DLC mapping: Bolt S4
- Depends on: SF-003 terminal no-go
- Dependency boundary: add FastAPI/Pydantic/TestClient dependencies only after
  the contract tests fail because the adapter does not exist

## Purpose

Expose the synthetic demonstration and the development decision to a local UI
without moving domain rules into HTTP code or implying that a rejected optimizer
is safe to recommend.

## Endpoints

### `GET /health`

Return service status, application version and schema version. This endpoint does
not execute the solver.

### `GET /api/v1/demos/{demo_id}`

Supported IDs are `single-opening` and `global-conflict`. The response includes:

- `schema_version`, `scenario_id`, `synthetic: true` and `automatic_action: none`;
- deterministic interval and request summaries needed by a visual client;
- exactly two baseline plans for `single-opening`;
- the two baselines plus the V1 CP-SAT counterexample plan for `global-conflict`;
- assignments, recovered minutes, remaining gap and stable exclusion reason codes;
- optimizer phase/status evidence when the CP-SAT plan is present;
- a disclosure that the global-conflict plan proves a controlled assignment
  capability, not acceptance of the longitudinal research candidate.

An unknown demo ID returns a versioned `404` error with stable code
`demo_not_found`. No request body is accepted.

### `GET /api/v1/research/development-decision`

Return a checked-in summary of the completed SF-003 decision: V1–V4 observations,
the fixed limit, `candidate_accepted: false`, `calibration_open: false`,
`final_frozen_set_exists: false` and the public evidence boundary. It must not run
the 40-seed experiment on every request or describe V4 as a recommendation.

## Architecture boundary

- `slotfit.api` owns FastAPI routing and exception translation.
- `slotfit.api_schemas` owns Pydantic transport models.
- `slotfit.api_service` converts existing domain results to transport-neutral
  dictionaries or value objects.
- Domain, eligibility and strategy modules never import FastAPI or Pydantic.
- All endpoints are read-only, deterministic and free of network/database access.
- CORS is not enabled until a concrete local UI origin exists.

## Error and safety contract

- Client-visible errors use `{schema_version, error: {code, message}}`.
- Internal exception text and stack traces are not part of the contract.
- There are no booking, messaging, external integration or real-data endpoints.
- There is no endpoint that accepts a patient, provider or clinic payload.
- Every plan response says `automatic_action: none`.

## Dependency decision

- `fastapi==0.162.0` for the synchronous local REST adapter and generated OpenAPI;
- `pydantic==2.14.1` for explicit versioned response validation;
- `httpx==0.28.1` for FastAPI's in-process `TestClient` contract tests.

The versions are pinned for replay. GraphQL, gRPC, authentication, queues and
microservices are outside this local synthetic POC.

## Red, green, refactor

1. Red: contract tests import the missing app and assert the three endpoint
   families, error shape and OpenAPI paths.
2. Green: add pinned dependencies and the smallest adapter/service/schema split.
3. Refactor: centralize deterministic serialization without modifying domain
   dataclasses.
4. Verify: focused API tests, `make test`, `make api-smoke` and OpenAPI assertions.

## Acceptance criteria

- [ ] Health response is versioned and does not run planning.
- [ ] Both deterministic demos return two or three explainable plans.
- [ ] The global counterexample exposes three `OPTIMAL` phases and a disclosure.
- [ ] Unknown demo IDs return the stable versioned error contract.
- [ ] Development decision reports the terminal no-go without recomputation.
- [ ] OpenAPI exposes only the declared read-only routes.
- [ ] Domain and strategy modules remain framework-independent.
- [ ] Tests use no network, database, real data or external action.
- [ ] `make test` and `make api-smoke` pass from the pinned environment.

## Rejection conditions

- an endpoint presents V4 as accepted or recommended;
- transport models enter the domain core;
- a route accepts arbitrary scenario/identity data in this Bolt;
- the API performs a message, booking or external mutation;
- errors expose stack traces or unstable exception strings.
