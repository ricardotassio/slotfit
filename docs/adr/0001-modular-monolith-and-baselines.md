# ADR-0001 — Modular monolith and explicit baselines

- Status: Accepted
- Date: 2026-10-25

## Context

The experiment needs a reproducible end-to-end workflow, but has one developer, low volume and no independent deployment requirements.

## Decision

Use one repository and one deployable API/web system with internally separated domain modules. Implement FIFO and best-fit before adding CP-SAT.

## Consequences

- Lower operational complexity and easier local reproduction.
- The optimizer must prove value against real baselines.
- Components can be separated later only if deployment or scaling evidence appears.
- The project intentionally does not demonstrate microservices.

