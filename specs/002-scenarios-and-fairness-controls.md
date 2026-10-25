# SF-002 — Scenario generation and fairness controls

- Status: Done
- AI-DLC mapping: Bolt S2 and the evaluation foundation for S7
- Depends on: SF-001

## Problem

The fixed fixture cannot expose instability, repeated exclusion or strategy behavior across different operational conditions. The next increment must create reproducible variation and measure declared risks before adding an optimizer.

## In scope

- a deterministic generator whose seed changes generated content;
- versioned generation configuration and manifest;
- operational audit slices for duration, availability width, resource scarcity, wait age and notice requirement;
- strict separation between model-visible decision attributes and audit-only slice metadata;
- stable eligibility vocabulary for provider, duration, room, availability, notice and consent;
- metamorphic and property-oriented tests;
- baseline evaluation records suitable for later aggregation.

## Non-goals

- demographic or clinical fairness claims;
- real data;
- objective-weight tuning;
- OR-Tools, API, database or UI;
- a single combined “fairness score.”

## Data contract

Every generated scenario records:

- scenario and generator version;
- seed;
- distribution configuration identifier;
- decision inputs;
- audit-only slice labels;
- expected challenge property;
- creation timestamp only when it does not affect replay equality.

Audit-only labels must not be accepted by an eligibility or strategy function.

## Required invariants

1. Same seed, generator version and configuration reproduce identical decision content.
2. At least two approved seeds generate different decision content.
3. Replacing opaque identifiers does not change selected positions or recovered minutes.
4. Reordering requests does not change the plan unless an explicit, documented tie-breaker applies.
5. Adding an ineligible request does not change assignments.
6. Duplicating a request cannot create duplicate assignments or objective credit.
7. Every exclusion has one or more stable reason codes.

## Acceptance criteria

- [x] Generation configuration has an explicit schema and version.
- [x] Development, calibration, regression and challenge seed registries are distinct; the final frozen registry is intentionally not minted yet.
- [x] Slice metadata is structurally unavailable to strategy scoring.
- [x] Required invariants have executable tests, including a mutation sentinel that exposes lexical identifier leakage.
- [x] FIFO and best-fit run on all registered scenarios without hard-constraint violations.
- [x] Evaluation emits selection, exposure, compatible-opportunity waiting, starvation-threshold, recovered-utilization and worst-slice inputs separately.
- [x] Thresholds remain `TBD` until development evidence exists; future frozen-test results cannot set them.

## Red, green, refactor

- Red: add the same-seed/different-seed and opaque-identifier invariance tests.
- Green: implement the smallest versioned generator and decision/audit data separation that passes them.
- Refactor: centralize manifest construction without changing generated behavior.
- Verify: run focused generator tests, `make test`, and a replay command over at least two seeds.

## Bias-risk review

The risk reviewer must verify proxy risk, leakage, distribution imbalance, tie-break behavior and the absence of demographic claims. A finding that audit-only data reaches a strategy is blocking.

## Exit and handoff

SF-002 is done only when replay, invariance and evaluation-record evidence are committed. It then enables the bounded optimizer spike in SF-003.

## Observed evidence

- Red: `tests.test_generation_and_invariance` initially failed because the
  generator module did not exist.
- Green: deterministic generation, disjoint split seeds, audit-data separation,
  identifier/order/ineligible-record invariants and duplicate rejection pass.
- Red: `tests.test_evaluation` initially failed because the evaluation module did
  not exist.
- Green: event-level records expose eligibility opportunity, selection, recovered
  utilization and hard-constraint violations after planning.
- Red: `tests.test_longitudinal` initially failed because the longitudinal module
  did not exist.
- Green: controlled opportunity rounds preserve request identity, remove exposed
  requests and count compatible opportunities missed before exposure.
- Mutation evidence: the opaque-ID counterfactual reverses lexical identifiers and
  proves that a deliberately broken identifier-based policy flips its decision.
- Evaluation-set integrity: seeds exercised during engineering are labelled
  `regression`, never `frozen-test`. The final frozen registry will be created only
  after the SF-003 objective and guardrails are immutable.
- Honest limitation: opportunity counts are inputs, not elapsed patient wait. No
  request is labelled `starved` until a development-only threshold is proposed,
  reviewed and frozen.
