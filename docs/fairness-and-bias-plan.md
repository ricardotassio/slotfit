# Fairness and bias plan

## Why this belongs in the product contract

A cancellation-recovery tool can improve utilization and still create a bad operational outcome. If it repeatedly favors short appointments, flexible schedules or common resources, the same kinds of requests may remain on the waitlist even when every individual recommendation looks reasonable.

SlotFit therefore treats fairness as an observable system property, not as a claim that an algorithm is "unbiased." Synthetic data cannot prove absence of bias. It can expose assumptions, exercise failure modes and make the trade-off between utilization and repeated exclusion measurable before any real-world evaluation is considered.

## Concrete real-life question

> When a late cancellation creates a usable opening, can the clinic recover time without repeatedly overlooking requests that are harder to place?

The experiment does not infer urgency or decide who deserves care. It ranks feasible synthetic plans for human review. Hard constraints remain hard, and the reviewer sees why each request was included or excluded.

## Current limitations

The first scenario remains a fixed teaching fixture. A separate versioned generator
now produces deterministic operational variation across disjoint seed registries.
That generator supports replay and invariance testing. A controlled longitudinal
runner can repeat compatible-opportunity rounds for the same synthetic cohort, but
those counts are not elapsed patient wait or a real clinic calendar. No request is
labelled starved until a development-only threshold is proposed, reviewed and
frozen, so no aggregate fairness conclusion is supported.

The current baselines also encode preferences:

- FIFO privileges join order;
- local best-fit privileges immediate recovered minutes;
- eligibility rules determine who is considered at all;
- presentation order can anchor the reviewer even when the underlying scores are unchanged.

These are design choices to evaluate, not neutral truths.

## Data boundary

### Decision attributes

Only operational facts required to establish feasibility may affect a plan:

- requested duration;
- compatible provider and room;
- declared availability;
- minimum notice;
- explicit contact consent;
- time already waiting, if the declared fairness policy uses it.

### Audit-only attributes

Synthetic slice labels may be attached to an evaluation record but must not influence eligibility or score unless a later, separately reviewed requirement explicitly says otherwise. Examples include:

- narrow versus broad availability;
- short versus long requested duration;
- common versus scarce resource need;
- short versus long time on the waitlist;
- short versus long notice requirement.

These are operational slices, not demographic groups. SlotFit will not claim demographic fairness from synthetic operational data.

## Scenario design

The generator must be adversarial enough to reveal a weak policy, not merely realistic-looking. The frozen evaluation set will cross the following dimensions:

| Dimension | Example slices | Failure the slice can reveal |
|---|---|---|
| Appointment duration | short, medium, long | short requests always win because they are easier to fit |
| Availability | narrow, broad | flexible requests dominate every recovery opportunity |
| Required resource | common, scarce | scarce-room requests are indefinitely deferred |
| Wait age | recent, aging | a high-utilization policy starves older requests |
| Notice requirement | short, long | short-notice compatibility acts as a hidden advantage |
| Cancellation shape | isolated gap, adjacent gaps | a policy performs well only on a convenient topology |

Generation provenance must include the seed, generator version, distribution configuration and expected challenge property. Development, calibration and frozen test scenarios must be separated before objective weights are finalized.

## Fairness contract

The first fairness objective is operational and deliberately narrow:

> Among feasible requests, improve recovered utilization without creating avoidable repeated exclusion by duration, availability, resource need, wait age or notice requirement.

The policy will be evaluated on both efficiency and fairness. A higher utilization score is not sufficient if a declared guardrail fails.

### Required measurements

- selection rate per operational slice;
- exposure rate: how often an eligible request appears in a displayed plan;
- median and p90 simulated wait by slice;
- starvation rate after a predeclared number of compatible opportunities;
- worst-slice result and gap from the overall result;
- counterfactual flip rate under irrelevant changes;
- hard-constraint violations;
- recovered utilization;
- an efficiency-versus-fairness frontier across fixed objective settings.

Exact thresholds must be set from the development set, recorded before the frozen test run and never adjusted after seeing frozen-test results.

## Invariance and metamorphic tests

The following properties are stronger evidence than a few attractive examples:

1. Changing an opaque request identifier cannot change the decision.
2. Reordering otherwise identical input records cannot change the selected plan, except for an explicitly documented tie-breaker.
3. Increasing wait age while keeping feasibility unchanged cannot reduce the request's fairness contribution.
4. Adding an ineligible request cannot change the plan.
5. Duplicating a request cannot create two bookable people or inflate the objective.
6. The same seed, configuration and version must reproduce the same scenario and result.
7. Small changes to an objective weight must be reported when they cause large changes in who is selected.

These tests do not prove fairness. They detect instability, leakage and arbitrary behavior that would undermine a fairness claim.

## Human factors and presentation bias

The interface must not disguise policy choices as a single authoritative score. Each displayed plan should separate:

- feasibility and any exclusion reasons;
- recovered time;
- number of requests served;
- wait-age or starvation impact;
- operational-slice guardrail status;
- the strategy and objective configuration used.

Plans should use neutral visual treatment, and their ordering rule must be disclosed. The reviewer may accept, reject or ask for another plan; SlotFit never changes a real schedule or contacts a person.

## Evaluation gate

A strategy is eligible for the final demo only if all of the following hold on the frozen controlled benchmark:

- zero hard-constraint violations;
- zero decision changes caused only by opaque identifiers;
- starvation remains within the predeclared guardrail;
- no worst-slice metric crosses its predeclared degradation limit;
- every inclusion and exclusion has a stable explanation;
- utilization gains appear across multiple scenario distributions and seeds, not only one fixture;
- a human remains responsible for the simulated choice.

If no candidate passes, the correct result is that the tested policy is not acceptable. The project will show that failure rather than weaken the guardrail.

## What would be required beyond the POC

No production or fairness conclusion should be drawn without authorized, representative local data; privacy and legal review; stakeholder review of the fairness definition; validation in the intended workflow; monitoring for distribution shift and repeated exclusion; an appeal or override path; and a rollback plan.

The public claim remains limited to controlled, reproducible behavior on synthetic scenarios.

## Reference framework

- [NIST SP 1270: Towards a Standard for Identifying and Managing Bias in Artificial Intelligence](https://www.nist.gov/publications/towards-standard-identifying-and-managing-bias-artificial-intelligence)
- [FDA: Addressing the Limitations of Medical Data for AI](https://www.fda.gov/medical-devices/medical-device-regulatory-science-research-programs-conducted-osel/addressing-limitations-medical-data-ai)
- [FDA: Transparency for Machine Learning-Enabled Medical Devices](https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/transparency-machine-learning-enabled-medical-devices-guiding-principles)
