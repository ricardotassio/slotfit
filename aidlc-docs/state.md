# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Construction
- Active Bolt: S1 — deterministic domain and first synthetic scenario
- Active spec: `SF-001` — Verification
- Last completed gate: problem contract and baseline definition
- External integrations: none
- Real data: prohibited

## Current objective

Prove that the same synthetic scenario can be represented, replayed and evaluated by two simple strategies before adding an optimizer.

## Exit criteria for S1

- timezone-aware domain values;
- deterministic `demo-1400` scenario;
- explicit eligibility reason codes;
- FIFO result is `WR-001`;
- local best-fit result is `WR-002`;
- `WR-003` is excluded for unavailable room;
- tests run without third-party services;
- Ricardo can explain the model, invariants and baseline trade-off.

## Next gate

Review S1 and perform the teach-back before Bolt S2 expands eligibility rules.

The machine-verifiable S1 criteria passed on 2026-10-25. The remaining gate is the human teach-back and review-log closure; `SF-002` is specified but not active.
