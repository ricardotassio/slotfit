# SF-010 — Clinic-day story fixture and plain-language explanations

- Status: Done
- AI-DLC mapping: Bolt S10
- Depends on: SF-009 Done; cycle 2 plan sections 3 and 5
  ([`../aidlc-docs/refinement-plan-2026-10.md`](../aidlc-docs/refinement-plan-2026-10.md))

## Purpose

Give the three-screen story (problem, impact on the clinic, solution) a
deterministic synthetic day and plain-language reasons, produced by the same
engine and served by the same API, so that no number or sentence in the story is
hand-written in the UI.

## Domain scope

- `slotfit.explanations`: `REASON_CODES` is the closed list of eligibility reason
  codes; `explain(reason_code)` returns one short English sentence per code;
  `explain_evaluation(evaluation)` returns the eligible sentence or one sentence
  per reason code. Unknown codes raise. The copy never uses audit-band vocabulary
  ("scarce", "narrow", "aging", "band", "slice") so the UI cannot look
  slice-aware.
- `slotfit.day_context`: `BookedAppointment`, `Cancellation` and `DayContext`
  are frozen display-only values. They never enter `Scenario`, eligibility,
  strategies or the optimizer; a source scan test enforces that boundary.
- `slotfit.scenarios.clinic_day_story(seed=1600)` returns `(Scenario, DayContext)`.
  The scenario reuses the two openings and two requests of
  `multi-slot-counterexample-1500` and adds a third request that needs the closed
  Room B. Seed `1600` is hand-built and belongs to no registry (`SPLIT_SEEDS`,
  `MULTI_SLOT_SEEDS`); it is not a development seed.

## API scope

- `GET /api/v1/demos/clinic-day`: FIFO, local best-fit and CP-SAT plans, optimizer
  evidence, the existing counterexample disclosure, and `day_context`.
- `CandidateEvaluationResponse.explanations: list[str]` on every demo.
- `DemoResponse.day_context: DayContextResponse | None` (`null` for other demos).
- `SCHEMA_VERSION` becomes `1.1` (additive change); the review command schema
  stays `1.0`.

## Acceptance criteria

- [x] `clinic_day_story` is deterministic and shares intervals and the first two
      requests with the 1500 fixture; FIFO and best-fit recover 60 minutes, CP-SAT
      recovers 120 with three `OPTIMAL` phases; the Room B request is ineligible
      for both openings with `REQUIRED_ROOM_UNAVAILABLE` only.
- [x] Booked appointments never overlap an opening; the day window contains every
      booked appointment and opening; every opening has a cancellation record.
- [x] `domain.py`, `eligibility.py`, `strategies.py` and `optimizer.py` do not
      import `day_context`.
- [x] Every code appended in `eligibility.py` has an explanation and vice versa.
- [x] The API contract test covers `clinic-day`, `explanations` on every
      evaluation and `day_context: null` on the other demos.
- [x] `make verify` passes; traceability gains SF-FR-010 and SF-FR-011.

## Rejection conditions

- a strategy or the optimizer reads `DayContext`;
- explanation text mentions a slice, band or demographic attribute;
- the story fixture is registered or used as a development seed;
- any plan number for `clinic-day` differs from the engine output.

## Observed evidence

Closed 2026-10-26.

- `make verify`: 98 Python tests (14 new), in-process API smoke, typed web build
  and six Playwright tests pass.
- `clinic_day_story()` is equal across calls, shares intervals and the first two
  requests with `multi-slot-counterexample-1500`, and its third request fails only
  with `REQUIRED_ROOM_UNAVAILABLE`; FIFO 60, best-fit 60, CP-SAT 120 with three
  `OPTIMAL` phases and every assignment on an eligible pair.
- Seven booked blocks sit inside the 08:00–17:00 day and never overlap the
  14:00 and 15:30 openings; both openings carry a cancellation record; Room B is
  listed as closed. Seed 1600 is in neither `SPLIT_SEEDS` nor `MULTI_SLOT_SEEDS`.
- `domain.py`, `eligibility.py`, `strategies.py` and `optimizer.py` contain no
  reference to `day_context`.
- The six codes appended in `eligibility.py` equal `REASON_CODES`; the copy
  contains none of "scarce", "narrow", "aging", "band", "slice".
- `GET /api/v1/demos/clinic-day` returns three plans (60/60/120), optimizer
  evidence, seven booked blocks, two cancellations, `["ROOM-B"]` closed and a
  non-empty `explanations` list on every evaluation; the other demos return
  `day_context: null`; health and error envelopes report schema `1.1`.

Commits: `b0e5d2f`, `2cf4212`, `9105240`, `af39859` and the closing docs commit.
