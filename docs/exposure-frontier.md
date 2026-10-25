# Local efficiency/exposure frontier

## Question

How much locally recoverable time would an oracle need to trade before V3's binding
short-duration slice meets its unchanged 10 percentage-point degradation limit?

## Controlled method

The frontier follows the V3 cohort path for 40 development seeds and five rounds.
At each round, it enumerates feasible plans from decision data only. A post-hoc
oracle then maximizes exposure for `duration_band=short` under predeclared floors of
100%, 95%, 90% and 80% of that round's maximum recovered minutes.

The slice label enters only the diagnostic oracle after plan enumeration. This
cannot be deployed as a policy. Counterfactual choices also do not alter later V3
cohorts, so the result measures local capacity rather than a globally consistent
longitudinal strategy.

## Observed frontier

| Local floor | Aggregate recovered | Ratio vs optimum | Short exposures | Shortfall degradation | Target gate |
|---:|---:|---:|---:|---:|---|
| 100% | 7,950 / 7,950 min | 100.00% | 40 / 73 | 12.35 p.p. | Fail |
| 95% | 7,950 / 7,950 min | 100.00% | 40 / 73 | 12.35 p.p. | Fail |
| 90% | 7,905 / 7,950 min | 99.43% | 43 / 73 | 8.24 p.p. | Pass |
| 80% | 7,575 / 7,950 min | 95.28% | 59 / 73 | -3.45 p.p. | Pass |

The 95% floor produces the same choices as the optimum because appointment
durations are discrete. At the 90% floor, three additional short exposures cost 45
aggregate minutes while preserving 168 requests served on the fixed V3 path.

## Decision

This does **not** accept a candidate or the complete guardrail suite. It provides a
grounded V4 hypothesis: constrain each round to at least 90% of maximum recovered
minutes, then use label-free request history and placement scarcity to choose within
that feasible region. V4 must be evaluated end-to-end because its selections will
change subsequent cohorts and may move the worst slice again.

Calibration remains closed. The 90% value is a development-derived candidate
configuration and must be frozen before calibration if V4 passes development.

## Reproduction

```bash
make exposure-frontier
```
