# SF-016 — Layered package layout, composition root and Docker reproduction

- Status: In progress
- AI-DLC mapping: Bolt S16 (authorized by Ricardo on 2026-10-26, before SF-011)
- Depends on: SF-015 Done

## Purpose

Make the architecture visible in the folder structure. The dependency direction
already holds in the imports (SF-015 audit); this Bolt moves the 23 flat modules
into layer packages, adds a single composition root, enforces the direction
with a test, and provides a Docker image so anyone can reproduce the evidence
without installing Python, uv or Node.

## Scope

### Package layout (behaviour-preserving)

```text
src/slotfit/
  domain/        model, eligibility, explanations, day_context
  application/   strategies, scenarios
  solver/        optimizer                       (only importer of ortools)
  research/      generation, multi_generation, evaluation, longitudinal,
                 comparison, alternative_diagnostic, exposure_frontier, thresholds
  adapters/
    api/         routes, schemas, service        (only importers of fastapi, pydantic)
    persistence/ sqlite_review_repository        (only importer of sqlite3)
    cli/         demo, report, diagnostic, frontier
  composition.py wires the FastAPI app and the review repository
```

- Allowed direction: `domain` imports nothing from the package; `application`
  imports `domain`; `solver` imports `domain` and `application`; `research`
  imports those three; `adapters` import anything below them and never
  `composition`; `composition` imports anything.
- `tests/test_architecture.py` parses every module with `ast` and fails on any
  import that breaks the direction or places a third-party framework outside
  its adapter.
- Plans, numbers, reason codes, API payloads and `SCHEMA_VERSION` stay
  identical; `make verify` is green after every commit.

### Composition root

- `slotfit.composition` creates the app, binds the SQLite repository path and,
  when `web/dist` exists, serves the built UI from the same process.
- Makefile, Playwright configuration, runbook and CI point to the new entry
  points.

### Docker reproduction

- A multi-stage `Dockerfile` builds the web bundle with Node, syncs the locked
  Python environment with uv and runs the API serving the UI on port 8000.
- `make docker-build`, `make docker-run` and `make docker-test` (Python tests
  and API smoke inside the image). Browser tests stay on the host.
- Documented as ADR-0005; the local lockfile setup remains the primary path.

### Documentation

- ADR-0004 records the layered layout and the composition root.
- `docs/architecture.md`, README and the runbook point to the real folders.

## Acceptance criteria

- [ ] `tests/test_architecture.py` fails before the move (RED evidence) and
      passes after it.
- [ ] Every module lives in a layer package; `src/slotfit` has no loose module
      besides `__init__.py` and `composition.py`.
- [ ] `make verify` passes; before/after diff of `make development-report`,
      `make multi-slot-demo`, `make alternative-diagnostic` and
      `make exposure-frontier` is identical except solver wall time.
- [ ] `docker build` succeeds and `make docker-test` passes on the host.
- [ ] README, runbook, architecture doc and both ADRs describe the new layout.

## Rejection conditions

- any observable value changes;
- a framework import outside its adapter package;
- a Docker path that reads real data or contacts an external service;
- a documented folder that does not exist.

## Observed evidence

Open.
