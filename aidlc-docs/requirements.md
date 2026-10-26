# SlotFit requirements

## Intent

Study whether a constraint-based plan can recover more usable time than FIFO or local best-fit in synthetic clinic calendars while preserving hard constraints and human control.

## Functional requirements

- **SF-FR-001:** load or generate a synthetic scenario from a recorded seed.
- **SF-FR-002:** evaluate eligibility with stable reason codes.
- **SF-FR-003:** execute FIFO and local best-fit on identical inputs.
- **SF-FR-004:** later execute a constraint strategy over the day horizon.
- **SF-FR-005:** present up to three plans and their trade-offs.
- **SF-FR-006:** record a human review decision without changing a real schedule.
- **SF-FR-007:** export per-scenario and aggregate evaluation evidence.
- **SF-FR-008:** report selection, exposure, wait and starvation outcomes by declared operational slice.
- **SF-FR-009:** present utilization and fairness dimensions separately, including the worst-slice result and violated guardrails.
- **SF-FR-010:** provide a deterministic synthetic clinic-day story fixture that extends the global-conflict counterexample with display-only context kept outside every decision input.
- **SF-FR-011:** provide a plain-language explanation for every eligibility reason code, served with each evaluation.

## Non-functional requirements

- **SF-NFR-001:** same seed and version produce the same scenario.
- **SF-NFR-002:** hard-constraint violations must be zero.
- **SF-NFR-003:** core behavior is testable without network access.
- **SF-NFR-004:** every run records strategy and input versions.
- **SF-NFR-005:** a clean local setup is documented.
- **SF-NFR-006:** opaque identifiers and irrelevant input ordering do not change the plan.
- **SF-NFR-007:** fairness thresholds are recorded before the frozen test run and cannot be tuned against its results.
- **SF-NFR-008:** synthetic scenario provenance includes seed, generator version and distribution configuration.

## Prohibited behavior

- external communication or booking;
- real PHI/PII;
- inferred clinical priority;
- automatic consequential decision;
- unsupported financial or patient-outcome claim.

## Primary metric

`recovered_utilization = scheduled_minutes / feasible_open_minutes`

The denominator excludes time for which no factually feasible combination exists.

## Fairness measurement boundary

Fairness is defined here as avoiding preventable repeated exclusion across operational slices such as duration, availability, resource need, wait age and notice requirement. It is not a claim of demographic fairness or real-world clinical benefit. The complete contract is in [`../docs/fairness-and-bias-plan.md`](../docs/fairness-and-bias-plan.md).
