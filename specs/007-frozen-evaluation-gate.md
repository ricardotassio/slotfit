# SF-007 — Frozen evaluation eligibility gate

- Status: Closed — not executed by design
- AI-DLC mapping: Bolt S7
- Depends on: SF-003

## Gate question

Is there a candidate that passed every fixed development guardrail, was frozen,
and then passed calibration without tuning?

## Observed answer

No. V1–V4 each failed the unchanged worst-supported-slice degradation limit on
the 40-seed development set. Calibration never opened, no configuration freeze
commit exists and no final frozen seed manifest was minted.

## Required action

Do not run a 400-seed final evaluation. Doing so would spend the held-out evidence
on a rejected configuration and invite post-result selection. The absence of a
final report is the correct gate outcome, not missing implementation.

## Evidence

- SF-003 terminal decision and four candidate results;
- `docs/methodology-no-go-review.md`;
- API/UI fields `candidate_accepted: false`, `calibration_open: false` and
  `final_frozen_set_exists: false`;
- tests that preserve those fields in the user-visible evidence flow.

## Reopening rule

Only a new research specification may reopen S7. It must define a materially new
hypothesis, fresh development/calibration registries and thresholds before results
are observed. It may not rename V4, reuse the current development set for tuning or
silently relax the 10 percentage-point limit.

## Acceptance criteria

- [x] Development decision is terminal and traceable.
- [x] Calibration remains closed.
- [x] No accepted configuration or freeze commit is claimed.
- [x] Final frozen manifest remains nonexistent.
- [x] UI and publication materials disclose the no-go.
- [x] Reopening requires a new independent research contract.

