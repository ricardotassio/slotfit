# ADR-0005 — Docker image as a secondary reproduction path

- Status: Accepted (2026-10-26, SF-016)

## Context

The primary setup is lockfile-based and local (`uv`, Node, `make verify`). A
reader who wants to see the evidence without installing Python, uv or Node
had no path, and the README promised "no Docker" as a simplification rather
than as a boundary.

## Decision

Add a multi-stage `Dockerfile` and a `compose.yaml`:

- stage 1 builds the web bundle with Node from `web/package-lock.json`;
- stage 2 installs the locked Python environment with `uv sync --frozen` from
  `uv.lock`, copies the source and tests, and runs
  `uvicorn slotfit.composition:app` on port 8000, which serves the API and the
  built UI from one process;
- the review log is written to `/data/slotfit.db` (named volume in compose),
  selected through `SLOTFIT_REVIEW_DATABASE`.

`make docker-build`, `make docker-run` and `make docker-test` wrap the three
uses. `docker-test` runs the Python suite and an in-process smoke test inside
the image; browser tests stay on the host because they need Playwright's
Chromium.

## Consequences

- The local lockfile setup remains the primary and CI path; the image is a
  convenience for reproduction and must not drift from the lockfiles, which is
  why it installs only from `uv.lock` and `package-lock.json`.
- The container has no network dependency at runtime and reads no real data;
  the claim boundary of `AGENTS.md` is unchanged.
- The base images (`python:3.12-slim`, `node:24-slim`, the `uv` binary image)
  are the only additions; they are not Python or npm dependencies.
