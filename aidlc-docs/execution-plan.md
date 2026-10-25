# Execution plan

Cards pedagógicos e operacionais de todos os Bolts:
[`../docs/bolts/README.md`](../docs/bolts/README.md).

## Bolt S1 — deterministic domain and baselines

- Intent: make the first scenario executable without external dependencies.
- Requirements: SF-FR-001, SF-FR-002, SF-FR-003, SF-NFR-001, SF-NFR-003.
- Inputs: accepted problem contract and `demo-1400` fixture.
- Files: domain models, scenario generator, eligibility, strategies, CLI and tests.
- Tests: deterministic replay, FIFO, best-fit, unavailable room and consent.
- Stop conditions: any ambiguity about whether an input is a hard or soft constraint.
- Definition of Done: all S1 exit criteria in `state.md` pass.

## Bolt S2 — complete eligibility vocabulary

- Status: complete on 2026-10-25.
- Added provider, duration, room, availability, notice and consent reason codes.
- Added property-oriented invariant and mutation-sentinel tests.
- Separated decision attributes from audit-only operational slice labels.
- Implemented identifier and input-order metamorphic tests.
- Added event and controlled longitudinal evaluation inputs without adding an
  optimizer or inventing a starvation threshold.

## Bolt S3 — OR-Tools spike

- Add one CP-SAT strategy behind the existing strategy boundary.
- Compare it with baselines on development fixtures.
- Report utilization and fairness dimensions separately.
- Reject configurations that cross predeclared starvation or worst-slice guardrails.
- Record infeasible and timeout behavior.

## Bolt S7 gate outcome

- Status: closed without execution.
- Reason: no SF-003 candidate passed the fixed development guardrails, so
  calibration and configuration freeze never opened.
- Consequence: the 400-seed final set remains intentionally nonexistent and no
  final-effect claim is allowed.

## Later Bolts

- S4: FastAPI and Pydantic boundary.
- S5: PostgreSQL, runs and idempotent review events.
- S6: Vue/FullCalendar UI.
- S7: frozen simulation gate closed without execution; no candidate was eligible.
- S8: hardening, documentation, evidence-backed video and post.

Os itens S4–S8 são contratos de roadmap. Seus cards descrevem Definition of Ready,
Definition of Done, riscos e alternativas, mas não constituem evidência de
implementação.
