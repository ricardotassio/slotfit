# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Construction
- Active Bolt: S3 — multi-slot optimizer and development evaluation
- Active spec: `SF-003` — In progress
- Last completed gate: 40-seed development evidence reviewed; first candidate rejected
- External integrations: none
- Real data: prohibited

## Current objective

Revise the candidate policy to address the failed supported-slice exposure
guardrail without changing the threshold or using audit-only slices as inputs.

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

Specify and test a minimal per-request exposure-debt signal, then rerun the same
40 development seeds. Calibration remains closed until all development guardrails
pass. The final frozen set remains nonexistent.

The S1 machine-verifiable criteria passed on 2026-10-25. Ricardo explicitly
authorized progression. His teach-back self-assessment remains a non-blocking
learning follow-up, so SF-001 is `Accepted with follow-up`, not `Done`.
