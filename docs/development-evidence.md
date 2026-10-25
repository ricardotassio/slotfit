# Development evidence — SF-003

## Decision

**The first CP-SAT candidate is rejected for progression to calibration.**

It improves controlled utilization and passes safety, optimality, stability and
repeated-exclusion checks, but fails the predeclared supported-slice guardrail.
The correct response is to revise the candidate on development data, not to relax
the guardrail.

## Controlled scope

- split: `development` only;
- generator: `slotfit-multislot-v1`;
- distribution: `multislot-operational-v1`;
- 40 registered seeds, 10 synthetic requests and 3 openings per seed;
- 5 compatible-opportunity rounds per strategy and seed;
- no real, patient or clinic data;
- no final frozen manifest exists.

Every strategy consumes the same decision scenario. Operational slices are joined
after planning and never enter eligibility or objective coefficients.

## Aggregate observations

| Strategy | Mean recovered utilization | Mean requests served | Starvation K=3 | Overall exposure | Hard violations |
|---|---:|---:|---:|---:|---:|
| FIFO | 72.01% | 2.200 | 3.57% | 59.79% | 0 |
| Local best-fit | 76.46% | 2.275 | 2.98% | 60.87% | 0 |
| CP-SAT candidate | 96.81% | 2.700 | 0.00% | 70.59% | 0 |

The CP-SAT candidate returned three `OPTIMAL` phases on all 40 seeds. Across all
development seeds and strategies, reversing request/interval input order and
renaming opaque identifiers caused zero assignment-position flips.

These observations describe this synthetic development distribution only. They do
not demonstrate clinic impact, production latency, demographic fairness or patient
benefit.

## Guardrail decision

An exposure gap is the signed difference between overall exposure and slice
exposure. For pass/fail, negative gaps are clamped to zero because an above-overall
slice has no exposure shortfall. A candidate slice is compared only with baseline
observations that independently meet the minimum support of 30 eligible
opportunities.

| Guardrail | Observed | Limit | Result |
|---|---:|---:|---|
| Hard-constraint violations | 0 | 0 | Pass |
| Opaque-ID flips | 0 | 0 | Pass |
| Input-order flips | 0 | 0 | Pass |
| K=3 starvation degradation vs better baseline | -2.98 pp | +5.00 pp | Pass |
| Worst supported exposure-shortfall degradation | +12.58 pp | +10.00 pp | **Fail** |

The failing comparison is `notice_band=moderate`. Eleven candidate slices had a
supported baseline reference. Unsupported slices remain visible in the report but
cannot determine pass/fail.

The candidate's own largest absolute supported exposure gap is 23.71 p.p. for
`availability_band=single`. That is a different measurement from the failing
12.58 p.p. *degradation relative to the better supported baseline*; both are
reported so the narrative cannot substitute one for the other.

## Interpretation

The result is not “CP-SAT is biased” and it is not “optimization failed.” It shows
that the present lexicographic objectives optimize minutes, number served and wait
age but do not directly control exposure shortfall across repeated compatible
opportunities. A globally efficient static plan can therefore be insufficient as
a longitudinal policy.

## Candidate V2 hypothesis — tested and rejected

V2 tested a minimal, auditable exposure-debt signal derived only from prior compatible
opportunities missed by each request. The signal does not use audit-only slice
labels. It enters after recovered minutes and requests served, preserving all hard
constraints, and before the existing wait-age tie-break.

The focused counterexample passed: when efficiency and count tie, a request with
two prior misses gains priority. However, V2 changed **zero** round-level selections
relative to V1 across the 40 development seeds. Aggregate metrics therefore did
not change, and V2 was rejected by the same 12.58 p.p. slice degradation.

This negative result indicates that exposure debt is ineffective when placed only
as a residual objective on the current distribution: the higher-priority phases
often leave no relevant alternative, or remaining requests carry equal debt.

## Next diagnostic gate

Before proposing V3:

1. enumerate or constrain alternative plans at the same recovered minutes and
   requests served;
2. measure whether those alternatives can improve exposure without using audit
   labels in the decision;
3. if not, produce an explicit efficiency-versus-exposure frontier on development;
4. do not enter calibration or mint final seeds.

## Candidate V3 — tested and rejected

V3 added decision-derived placement scarcity after exposure debt and before wait
age. It changed 17 round-level selections across 8 seeds without changing recovered
utilization or requests served. The worst supported degradation fell from 12.58 to
12.35 p.p., while the binding slice moved from moderate notice to short duration.

The improvement is real but below the fixed requirement. V3 remains rejected, and
calibration remains closed. Because the diagnostic had already established
residual alternatives and V3 used only part of that capacity, the next analysis
will construct an explicit development-only efficiency/exposure frontier rather
than adding another heuristic tie-break.

## Candidate V4 — tested and rejected

V4 applied the frontier-derived 90% per-round recovery floor before the label-free
debt, scarcity and wait-age phases. End-to-end, it reached 95.71% mean utilization
and kept 2.700 mean requests served, zero K=3 starvation and zero safety or
counterfactual violations.

The worst supported degradation improved to 10.80 p.p. but still failed the fixed
10 p.p. limit. This also demonstrates why the local oracle was correctly labelled a
diagnostic: changed selections alter later cohorts, so its 8.24 p.p. estimate did
not transfer directly.

After four candidates, the next action is a methodology/no-go review rather than
another objective. Calibration and final frozen generation remain closed.

## Reproduction

```bash
make development-report
```

The JSON report contains per-seed results, phase statuses and objective values,
recorded solver wall time, counterfactual flips, slice summaries and the explicit
guardrail decision. Runtime is observational metadata and does not participate in
replay equality.
