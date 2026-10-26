# Traceability

Implementation contracts: SF-FR-001 through SF-FR-003 map to [`../specs/001-domain-and-baselines.md`](../specs/001-domain-and-baselines.md). Scenario provenance, invariance and slice requirements map to [`../specs/002-scenarios-and-fairness-controls.md`](../specs/002-scenarios-and-fairness-controls.md). Optimization and its terminal development decision map to [`../specs/003-optimizer-and-evaluation.md`](../specs/003-optimizer-and-evaluation.md). The read-only HTTP boundary maps to [`../specs/004-api-boundary.md`](../specs/004-api-boundary.md). Governance reconciliation of the UI, dependencies and publication test after the first cycle maps to [`../specs/009-governance-reconciliation.md`](../specs/009-governance-reconciliation.md). Code organization and the experiment narrative map to [`../specs/015-code-organization-and-experiment-narrative.md`](../specs/015-code-organization-and-experiment-narrative.md). The layered package layout, composition root and Docker path map to [`../specs/016-layered-package-and-docker.md`](../specs/016-layered-package-and-docker.md).

| Requirement | Component | Test/evidence | Status |
|---|---|---|---|
| SF-FR-001 | `slotfit.scenarios.demo`, `slotfit.generation` | fixture and generated replay tests | Implemented |
| SF-FR-002 | `slotfit.eligibility` | exclusion and consent tests | Implemented in first slice |
| SF-FR-003 | `slotfit.strategies` | FIFO and best-fit tests | Implemented |
| SF-FR-004 | `slotfit.optimizer` | V1–V4 global-conflict, residual-policy, floor, phase and limit tests | Implemented through bounded-recovery development candidate |
| SF-FR-005 | `slotfit.api`, Vue comparison UI | API contracts and Playwright main flow | Implemented |
| SF-FR-006 | `slotfit.persistence`, review API | integration/idempotency tests | Implemented for simulated local review |
| SF-FR-007 | `slotfit.evaluation`, `slotfit.comparison` | event records, aggregate comparison and violation tests | Implemented for development split |
| SF-FR-008 | `slotfit.longitudinal`, `slotfit.comparison`, `slotfit.alternative_diagnostic`, `slotfit.exposure_frontier` | compatible misses, K sensitivity, slice exposure, guardrail, alternative capacity and local frontier | Implemented for development; V1–V3 rejected |
| SF-FR-009 | Vue outcome panel and development report | Playwright no-go/metric assertions | Implemented for development evidence |
| SF-FR-010 | `slotfit.scenarios.clinic_day_story`, `slotfit.day_context` | determinism, superset of the 1500 fixture, 60/60/120, no overlap, registry exclusion, decision-module import scan | Implemented |
| SF-FR-011 | `slotfit.explanations`, API `explanations` field | full reason-code coverage, unknown-code rejection, no audit-band vocabulary, API contract | Implemented |
| SF-NFR-001 | scenario generator | equality under same seed | Implemented |
| SF-NFR-002 | strategies and event evaluator | all registered generated seeds | Implemented for baselines |
| SF-NFR-003 | core package | `make test` | Implemented |
| SF-NFR-004 | CLI and API plan evidence | strategy, engine and phase fields | Implemented for current strategies |
| SF-NFR-005 | runbook, lockfiles and CI | locked setup plus `make verify` | Implemented |
| SF-NFR-006 | all strategies | per-seed identifier and input-order metamorphic checks | Implemented for 40-seed development comparison |
| SF-NFR-007 | SF-003/SF-007 gate | fixed threshold plus terminal no-go | Final run intentionally ineligible |
| SF-NFR-008 | `slotfit.generation.ScenarioManifest` | provenance schema and checksum test | Implemented |
| SF-NFR-009 | `slotfit.optimizer`, `slotfit.comparison`, `slotfit.thresholds`, API boundary | behaviour-preserving refactors proven by before/after diffs of the development report, demos and diagnostics (SF-015) | Implemented |
| SF-NFR-011 | `tests/test_architecture.py`, package layout (ADR-0004) | every module in a layer package; inward imports; frameworks only in their adapter; RED on the flat layout, GREEN after the move (SF-016) | Implemented |
| SF-NFR-012 | `Dockerfile`, `compose.yaml`, `make docker-test` (ADR-0005) | image built from lockfiles only; 102 tests and API smoke pass inside it (SF-016) | Implemented |
| SF-NFR-010 | README, `docs/architecture.md`, `web/tests/screenshots.spec.ts` | sequential experiment narrative with generated screenshots carrying the no-go strip; publication-contract tests (SF-015) | Implemented |
