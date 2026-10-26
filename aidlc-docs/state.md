# AI-DLC state

- Project: SlotFit
- Repository type: greenfield
- Phase: Construction — cycle 2 (refinement)
- Active Bolt: S15 (SF-015, authorized out of order on 2026-10-26; S11 still next in the cycle-2 order)
- Active spec: SF-015
- Last completed gate: SF-010 clinic-day fixture and explanations (2026-10-26)
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

## Cycle 2 — approved

Ricardo approved the refinement cycle in
[`refinement-plan-2026-10.md`](refinement-plan-2026-10.md) on 2026-10-26 and
authorized SF-009. Decisions D1–D5 are taken as recommended in the plan (D1a no
money, D2a functional labels, D3 remove FullCalendar, D4 English-only UI, D5 S7
stays closed) unless he states otherwise. Units: SF-009 to SF-014, one active at
a time.
