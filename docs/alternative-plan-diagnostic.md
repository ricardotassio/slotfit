# Primary-optimal alternative-plan diagnostic

## Question

Did exposure-debt V2 fail because efficiency and request count leave no alternative,
or because its residual signal does not choose among available alternatives?

## Method

For each of 40 development seeds and five controlled rounds, a bounded exhaustive
enumerator receives only the decision `Scenario`. It retains all feasible plans
tied on recovered minutes and requests served. Only after enumeration does a
separate analyzer join audit slices and ask whether an alternative would expose
more requests from a slice.

This post-hoc oracle is diagnostic only. A strategy may not consume these slice
labels, and independently attractive round alternatives are not necessarily one
globally consistent five-round policy.

## Result

- 200 rounds analyzed;
- zero rounds where V2 missed the primary optimum;
- 34 rounds with more than one primary-optimal plan;
- the failing `notice_band=moderate` slice had 42 eligible opportunities and 24
  actual V2 exposures;
- in 8 rounds, an efficiency-equivalent alternative could expose more moderate-
  notice requests;
- those local alternatives contain 9 additional exposures in total.

Other supported slices also had local alternative capacity, including
`availability_band=single` (4), `wait_age_band=middle` (8) and
`wait_age_band=recent` (16). Duration slices had no local additional capacity on
the observed V2 cohort path.

## Decision

The evidence did not yet require sacrificing recovered minutes or request count.
There was residual choice, but exposure debt did not discriminate it. This result
authorized one label-free, decision-derived placement-scarcity V3 test on
development only.

## V3 follow-up

Placement scarcity changed 17 decisions across 8 seeds and reduced the worst
supported degradation from 12.58 to 12.35 p.p. without losing primary efficiency.
It used some residual capacity but did not pass the fixed 10 p.p. guardrail.
Therefore the next gate is an explicit efficiency-versus-exposure frontier instead
of another tie-breaker.

## Reproduction

```bash
make alternative-diagnostic
```
