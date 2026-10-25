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

## Candidate V2 — exposure-debt iteration

The rejected V1 optimizer remains unchanged and reproducible. V2 adds a
request-level signal derived only from the number of prior compatible opportunities
in which that request was not exposed. Audit-only slice labels remain structurally
unavailable to the optimizer.

V2 uses four integer lexicographic phases:

1. maximize recovered minutes;
2. while fixing phase 1, maximize requests served;
3. while fixing phases 1 and 2, maximize total prior exposure debt served;
4. while fixing phases 1–3, maximize the declared wait-age score.

Debt is a non-negative integer keyed by an active request ID. Missing active IDs
mean zero debt. Unknown IDs and negative values are invalid input. Debt never makes
an ineligible request eligible, never changes a hard constraint and cannot trade
away recovered minutes or requests served. After each controlled round, an
eligible but unexposed request gains one debt unit; an exposed request leaves the
subsequent-round cohort as before.

V2 must pass a focused counterexample in which debt changes only a residual choice,
then run against the same 40 development seeds and unchanged guardrails. V2 cannot
enter calibration unless every development guardrail passes.

### V2 acceptance criteria

- [x] A repeatedly compatible unexposed request gains residual priority without
  reducing recovered minutes or requests served.
- [x] Missing, negative and unknown debt inputs have explicit behavior and tests.
- [x] Audit-only slices remain absent from the optimizer input.
- [x] The same debt state and scenario replay identically.
- [x] The unchanged 40-seed development report accepts or rejects V2 explicitly.

### V2 development decision

V2 is rejected before calibration. Its focused residual-choice test passes, but it
changes zero round-level selections relative to V1 across the 40 registered
development seeds. Consequently its aggregate results equal V1: 96.81% mean
recovered utilization, zero K=3 starvation and a 12.58 percentage-point worst
supported exposure-shortfall degradation, which still fails the 10-point limit.

The next gate is diagnostic, not another objective change: determine whether any
plan with the same recovered minutes and requests served can improve the failing
exposure outcome. If no such plan exists, the project must expose an explicit
efficiency-versus-exposure frontier rather than pretend a residual tie-break can
solve the conflict.

## Alternative-plan diagnostic contract

The diagnostic enumerates feasible assignments from `Scenario` decision data only
and retains every plan tied on the two primary objectives: recovered minutes and
requests served. It must not accept an audit manifest or slice label.

After enumeration, a separate analyzer may join audit-only slices to answer a
counterfactual question: did an efficiency-equivalent plan exist that would have
exposed more requests from a currently underexposed operational slice? This is an
oracle for experiment diagnosis, not an allowed production strategy.

The first diagnostic follows the actual V2 cohort path for five rounds. For each
round it records the number of primary-optimal alternatives and, post hoc, which
slices had a strictly higher exposure count in at least one alternative. It does
not claim that independently attractive round alternatives form a globally optimal
five-round policy.

### Diagnostic acceptance criteria

- [x] Enumeration consumes `Scenario` only and preserves all hard constraints.
- [x] Every returned plan ties the V2 plan on recovered minutes and requests served.
- [x] Audit metadata is joined only after enumeration.
- [x] The 40-seed, five-round diagnostic is deterministic and records support.
- [x] The result determines whether V3 needs a better label-free tie-break or an
  explicit efficiency/exposure frontier.

### Diagnostic decision

Across 200 development rounds, V2 was primary-optimal every time and 34 rounds had
multiple primary-optimal plans. For the failing `notice_band=moderate` slice, 8
rounds contained a local efficiency-equivalent alternative, with 9 additional
exposures of capacity. The immediate next hypothesis is therefore a label-free
placement-scarcity tie-break, not an efficiency sacrifice. See
[`../docs/alternative-plan-diagnostic.md`](../docs/alternative-plan-diagnostic.md).

## Candidate V3 — placement scarcity

V3 preserves V2 and adds a label-free residual phase derived from the current
decision scenario. For each active request, `compatible_interval_count` is the
number of intervals for which the shared eligibility function returns eligible.
The placement-scarcity coefficient is:

`active_interval_count + 1 - compatible_interval_count`

Only requests with at least one eligible pair can receive objective credit. A
request compatible with fewer current intervals therefore receives more residual
credit, but only after recovered minutes, requests served and prior exposure debt
are fixed. Wait age remains the final tie-break.

The five V3 phases are:

1. maximize recovered minutes;
2. maximize requests served at the phase-1 optimum;
3. maximize prior exposure debt served at phases 1–2;
4. maximize placement-scarcity score at phases 1–3;
5. maximize wait-age score at phases 1–4.

Placement scarcity uses no audit label and cannot make an ineligible pair feasible.
It is recomputed for the active scenario in each controlled round.

### V3 acceptance criteria

- [x] A focused residual-choice fixture selects two constrained requests over one
  flexible request without losing minutes or requests served.
- [x] V1 and V2 behavior remain reproducible and separately identified.
- [x] V3 preserves hard constraints, deterministic replay and counterfactual
  invariance.
- [x] The unchanged 40-seed development report explicitly accepts or rejects V3.
- [x] Calibration and final frozen generation remain closed until V3 passes every
  development guardrail.

### V3 development decision

V3 is rejected before calibration. It changed selections in 8 of 40 seeds and 17
of 200 controlled rounds while preserving the same 96.81% mean utilization, 2.700
mean requests served, zero K=3 starvation, zero hard violations and zero
counterfactual flips. The worst supported exposure-shortfall degradation improved
from V2's 12.58 to 12.35 percentage points, but still exceeded the unchanged
10-point limit. The binding slice changed from `notice_band=moderate` to
`duration_band=short`.

Placement scarcity therefore uses some residual capacity but is insufficient. Per
the predeclared diagnostic decision, the next development gate is an explicit
efficiency-versus-exposure frontier, not another ungrounded tie-break.

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
