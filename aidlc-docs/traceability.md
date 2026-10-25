# Traceability

Implementation contracts: SF-FR-001 through SF-FR-003 map to [`../specs/001-domain-and-baselines.md`](../specs/001-domain-and-baselines.md). Scenario provenance, invariance and slice requirements map to [`../specs/002-scenarios-and-fairness-controls.md`](../specs/002-scenarios-and-fairness-controls.md). Optimization and frozen evaluation map to [`../specs/003-optimizer-and-evaluation.md`](../specs/003-optimizer-and-evaluation.md).

| Requirement | Component | Test/evidence | Status |
|---|---|---|---|
| SF-FR-001 | `slotfit.scenarios.demo` | `test_demo_scenario_is_deterministic` | Implemented |
| SF-FR-002 | `slotfit.eligibility` | exclusion and consent tests | Implemented in first slice |
| SF-FR-003 | `slotfit.strategies` | FIFO and best-fit tests | Implemented |
| SF-FR-004 | future CP-SAT strategy | frozen benchmark | Planned |
| SF-FR-005 | future web app | Playwright demo flow | Planned |
| SF-FR-006 | future review service | integration/idempotency tests | Planned |
| SF-FR-007 | future evaluation runner | versioned artifacts | Planned |
| SF-FR-008 | future evaluation runner | per-slice exposure, wait and starvation report | Planned |
| SF-FR-009 | future web app and evaluation report | worst-slice and guardrail display | Planned |
| SF-NFR-001 | scenario generator | equality under same seed | Implemented |
| SF-NFR-002 | all strategies | invariant suite | Partial |
| SF-NFR-003 | core package | `make test` | Implemented |
| SF-NFR-006 | all strategies | identifier and input-order metamorphic tests | Planned |
| SF-NFR-007 | evaluation configuration | frozen threshold artifact | Planned |
| SF-NFR-008 | scenario manifest | provenance schema test | Planned |
