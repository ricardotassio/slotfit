# SF-003 methodology and no-go review

## Decision

Close SF-003 as a valid negative experiment. None of the four development-only
candidates is eligible for calibration, configuration freeze or a final frozen
evaluation. The final frozen set therefore remains intentionally nonexistent.

This is a successful application of the method: the project preserved a fixed
guardrail when the result was close instead of moving the threshold to manufacture
an acceptance.

## Evidence reviewed

| Candidate | Main idea | Mean utilization | Worst supported degradation | Decision |
|---|---|---:|---:|---|
| V1 | static lexicographic optimum | 96.81% | 12.58 p.p. | reject |
| V2 | prior compatible-opportunity debt | 96.81% | 12.58 p.p. | reject |
| V3 | label-free placement scarcity | 96.81% | 12.35 p.p. | reject |
| V4 | 90% per-round recovery floor | 95.71% | 10.80 p.p. | reject |

Every candidate produced zero hard-constraint violations, zero opaque-identifier
flips, zero input-order flips and zero K=3 starvation events in the registered
40-seed development set. V4 came closest, but its 10.80 percentage-point result
still exceeded the predeclared 10-point limit.

## What the experiment established

- CP-SAT solves the controlled global-assignment counterexample that defeats both
  greedy baselines.
- A technically optimal assignment is not automatically acceptable under a
  repeated-exclusion policy.
- Residual tie-breaks had too little leverage on this longitudinal cohort.
- A local, slice-aware oracle suggested capacity for improvement, but its fixed
  cohort path did not transfer to the label-free end-to-end V4 policy.
- Relaxing the efficiency objective improved exposure but did not meet the entire
  declared contract.

These are controlled synthetic observations. They are not evidence of clinical,
access, financial or demographic impact.

## Why there is no V5

Another objective change would be post-result tuning against the same 40 seeds.
It would increase researcher degrees of freedom and make a later calibration run
look more independent than it is. The responsible next step is a new research
specification with a new development distribution and a separately justified
policy, not another SF-003 candidate.

## Progression boundary

S4 may expose the deterministic fixtures, baseline trade-offs and this rejected
research decision through a local API. It must not label V4 as recommended, create
a final frozen set or imply that an automatic scheduling action is safe. S7 is
skipped under the present research line because its eligibility gate was not met.

## Interview and video lesson

The strongest result is the decision process: define the rejection rule first,
test increasingly plausible hypotheses, preserve decision/audit separation and
stop when further tuning would compromise the evidence. The video should show the
counterexample, the improving-but-still-rejected sequence and the human-owned
`automatic_action: none` boundary.
