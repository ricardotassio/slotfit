# SlotFit

SlotFit is an explainable scheduling experiment that studies how a clinic could respond to a cancellation without turning the workflow into opaque automation.

The project compares simple baselines with constraint optimization over entirely synthetic calendars. It never contacts a person, books an appointment, infers clinical urgency, or integrates with a real practice-management system.

## Current status

**AI-DLC Construction Bolt S2 is complete; the S3 optimizer spec is still Draft.**

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
- executable unit tests;
- architecture and decision records.

OR-Tools, FastAPI, PostgreSQL and the Vue interface have not been added yet. They enter in later Bolts after the domain and baselines are understood.

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
make demo
make multi-slot-demo
make generated-demo
make longitudinal-demo
```

`make demo` runs the fixed teaching fixture. `make multi-slot-demo` shows the
global-assignment counterexample before CP-SAT. `make generated-demo` runs registered
development seed `1101` and prints its provenance, plans and event evaluations.
`make longitudinal-demo` replays three controlled compatible-opportunity rounds
for both baselines. The current Bolt uses no third-party runtime dependency.

## Planned stack

- Python 3.12
- FastAPI and Pydantic v2 at the API boundary
- OR-Tools CP-SAT for constraint optimization
- PostgreSQL for runs and append-only review events
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
- [`docs/video-storyboard.md`](docs/video-storyboard.md)
- [`docs/adr/0001-modular-monolith-and-baselines.md`](docs/adr/0001-modular-monolith-and-baselines.md)
- [`docs/adr/0002-lexicographic-cp-sat.md`](docs/adr/0002-lexicographic-cp-sat.md)
