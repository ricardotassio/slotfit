# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Construction
- Active Bolt: S6 — comparison and simulated-review UI
- Active spec: `SF-006` — Ready
- Last completed gate: SF-005 append-only simulated review verified
- External integrations: none
- Real data: prohibited

## Current objective

Implement the S6 local comparison UI with neutral ordering, accessible fallback
and an explicit rejected-candidate disclosure.

## Exit criteria for S1

- timezone-aware domain values;
- deterministic `demo-1400` scenario;
- explicit eligibility reason codes;
- FIFO result is `WR-001`;
- local best-fit result is `WR-002`;
- `WR-003` is excluded for unavailable room;
- tests run without third-party services;
- Ricardo can explain the model, invariants and baseline trade-off.

## Completed S2 evidence

- versioned deterministic generator and decision checksum;
- disjoint development, calibration, regression and challenge seed registries;
- audit-only operational slices excluded from strategy inputs;
- metamorphic checks for opaque IDs, input order and irrelevant ineligible records;
- event-level evaluation with hard-constraint violation detection;
- deterministic controlled opportunity rounds that produce waiting and
  starvation-threshold inputs without inventing a threshold.

## Next gate

Close SF-006 only after build, real local integration, browser-state,
idempotency and automated accessibility checks pass. Calibration remains closed
and the final frozen set remains nonexistent.

The S1 machine-verifiable criteria passed on 2026-10-25. Ricardo explicitly
authorized progression. His teach-back self-assessment remains a non-blocking
learning follow-up, so SF-001 is `Accepted with follow-up`, not `Done`.
