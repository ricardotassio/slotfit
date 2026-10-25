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

- Public repository license before publication.

## 2026-10-25 — SF-003 design gate

- Decision: CP-SAT is justified only by a multi-slot global assignment conflict,
  not by the original single-interval example.
- Decision: pin `ortools==9.15.6755` when the dependency enters.
- Decision: use lexicographic recovered-minutes, requests-served and wait-age
  phases; do not use a blended tunable score.
- Decision: keep repeated-exclusion guardrails outside the first solver objective.
- Decision: define a controlled starvation event at three compatible opportunities
  without plan exposure and report sensitivity at two and four.
- Decision: use one worker, fixed seed, deterministic-time bound and wall-time
  ceiling; require `OPTIMAL` in every phase for an optimized claim.
- Decision: mint 400 final frozen seeds only after configuration and guardrails are
  committed. Previously exercised seeds remain regression-only.
- Evidence: the dependency entered only after the multi-slot baseline tests failed
  and then passed independently; Python is pinned to 3.12 and OR-Tools to
  `9.15.6755`.

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
- Decision: register disjoint development, calibration, regression and challenge
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
- Correction: the `3101`–`3104` seeds were exercised in routine engineering tests,
  so they are regression seeds, not a valid final frozen set. The real frozen
  manifest will be minted only after SF-003 configuration and guardrails are
  immutable.

## 2026-10-25 — SF-003 development decision

- Decision: operationalize an exposure deficit as `max(overall exposure - slice
  exposure, 0)` while retaining the signed gap in report output.
- Decision: a baseline slice may influence pass/fail only when it independently
  meets the predeclared support of 30 eligible opportunities.
- Decision: reject the first CP-SAT candidate because its worst supported
  exposure-shortfall degradation is 12.58 percentage points, above the unchanged
  10-point limit.
- Decision: do not enter calibration, freeze configuration or mint final seeds.
- Next hypothesis: use per-request compatible-opportunity debt, never audit-only
  slice labels, to make the longitudinal policy exposure-aware.

## 2026-10-25 — Bolt card catalog

- Decision: document S1–S8 with a common learning-card contract covering purpose,
  mechanics, critical complexity assessment, evidence/DoD and interview defense.
- Decision: distinguish implemented evidence (S1–S3) from roadmap contracts
  (S4–S8); a future card never implies existing functionality.
- Decision: keep the cards under `docs/bolts/` and link the catalog from the README
  and the canonical execution plan.
- Verification: all relative links resolve, `git diff --check` passes and the
  unchanged implementation suite remains at 46 passing tests.

## 2026-10-25 — Exposure-debt V2 decision

- Decision: preserve V1 and identify V2 separately rather than rewriting historical
  evidence.
- Decision: exposure debt is request-level compatible misses only; no audit slice
  may enter the optimizer.
- Observation: V2 changed zero selections across 40 development seeds and did not
  improve the failed slice guardrail.
- Decision: reject V2 and diagnose the efficiency/exposure feasible frontier before
  adding another objective or changing its priority.

## 2026-10-25 — Primary-optimal alternative diagnosis

- Decision: enumerate primary-optimal assignments from decision data before joining
  audit slices, preserving the decision/audit boundary.
- Observation: 34 of 200 rounds have residual primary-optimal choice; the failing
  moderate-notice slice has 9 local additional exposures of capacity.
- Limitation: local alternatives along the V2 cohort path are not a globally
  optimized longitudinal policy.
- Decision: test placement scarcity as a label-free V3 residual signal before
  allowing any efficiency trade-off.
- Verification: 57 tests passed and the standalone diagnostic JSON was generated
  and parsed successfully.

## 2026-10-25 — Placement-scarcity V3 decision

- Decision: compute scarcity from current eligible interval counts, never from an
  audit slice label.
- Observation: V3 changes 17 of 200 rounds and improves the worst degradation by
  0.23 percentage point while preserving primary efficiency.
- Decision: reject V3 because 12.35 p.p. remains above the 10 p.p. guardrail.
- Next gate: measure an explicit development-only efficiency/exposure frontier;
  do not add another residual heuristic without evidence.
