# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Complete — local POC and publication package
- Active Bolt: none
- Active spec: none
- Last completed gate: SF-008 full local verification
- External integrations: none
- Real data: prohibited

## Current objective

No implementation work remains in the current roadmap. External publication,
remote creation and a second independent research line remain separate user-owned
decisions.

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

The project may be published only after real repository/video URLs replace the
explicit placeholders and the user authorizes the external actions. The current
artifacts must retain the terminal no-go and claim boundary.

The S1 machine-verifiable criteria passed on 2026-10-25. Ricardo explicitly
authorized progression. His teach-back self-assessment remains a non-blocking
learning follow-up, so SF-001 is `Accepted with follow-up`, not `Done`.
