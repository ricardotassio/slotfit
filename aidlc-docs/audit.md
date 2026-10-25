# AI-DLC audit

## 2026-10-25 — Repository inception

- Created as a separate local Git repository.
- Public target: vendor-neutral scheduling experiment.
- Decision: build SlotFit before SafeHandoff Lab.
- Decision: no remote repository or publication in this stage.
- Decision: use a modular monolith and keep the domain independent from frameworks.
- Decision: implement FIFO and best-fit before OR-Tools.
- Decision: use standard-library dataclasses in the first domain Bolt; Pydantic enters at the API boundary.
- Decision: no ML, LLM, message delivery or real scheduling integration.

## 2026-10-25 — Fairness and public narrative contract

- Decision: synthetic data will be used to expose assumptions and test invariants, not to claim absence of bias.
- Decision: fairness is operationally scoped to repeated exclusion across duration, availability, resource need, wait age and notice requirement.
- Decision: demographic fairness is outside the evidence boundary of the synthetic POC.
- Decision: decision attributes and audit-only slice labels remain separate.
- Decision: utilization gains cannot override hard constraints or predeclared starvation and worst-slice guardrails.
- Decision: objective weights and guardrails are frozen before the final test run.
- Decision: the video must show one failed or rejected case and state the human decision boundary.
- Evidence plan: [`../docs/fairness-and-bias-plan.md`](../docs/fairness-and-bias-plan.md) and [`../docs/video-storyboard.md`](../docs/video-storyboard.md).

## Open decisions

- Exact numerical fairness guardrails after inspecting only the development distribution.
- OR-Tools objective weights before the frozen test set.
- Public repository license before publication.

## 2026-10-25 — Cross-agent specification workflow

- Decision: `AGENTS.md` is the canonical repository instruction file for Codex and Claude Code.
- Decision: `CLAUDE.md` imports `AGENTS.md` rather than duplicating project rules.
- Decision: specs under `specs/` own bounded implementation contracts; AI-DLC files own lifecycle state and traceability.
- Decision: read-only spec, risk and test reviewer roles are available in both agent environments.
- Decision: no model is pinned in repository configuration; the active environment chooses an available model.
- Decision: SF-001 initially remained in verification until progression was
  explicitly authorized; the teach-back remains recorded rather than silently
  treated as complete.

## 2026-10-25 — S1 progression and SF-002 implementation

- Decision: accept S1 for progression with a non-blocking personal teach-back
  follow-up; do not label it `Done`.
- Decision: use SHA-256-derived deterministic choices instead of a runtime random
  number generator so replay depends only on seed, version and field identity.
- Decision: register disjoint development, calibration, frozen-test and challenge
  seed sets before optimizer work.
- Decision: keep operational audit slices in the manifest and outside `Scenario`,
  which is the strategy input.
- Decision: join audit metadata only in `slotfit.evaluation`, after a plan exists.
- Decision: report invalid selections as hard-constraint violations.
- Decision: do not emit simulated waiting or starvation from a single event. A
  longitudinal model is required before those measurements are meaningful.
- Decision: model repeated exposure as deterministic compatible-opportunity rounds,
  not as elapsed patient time or a real clinic calendar.
- Decision: remove a plan-exposed request before the next controlled round so one
  synthetic identity cannot receive repeated objective credit.
- Decision: emit compatible opportunities missed and first exposure round, but do
  not choose a starvation threshold inside SF-002.
- Decision: use registered development seed `1101` for the demonstrable generated
  and longitudinal examples; do not use frozen-test outcomes for configuration.
