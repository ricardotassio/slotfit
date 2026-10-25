# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Construction
- Active Bolt: none — preparing the S3 decision gate
- Active spec: none; `SF-003` remains Draft
- Last completed gate: S2 generated scenarios and fairness-control evidence
- External integrations: none
- Real data: prohibited

## Current objective

Resolve the bounded optimizer experiment before adding OR-Tools: choose a
development-only threshold method, solver runtime, objective units and output
artifact contract without inspecting frozen-test outcomes.

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
- disjoint development, calibration, frozen-test and challenge seed registries;
- audit-only operational slices excluded from strategy inputs;
- metamorphic checks for opaque IDs, input order and irrelevant ineligible records;
- event-level evaluation with hard-constraint violation detection;
- deterministic controlled opportunity rounds that produce waiting and
  starvation-threshold inputs without inventing a threshold.

## Next gate

Move `SF-003` from `Draft` to `Ready` only after its five unresolved acceptance
criteria are explicit. Do not add OR-Tools before that spec gate closes.

The S1 machine-verifiable criteria passed on 2026-10-25. Ricardo explicitly
authorized progression. His teach-back self-assessment remains a non-blocking
learning follow-up, so SF-001 is `Accepted with follow-up`, not `Done`.
