# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Construction
- Active Bolt: S3 — multi-slot baselines before the optimizer dependency
- Active spec: `SF-003` — In progress
- Last completed gate: SF-003 design contract moved from Draft to Ready
- External integrations: none
- Real data: prohibited

## Current objective

Implement the visual multi-slot counterexample and generalize both greedy baselines
before adding OR-Tools. The optimizer dependency enters only after those tests are
red and the baseline behavior is understood.

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

Make the multi-slot greedy counterexample executable. Do not add OR-Tools until the
baseline tests demonstrate the global-assignment gap.

The S1 machine-verifiable criteria passed on 2026-10-25. Ricardo explicitly
authorized progression. His teach-back self-assessment remains a non-blocking
learning follow-up, so SF-001 is `Accepted with follow-up`, not `Done`.
