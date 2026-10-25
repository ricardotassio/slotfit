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
