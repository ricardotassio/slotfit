# Traceability

| Requirement | Component | Test/evidence | Status |
|---|---|---|---|
| SF-FR-001 | `slotfit.scenarios.demo` | `test_demo_scenario_is_deterministic` | Implemented |
| SF-FR-002 | `slotfit.eligibility` | exclusion and consent tests | Implemented in first slice |
| SF-FR-003 | `slotfit.strategies` | FIFO and best-fit tests | Implemented |
| SF-FR-004 | future CP-SAT strategy | frozen benchmark | Planned |
| SF-FR-005 | future web app | Playwright demo flow | Planned |
| SF-FR-006 | future review service | integration/idempotency tests | Planned |
| SF-FR-007 | future evaluation runner | versioned artifacts | Planned |
| SF-NFR-001 | scenario generator | equality under same seed | Implemented |
| SF-NFR-002 | all strategies | invariant suite | Partial |
| SF-NFR-003 | core package | `make test` | Implemented |

