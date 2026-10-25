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

## Non-functional requirements

- **SF-NFR-001:** same seed and version produce the same scenario.
- **SF-NFR-002:** hard-constraint violations must be zero.
- **SF-NFR-003:** core behavior is testable without network access.
- **SF-NFR-004:** every run records strategy and input versions.
- **SF-NFR-005:** a clean local setup is documented.

## Prohibited behavior

- external communication or booking;
- real PHI/PII;
- inferred clinical priority;
- automatic consequential decision;
- unsupported financial or patient-outcome claim.

## Primary metric

`recovered_utilization = scheduled_minutes / feasible_open_minutes`

The denominator excludes time for which no factually feasible combination exists.

