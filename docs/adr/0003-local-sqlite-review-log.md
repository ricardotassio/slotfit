# ADR-0003 — Local SQLite review log before PostgreSQL

- Status: Accepted
- Date: 2026-10-25

## Context

S5 needs to demonstrate transactional idempotency and an append-only human review
trail. The POC has one local process, tiny volume, no background worker, no shared
deployment and no real integration. Running PostgreSQL would add service lifecycle,
credentials and container setup without exercising a concurrency or scale need
that exists in the experiment.

## Decision

Use the Python standard-library SQLite adapter for the local POC. Store immutable
review events with a unique idempotency key inside an explicit transaction. Add
database triggers that reject update and delete operations. Keep the repository
contract and SQL boundary separate so a future PostgreSQL adapter can replace it
when multi-user deployment or measured write contention exists.

## Alternatives considered

- **PostgreSQL now:** deferred because no current requirement needs a server,
  credentials, cross-process concurrency or PostgreSQL-specific feature.
- **In-memory list:** rejected because it cannot demonstrate durable uniqueness,
  transaction behavior or append-only protection.
- **Full event-sourcing framework:** rejected because the only event is a simulated
  human review and no projection/replay infrastructure is required.
- **Message queue:** rejected because nothing is delivered asynchronously.

## Consequences

- A clone can run the review flow without Docker or a database service.
- The demo proves idempotency and immutable audit history at the correct scale.
- SQLite's write-serialization is acceptable only for this single-user local POC.
- Production or multi-user claims require a new ADR and PostgreSQL integration
  tests; this implementation is not evidence of production persistence capacity.

