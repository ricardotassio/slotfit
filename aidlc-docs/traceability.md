# Traceability

Implementation contracts: SF-FR-001 through SF-FR-003 map to [`../specs/001-domain-and-baselines.md`](../specs/001-domain-and-baselines.md). Scenario provenance, invariance and slice requirements map to [`../specs/002-scenarios-and-fairness-controls.md`](../specs/002-scenarios-and-fairness-controls.md). Optimization and frozen evaluation map to [`../specs/003-optimizer-and-evaluation.md`](../specs/003-optimizer-and-evaluation.md).

| Requirement | Component | Test/evidence | Status |
|---|---|---|---|
| SF-FR-001 | `slotfit.scenarios.demo`, `slotfit.generation` | fixture and generated replay tests | Implemented |
| SF-FR-002 | `slotfit.eligibility` | exclusion and consent tests | Implemented in first slice |
| SF-FR-003 | `slotfit.strategies` | FIFO and best-fit tests | Implemented |
| SF-FR-004 | `slotfit.optimizer` | global-conflict, phase and limit tests | Implemented for first multi-slot fixture |
| SF-FR-005 | future web app | Playwright demo flow | Planned |
| SF-FR-006 | future review service | integration/idempotency tests | Planned |
| SF-FR-007 | `slotfit.evaluation`, `slotfit.comparison` | event records, aggregate comparison and violation tests | Implemented for development split |
| SF-FR-008 | `slotfit.longitudinal`, `slotfit.comparison`, `slotfit.alternative_diagnostic`, `slotfit.exposure_frontier` | compatible misses, K sensitivity, slice exposure, guardrail, alternative capacity and local frontier | Implemented for development; V1–V3 rejected |
| SF-FR-009 | future web app and evaluation report | worst-slice and guardrail display | Planned |
| SF-NFR-001 | scenario generator | equality under same seed | Implemented |
| SF-NFR-002 | strategies and event evaluator | all registered generated seeds | Implemented for baselines |
| SF-NFR-003 | core package | `make test` | Implemented |
| SF-NFR-004 | CLI plans and optimizer evidence | strategy, engine and phase fields | Implemented for current strategies |
| SF-NFR-006 | all strategies | per-seed identifier and input-order metamorphic checks | Implemented for 40-seed development comparison |
| SF-NFR-007 | evaluation configuration | frozen threshold artifact | Planned |
| SF-NFR-008 | `slotfit.generation.ScenarioManifest` | provenance schema and checksum test | Implemented |
