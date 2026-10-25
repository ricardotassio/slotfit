# SF-003 — Multi-slot optimizer and controlled evaluation

- Status: In progress
- AI-DLC mapping: Bolts S3 and S7
- Depends on: SF-002
- Dependency boundary: pin `ortools==9.15.6755` only after the multi-slot
  baseline tests are red

## Experimental question

Can a constraint strategy recover more usable time than FIFO and local best-fit
across interacting open intervals without violating hard constraints or
predeclared repeated-exclusion guardrails?

The optimizer is justified only by a global assignment conflict: a flexible
request can consume the only interval available to a constrained request. A
single interval is not sufficient evidence for CP-SAT.

## First visual scenario

Use two non-overlapping openings and two feasible requests:

- `OPEN-A`: 60 minutes;
- `OPEN-B`: 60 minutes;
- an older flexible 60-minute request can use either opening;
- a 60-minute request can use only `OPEN-A`.

Both chronological greedy baselines place the older flexible request in `OPEN-A`
because duration also ties, then cannot place the constrained request in `OPEN-B`.
They recover 60 minutes. A global assignment can place the constrained request in
`OPEN-A` and the flexible request in `OPEN-B`, recovering 120 minutes. This is a
controlled counterexample, not a performance claim.

## Implementation slices

1. Extend FIFO and best-fit to multiple intervals, preserving their declared
   greedy policies and preventing duplicate request assignment.
2. Add CP-SAT behind the same `Scenario -> CandidatePlan` boundary.
3. Generate versioned multi-slot development scenarios and event records.
4. Run development and calibration analysis; freeze configuration and guardrails.
5. Mint a new frozen manifest and run it once for the final report.

## Hard constraints

- create a binary assignment variable only for an eligible request/interval pair;
- at most one request per open interval;
- at most one interval per request;
- assigned duration must fit the interval;
- provider, room, availability, notice and consent remain mandatory;
- a plan must never contact a person or modify an external schedule.

No hard constraint may become a penalty term.

## Objective contract

Use three integer, lexicographic phases rather than a blended score:

1. maximize recovered minutes;
2. while fixing phase 1's optimum, maximize requests served;
3. while fixing phases 1 and 2, maximize the declared wait-age score
   `request_count + 1 - joined_order`.

The wait-age coefficient range is therefore `1..request_count` and is used only
after efficiency and request count are fixed. There are no tunable objective
weights in SF-003. Residual ties use model construction ordered by
`joined_order`, interval start and interval position—not opaque identifiers—and
must pass the identifier counterfactual test.

## Solver contract

- package: `ortools==9.15.6755`, recorded in the lockfile;
- `num_workers = 1`;
- `random_seed = 1`;
- `max_deterministic_time = 0.25` per phase;
- `max_time_in_seconds = 1.0` per phase as a defensive wall-clock ceiling;
- `log_search_progress = false` in normal runs;
- all three phases must return `OPTIMAL` before the plan is called optimized;
- `FEASIBLE`, `INFEASIBLE`, `MODEL_INVALID` and `UNKNOWN` remain distinct output
  statuses;
- no baseline fallback may be reported under the CP-SAT strategy name.

The limits are POC engineering bounds, not production latency claims. They will be
reported together with observed wall time and solver status.

## Guardrail-selection method

Only the multi-slot development set may shape a configuration. Calibration may
confirm a frozen choice but may not tune it. Regression detects code changes. The
final frozen set does not exist until every item below is committed.

Predeclared controlled policy:

- simulate five compatible-opportunity rounds per seed;
- define a starvation event as three compatible opportunities without plan
  exposure (`K = 3`);
- report sensitivity for `K = 2` and `K = 4`, but never change the pass/fail value
  after calibration;
- require zero hard-constraint violations and zero opaque-ID flips;
- require the candidate median starvation-event rate to be no more than five
  percentage points above the better baseline;
- require each supported operational slice's exposure-rate gap from the overall
  rate to be no more than ten percentage points worse than the better baseline;
- call a slice supported only when it has at least 30 eligible opportunities;
  unsupported slices are reported, never merged or silently discarded;
- reject the strategy when a guardrail fails even if utilization improves.

These thresholds are experiment tolerances, not clinical fairness standards. The
report must show absolute results for both baselines so “better baseline” cannot
hide a weak reference point.

## Evaluation sets and uncertainty

- development: 40 new multi-slot seeds;
- calibration: 40 new multi-slot seeds;
- regression: 20 visible engineering seeds;
- challenge: explicit adversarial fixtures;
- final frozen: 400 seeds minted only after configuration freeze.

The final seed is the unit of analysis. Four hundred independent scenario seeds
bound the worst-case 95% margin of error for a binary scenario-level rate to about
4.9 percentage points (`1.96 * sqrt(0.25 / 400)`). Report paired differences and
95% bootstrap intervals by seed; do not treat requests within one seed as
independent samples.

## Required comparison

All strategies consume identical decision manifests. Report separately:

- hard-constraint violations;
- recovered utilization and paired difference;
- requests served;
- plan exposure by operational slice;
- median and p90 compatible opportunities missed before first exposure;
- starvation-event rate at `K = 3` plus sensitivity at `K = 2` and `K = 4`;
- worst supported slice and gap from the overall result;
- opaque-ID and input-order flips;
- runtime, phase status and objective value.

## Artifact contract

Each run writes an immutable directory keyed by a configuration checksum:

- `manifest.json`: schema, code revision, Python/OR-Tools versions, generator and
  distribution versions, split, seeds, solver configuration, guardrails and input
  checksums;
- `scenario-results.jsonl`: one scenario/strategy record with assignments,
  exclusions, objective phases, utilization, violations, runtime and status;
- `slice-summary.json`: support, exposure, compatible misses, starvation events,
  worst-slice gaps and uncertainty intervals;
- `decision.json`: every guardrail's observed value, limit and pass/fail result.

Artifact creation must fail closed on schema, checksum or provenance mismatch.
Timestamps may describe execution but never participate in replay identity.

## Rejection conditions

- any hard-constraint violation;
- opaque-identifier or irrelevant-order counterfactual flip;
- threshold or objective changed after calibration or frozen-manifest creation;
- a utilization gain that crosses a starvation or worst-slice guardrail;
- unexplained infeasible, limit, invalid-model or fallback behavior;
- gain visible only in one convenient seed or distribution;
- treating `FEASIBLE` as proven optimal.

## Acceptance criteria

- [x] Development-only guardrail method and thresholds are explicit.
- [x] Maximum runtime and deterministic solver configuration are explicit.
- [x] Objective phases, units and coefficient range are explicit.
- [x] Frozen size has a scenario-level uncertainty justification.
- [x] Output artifact and comparison schemas are explicit.
- [x] Multi-slot counterexample fails under at least one greedy baseline.
- [x] Multi-slot baselines preserve hard constraints and never assign a request twice.
- [x] CP-SAT returns the global 120-minute plan with three `OPTIMAL` phases.
- [x] Counterfactual, status and deterministic-limit tests pass.
- [x] Development evidence is reviewed before configuration freeze.
- [ ] Final frozen manifest is created only after the freeze commit.

## First development decision

The first candidate is rejected before calibration. Across 40 development seeds it
recovered 96.81% mean utilization with zero hard violations, zero opaque-ID flips,
zero input-order flips and zero K=3 starvation events. It nevertheless increased
the worst supported exposure shortfall by 12.58 percentage points relative to the
better supported baseline, exceeding the fixed 10-point limit. The failing slice
was `notice_band=moderate`.

For the slice gate, signed exposure gaps are retained in output, but negative gaps
are clamped to zero for the pass/fail shortfall comparison. Only baseline slice
observations with at least 30 eligible opportunities may serve as references.
Unsupported results remain reported. Full evidence and the next hypothesis are in
[`../docs/development-evidence.md`](../docs/development-evidence.md).

## Red, green, refactor

- Red: add the multi-slot counterexample and duplicate-assignment tests before
  changing a strategy.
- Green: generalize the baselines without importing OR-Tools.
- Red: add the global-plan and explicit-status tests while OR-Tools is absent.
- Green: add the smallest CP-SAT adapter that satisfies the solver contract.
- Refactor: centralize plan validation and artifact serialization without changing
  results.
- Verify: focused tests, `make test`, counterfactual suite and development-only
  report.

## Public evidence boundary

The final result may report measured controlled behavior on the versioned synthetic
benchmark. It may not claim clinic impact, access improvement, revenue recovery,
patient benefit, demographic fairness or production readiness.

## Primary references

- [Google OR-Tools CP-SAT status contract](https://developers.google.com/optimization/cp/cp_solver)
- [Google OR-Tools assignment/scheduling example](https://developers.google.com/optimization/scheduling/employee_scheduling)
- [OR-Tools SAT parameter definitions](https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto)
- [OR-Tools 9.15.6755 package metadata](https://pypi.org/project/ortools/9.15.6755/)
