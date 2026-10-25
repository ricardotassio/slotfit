# Review and teach-back log

## 2026-10-25 — SF-001 verification evidence

- `make test`: 5 tests passed.
- `make demo`: FIFO selected `WR-001` and recovered 30 minutes.
- `make demo`: local best-fit selected `WR-002` and recovered 75 minutes.
- `WR-003` was excluded with `REQUIRED_ROOM_UNAVAILABLE`.
- The fixture seed is not yet a population generator; this limitation is explicit in `SF-001` and `SF-002`.
- Ricardo explicitly authorized progression on 2026-10-25 after receiving the
  conceptual answers. S1 is accepted for progression but not marked `Done` because
  the personal teach-back self-assessment remains open.

## Required S1 teach-back

Ricardo should be able to answer:

1. Why is FIFO necessary even if it is intentionally simple?
2. Which fields are hard constraints in the current model?
3. Why does best-fit select `WR-002`?
4. Why is `WR-003` excluded?
5. What is still missing before OR-Tools can be justified?

## 2026-10-25 — SF-002 implementation evidence

- Initial generator test run failed with `ModuleNotFoundError` for
  `slotfit.generation`.
- Initial evaluation test run failed with `ModuleNotFoundError` for
  `slotfit.evaluation`.
- The generator records schema, generator, distribution, split, seed, challenge
  property and decision checksum.
- Development, calibration, regression and challenge seeds are disjoint.
- Audit slices are joined only by the evaluator after a strategy returns a plan.
- Registered scenarios run through FIFO and best-fit with zero detected
  hard-constraint violations.
- Event records intentionally omit wait and starvation: the current single-event
  model cannot measure them honestly.

## 2026-10-25 — SF-002 completion

- `make test`: 24 tests passed.
- `make generated-demo`: development seed `1101` emitted two baseline plans, two
  event evaluations and `automatic_action: none`.
- `make longitudinal-demo`: three opportunity rounds ran for both baselines.
- FIFO recovered `[60, 75, 30]` minutes across the controlled rounds; local
  best-fit recovered `[75, 60, 60]`. These are fixture observations, not aggregate
  superiority claims.
- After three rounds, FIFO left `WR-002` unexposed after three compatible
  opportunities; best-fit left `WR-001` unexposed after three. This is precisely
  the input a later starvation threshold will evaluate, not a starvation label.
- Every registered split seed ran through both baselines without a detected hard
  constraint violation.
- SF-002 is complete. SF-003 remains blocked by its documented design decisions,
  not by missing code.
- The seeds initially named `frozen-test` were exercised by engineering checks and
  reclassified as `regression`. No final frozen set exists yet.

## 2026-10-25 — SF-003 multi-slot baseline

- Initial focused test failed because `multi_slot_counterexample` did not exist.
- Both baselines now evaluate every request/interval pair chronologically and
  prevent duplicate request or interval assignment.
- In the refined visual counterexample, both openings and requests last 60 minutes.
  FIFO and local best-fit choose the older flexible request for `OPEN-A`, then
  cannot place the constrained request in `OPEN-B`; each recovers 60 of 120 minutes.
- Reversing input interval order does not change either plan.
- `make test`: 29 tests passed before adding OR-Tools.

## 2026-10-25 — SF-003 CP-SAT adapter

- The optimizer test initially failed because `slotfit.optimizer` did not exist.
- Runtime is pinned to Python 3.12 and `ortools==9.15.6755` in `uv.lock`.
- Both greedy strategies recover 60 of 120 minutes in the refined global-conflict
  fixture; CP-SAT recovers 120 minutes.
- CP-SAT returns three `OPTIMAL` phases with objective values `120`, `2` and `3`.
- Opaque identifier and input-order counterfactuals preserve assignment positions.
- A deliberately tiny deterministic-time budget returns `UNKNOWN`, an empty CP-SAT
  plan and `optimized: false`; no baseline fallback is disguised as an optimizer.
- `automatic_action` remains `none`.

## 2026-10-25 — SF-003 first development review

- Added a deterministic three-interval, ten-request generator with 40 development,
  40 calibration, 20 regression and 10 challenge seeds. No final frozen seeds were
  created.
- Compared FIFO, local best-fit and CP-SAT across all 40 development seeds and five
  compatible-opportunity rounds per seed.
- Mean recovered utilization was 72.01% for FIFO, 76.46% for local best-fit and
  96.81% for CP-SAT. Mean requests served were 2.200, 2.275 and 2.700.
- CP-SAT produced zero hard-constraint violations, zero opaque-ID flips, zero
  input-order flips, 40 optimized runs and a 0.00% K=3 starvation-event rate.
- The candidate failed the supported-slice guardrail: its largest exposure-shortfall
  degradation was 12.58 percentage points for `notice_band=moderate`, above the
  predeclared 10-point limit.
- The candidate is rejected before calibration. The threshold was not changed.
- Focused comparison tests: 7 passed. Final `make test`: 46 tests passed.
- The development JSON report was generated and parsed successfully; compile and
  whitespace checks passed.

## 2026-10-25 — SF-003 exposure-debt V2

- Preserved V1 and added a separate `cp-sat-exposure-debt@0.2.0` candidate.
- V2 adds a non-negative per-request compatible-miss debt after recovered minutes
  and requests served, before wait age; audit-only slices are not accepted.
- A focused counterexample proves debt can change a residual choice without losing
  minutes or requests served.
- Across the same 40 development seeds, V2 changed zero longitudinal selections
  relative to V1 and reproduced the same aggregate metrics.
- V2 therefore remains rejected at 12.58 p.p. exposure-shortfall degradation vs
  the unchanged 10 p.p. guardrail. Calibration remains closed.
- Final verification: 52 tests passed; compile, JSON parsing and whitespace checks
  passed.

## 2026-10-25 — SF-003 alternative-plan diagnostic

- Added a bounded enumerator that consumes `Scenario` only and retains plans tied
  on recovered minutes and requests served.
- Joined operational slices only after enumeration for counterfactual diagnosis.
- V2 was primary-optimal in all 200 development rounds; 34 rounds had multiple
  primary-optimal plans.
- `notice_band=moderate` had efficiency-equivalent local improvements in 8 rounds,
  with 9 additional exposures of capacity.
- Decision: test decision-derived placement scarcity before constructing a frontier
  that sacrifices efficiency.
- Final verification: 57 tests passed; the diagnostic JSON parsed successfully;
  compile and whitespace checks passed.

## 2026-10-25 — SF-003 placement-scarcity V3

- Added a separate `cp-sat-placement-scarcity@0.3.0` candidate while preserving V1
  and V2.
- Placement scarcity is derived only from eligible interval counts and acts after
  minutes, requests served and exposure debt.
- V3 changed 17 rounds across 8 development seeds without changing utilization or
  requests served.
- Worst supported degradation improved from 12.58 to 12.35 p.p. but still failed
  the unchanged 10 p.p. guardrail; the binding slice became `duration_band=short`.
- Decision: reject V3 and construct the development-only efficiency/exposure
  frontier. Calibration remains closed.
- Final verification: 58 tests passed; the V3 development JSON parsed and reported
  the expected rejected decision.

## 2026-10-25 — SF-003 local efficiency/exposure frontier

- Predeclared local recovered-minute floors: 100%, 95%, 90% and 80%; target fixed
  to V3's binding `duration_band=short` slice.
- 100% and 95% reproduced the 12.35 p.p. failure.
- The 90% local floor selected 7,905 of 7,950 optimal aggregate minutes (99.43%),
  preserved 168 requests served and reduced target degradation to 8.24 p.p.
- Limitation: oracle choices use the audit slice post hoc and do not change later
  V3 cohorts; this is local capacity, not policy evidence.
- Decision: authorize only a label-free V4 development hypothesis with a 90%
  per-round recovered-minute floor. Calibration remains closed.
- Final verification: 61 tests passed; the frontier JSON parsed successfully;
  compile and whitespace checks passed.

## 2026-10-25 — SF-003 bounded-recovery V4

- Added a separate `cp-sat-bounded-recovery@0.4.0` candidate with a fixed 90%
  per-round recovery floor derived from the predeclared frontier.
- A focused test proves debt can select a lower-minute plan only inside the floor;
  invalid floors fail closed.
- V4 reached 95.71% mean utilization, preserved 2.700 mean requests served and
  retained zero K=3 starvation, hard violations and counterfactual flips.
- Worst supported degradation improved to 10.80 p.p. but remained above 10 p.p.;
  V4 is rejected and calibration remains closed.
- Decision: conduct a methodology/no-go review before any V5.
- Final verification: 63 tests passed; the V4 development JSON parsed successfully;
  compile and whitespace checks passed.
