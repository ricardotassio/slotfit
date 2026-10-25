# SF-003 — Optimizer and controlled evaluation

- Status: Draft
- AI-DLC mapping: Bolts S3 and S7
- Depends on: SF-002

## Experimental question

Can a constraint strategy improve recovered utilization over FIFO and local best-fit on frozen synthetic scenarios without violating hard constraints or predeclared repeated-exclusion guardrails?

## Candidate design

- OR-Tools CP-SAT behind the existing strategy boundary;
- hard constraints for factual feasibility;
- separately reported soft dimensions for utilization, requests served, wait age and starvation;
- bounded runtime with explicit infeasible and timeout behavior;
- no silent fallback that changes the reported strategy.

## Required comparisons

All strategies use identical manifests. Report:

- hard-constraint violations;
- recovered utilization;
- selection and exposure by slice;
- median and p90 simulated wait;
- starvation rate;
- worst-slice gap;
- sensitivity to objective weights;
- runtime and solver status.

## Rejection conditions

- any hard-constraint violation;
- opaque-identifier counterfactual flip;
- threshold chosen after viewing frozen-test outcomes;
- a utilization gain that crosses a starvation or worst-slice guardrail;
- unexplained infeasible, timeout or fallback behavior;
- gain visible only in one convenient seed or distribution.

## Acceptance criteria to resolve before `Ready`

- [ ] Exact development-only method for choosing guardrail thresholds.
- [ ] Maximum solver runtime and deterministic configuration.
- [ ] Objective terms, units and permitted weight ranges.
- [ ] Frozen manifest size justified by a precision or uncertainty target.
- [ ] Output artifact schema and comparison report approved.

## Public evidence boundary

The final result may report measured controlled behavior on the versioned synthetic benchmark. It may not claim clinic impact, access improvement, revenue recovery, patient benefit or production readiness.
