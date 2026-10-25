# Execution plan

## Bolt S1 — deterministic domain and baselines

- Intent: make the first scenario executable without external dependencies.
- Requirements: SF-FR-001, SF-FR-002, SF-FR-003, SF-NFR-001, SF-NFR-003.
- Inputs: accepted problem contract and `demo-1400` fixture.
- Files: domain models, scenario generator, eligibility, strategies, CLI and tests.
- Tests: deterministic replay, FIFO, best-fit, unavailable room and consent.
- Stop conditions: any ambiguity about whether an input is a hard or soft constraint.
- Definition of Done: all S1 exit criteria in `state.md` pass.

## Bolt S2 — complete eligibility vocabulary

- Add provider, duration, room, availability, notice and consent reason codes.
- Add property-oriented invariant tests.
- Separate decision attributes from audit-only operational slice labels.
- Implement identifier and input-order metamorphic tests.
- Do not add optimization yet.

## Bolt S3 — OR-Tools spike

- Add one CP-SAT strategy behind the existing strategy boundary.
- Compare it with baselines on development fixtures.
- Report utilization and fairness dimensions separately.
- Reject configurations that cross predeclared starvation or worst-slice guardrails.
- Record infeasible and timeout behavior.

## Later Bolts

- S4: FastAPI and Pydantic boundary.
- S5: PostgreSQL, runs and idempotent review events.
- S6: Vue/FullCalendar UI.
- S7: frozen simulation, slice analysis, counterfactual tests and evaluation.
- S8: hardening, documentation, evidence-backed video and post.
