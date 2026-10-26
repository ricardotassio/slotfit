# ADR-0004 — Layered package layout and a single composition root

- Status: Accepted (2026-10-26, SF-016)
- Supersedes: the flat module list implied by ADR-0001; the modular-monolith
  decision itself stands.

## Context

After SF-015 the dependency direction held in the imports (domain imports only
the standard library, OR-Tools only in the optimizer, FastAPI and Pydantic only
at the boundary, sqlite3 only in persistence), but 23 modules sat side by side
in `src/slotfit`. A reader could not see the layers without reading the
imports, and the FastAPI application and the SQLite repository were created at
import time inside the routes module.

## Decision

Adopt a ports-and-adapters layout, in the light form idiomatic to Python
(Percival and Gregory, *Architecture Patterns with Python*): packages are the
layer boundary, the core is made of pure functions and frozen values, and one
module chooses concrete adapters.

```text
src/slotfit/
  domain/        model, eligibility, explanations, day_context
  application/   strategies, scenarios
  solver/        optimizer                    (only importer of ortools)
  research/      generation, multi_generation, evaluation, longitudinal,
                 comparison, alternative_diagnostic, exposure_frontier, thresholds
  adapters/
    api/         routes, schemas, service     (only importers of fastapi, pydantic)
    persistence/ sqlite_review_repository     (only importer of sqlite3)
    cli/         demo, report, diagnostic, frontier
  composition.py create_app(): binds the repository, registers the routes,
                 serves web/dist when it exists
```

Allowed direction: `domain` imports nothing from the package; `application`
imports `domain`; `solver` imports `domain` and `application`; `research`
imports those three; `adapters` import anything below them and never
`composition`; `composition` imports anything.

`tests/test_architecture.py` enforces the direction and the framework
placement with `ast`, so no linter dependency is needed. It failed on the flat
layout (two failures: loose modules, frameworks outside their adapter) before
the move and passes after it.

## Consequences

- Entry points changed: `uvicorn slotfit.composition:app`,
  `python -m slotfit.adapters.cli.demo` and the three research CLIs.
- Tests override the review repository through the same dependency the
  composition root binds; no production code path builds infrastructure at
  import time.
- Rejected alternatives: feature folders (the project has one feature; the
  meaningful split is by responsibility) and a `Protocol` per dependency
  (almost everything has one implementation; that would be speculative).
- Proof of behaviour preservation: the development report, the multi-slot demo,
  the alternative diagnostic, the exposure frontier and the clinic-day API
  payload were diffed before and after the move with zero differing lines
  once solver wall time is excluded.
