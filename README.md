# SlotFit

SlotFit is an explainable scheduling experiment that studies how a clinic could respond to a cancellation without turning the workflow into opaque automation.

The project compares simple baselines with constraint optimization over entirely synthetic calendars. It never contacts a person, books an appointment, infers clinical urgency, or integrates with a real practice-management system.

## Current status

**AI-DLC Construction Bolts S1–S5 are implemented; CP-SAT candidates V1–V4 were
correctly rejected by development evidence before calibration, and the API exposes
that no-go without presenting it as a recommendation.**

The repository currently contains:

- the problem contract and non-goals;
- AI-DLC state, audit and execution plan;
- a small deterministic domain model;
- the first synthetic scenario;
- a versioned deterministic scenario generator with disjoint evaluation splits;
- FIFO and local best-fit baselines;
- evaluator-only operational slices and event-level evidence;
- deterministic opportunity rounds for repeated-exclusion analysis;
- metamorphic tests for opaque identifiers, input order and ineligible records;
- a multi-slot global-conflict fixture and lexicographic CP-SAT adapter;
- a 40-seed development comparison with per-slice guardrail decisions;
- an exposure-debt V2 whose focused behavior works but changes zero development
  selections, preserving the negative result;
- a bounded alternative-plan diagnostic showing where primary-optimal residual
  choices still exist;
- a placement-scarcity V3 that changes real development decisions but remains below
  the fixed exposure guardrail;
- a local oracle frontier that quantifies the observed efficiency/exposure trade-off
  without presenting the oracle as a deployable policy;
- a bounded-recovery V4 that improves but still fails the unchanged guardrail;
- a versioned FastAPI/Pydantic boundary for deterministic demos and research evidence;
- an idempotent append-only SQLite review log with no external action;
- executable unit tests;
- architecture and decision records.

OR-Tools, FastAPI, Pydantic and HTTPX2 are pinned. PostgreSQL was deliberately
deferred in favor of SQLite for the single-user local POC; the Vue interface is the
next Bolt.

## First demonstrable scenario

A 60-minute cancellation touches an adjacent 30-minute opening. Three synthetic wait requests are evaluated:

- FIFO selects a 30-minute request.
- Local best-fit selects a 75-minute request.
- A third request is excluded because its required room is unavailable.

This scenario proves contracts and explanations. It does not prove that the future optimizer is better.

## Run

Requires `uv` and an installed Python 3.12 interpreter.

```bash
make test
make api-test
make review-test
make api-smoke
make demo
make multi-slot-demo
make generated-demo
make longitudinal-demo
make development-report
make alternative-diagnostic
make exposure-frontier
```

`make demo` runs the fixed teaching fixture. `make multi-slot-demo` shows the
global-assignment counterexample before CP-SAT. `make generated-demo` runs registered
development seed `1101` and prints its provenance, plans and event evaluations.
`make longitudinal-demo` replays three controlled compatible-opportunity rounds
for both baselines. `make development-report` emits the full development-only JSON
comparison. The final frozen evaluation set does not yet exist.

`make alternative-diagnostic` reports post-hoc local capacity among plans tied on
minutes and requests served; it is not a deployable slice-aware strategy.
`make exposure-frontier` measures predeclared local efficiency floors on the fixed
V3 path and carries the same diagnostic-only boundary.

## Stack

- Python 3.12
- FastAPI and Pydantic v2 at the API boundary
- OR-Tools CP-SAT for constraint optimization
- SQLite for local append-only review events; PostgreSQL deferred until justified
- Vue 3, TypeScript and FullCalendar for the visual workflow
- pytest, Hypothesis and Playwright as the project grows
- Docker Compose for the reproducible local environment

## Public claim boundary

This is a reproducible engineering POC using synthetic data. Results will describe only the controlled simulation. They will not be presented as evidence of recovered revenue, reduced no-shows, patient benefit, or production readiness.

## Documentation

- [`specs/README.md`](specs/README.md)
- [`aidlc-docs/requirements.md`](aidlc-docs/requirements.md)
- [`aidlc-docs/execution-plan.md`](aidlc-docs/execution-plan.md)
- [`docs/problem.md`](docs/problem.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/fairness-and-bias-plan.md`](docs/fairness-and-bias-plan.md)
- [`docs/development-evidence.md`](docs/development-evidence.md)
- [`docs/alternative-plan-diagnostic.md`](docs/alternative-plan-diagnostic.md)
- [`docs/exposure-frontier.md`](docs/exposure-frontier.md)
- [`docs/bolts/README.md`](docs/bolts/README.md)
- [`docs/video-storyboard.md`](docs/video-storyboard.md)
- [`docs/adr/0001-modular-monolith-and-baselines.md`](docs/adr/0001-modular-monolith-and-baselines.md)
- [`docs/adr/0002-lexicographic-cp-sat.md`](docs/adr/0002-lexicographic-cp-sat.md)
