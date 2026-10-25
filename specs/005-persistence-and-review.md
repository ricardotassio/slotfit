# SF-005 — Append-only simulated human review

- Status: Ready
- AI-DLC mapping: Bolt S5
- Depends on: SF-004
- Architecture decision: ADR-0003

## Purpose

Record which synthetic plan a human reviewed, without changing a schedule or
contacting anyone. Demonstrate transaction-backed idempotency and immutable audit
history with the minimum infrastructure justified by the local POC.

## Data contract

`review_events` contains:

- server-generated event ID and UTC creation time;
- caller-generated idempotency key, unique and limited to 64 visible ASCII
  characters;
- synthetic `scenario_id` and plan `strategy`, each limited to 128 characters;
- lowercase SHA-256 `plan_checksum`;
- decision: `accept`, `reject` or `request_alternative`;
- optional rationale limited to 500 characters;
- constant `external_action = none`.

No patient, clinic, provider, free-form clinical or contact fields exist. The
schema uses a unique constraint for idempotency and triggers that reject updates
and deletes.

## HTTP contract

### `POST /api/v1/reviews`

Accept the versioned review command above. The first valid request returns `201`
and the stored event. Replaying the same idempotency key with byte-equivalent
semantic content returns `200`, the original event and `replayed: true`.

Reusing the key with different content returns `409` and stable code
`idempotency_conflict`. Pydantic validation errors use a stable versioned envelope
with code `validation_error`; arbitrary framework detail is not exposed.

### `GET /api/v1/reviews/{event_id}`

Return a stored event or stable `review_not_found` error. There is no update or
delete route.

## Repository contract

- `SQLiteReviewRepository` creates the schema explicitly and owns transactions.
- `record(command)` returns whether the result was created or replayed.
- uniqueness is enforced by the database, not a pre-insert read alone;
- on a uniqueness race, read the winner and compare canonical command content;
- persistence failure creates no external side effect;
- tests use a temporary database and no network/service.

## Acceptance criteria

- [ ] Schema migration is deterministic and repeatable.
- [ ] First write creates one immutable event.
- [ ] Equivalent replay returns the same event without a second row.
- [ ] Conflicting replay fails with a stable conflict.
- [ ] Direct update and delete attempts fail closed.
- [ ] Two repository connections cannot create duplicate idempotency rows.
- [ ] API returns versioned 201, 200, 404, 409 and validation contracts.
- [ ] No endpoint or repository performs an external action.
- [ ] Full test suite passes without Docker or PostgreSQL.

## Scope exclusions

- real schedule mutation, communication and identity data;
- authentication/authorization and multi-tenant access;
- PostgreSQL, ORM, event-sourcing framework or message broker;
- list/search endpoints, retention jobs and analytics projections.

Those exclusions are appropriate only for the local synthetic POC. A shared
deployment must reopen them explicitly.

