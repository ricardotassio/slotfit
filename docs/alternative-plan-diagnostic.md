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

The evidence does not yet require sacrificing recovered minutes or request count.
There is residual choice, but exposure debt did not discriminate it. V3 may test a
label-free, decision-derived placement-scarcity signal: requests compatible with
fewer intervals receive residual priority after minutes and count. This hypothesis
must be specified and tested on development only.

If placement scarcity cannot use the observed residual capacity, the project will
measure an explicit efficiency-versus-exposure frontier instead of adding more
unjustified tie-breakers.

## Reproduction

```bash
make alternative-diagnostic
```
