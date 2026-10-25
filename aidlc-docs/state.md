# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Construction
- Active Bolt: none — S7 gate closed; S8 hardening is next
- Active spec: none
- Last completed gate: SF-007 not executed because eligibility failed
- External integrations: none
- Real data: prohibited

## Current objective

Specify S8 hardening and bilingual evidence-based communication around the real
terminal no-go. Do not publish or push anything.

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

Open S8 only with explicit reproducibility, claim-review, threat/risk, bilingual
script and publication-draft criteria. Publishing remains outside authorization.

The S1 machine-verifiable criteria passed on 2026-10-25. Ricardo explicitly
authorized progression. His teach-back self-assessment remains a non-blocking
learning follow-up, so SF-001 is `Accepted with follow-up`, not `Done`.
