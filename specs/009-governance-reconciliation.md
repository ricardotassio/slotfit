# SF-009 — Governance reconciliation before cycle 2

- Status: Done
- AI-DLC mapping: Bolt S9 (first Bolt of cycle 2)
- Depends on: SF-008 Done; cycle 2 proposal approved by Ricardo on 2026-10-26
  ([`../aidlc-docs/refinement-plan-2026-10.md`](../aidlc-docs/refinement-plan-2026-10.md))

## Purpose

Bring documentation, tests and the web component back into agreement before any
new feature. `AGENTS.md` requires that a conflict between documents and code is
resolved in the owning document before implementation continues. Three such
conflicts exist at HEAD `d448e14`.

## Observed conflicts

1. The uncommitted rewrite of `docs/video-script-en.md` says "against a limit of
   10"; `tests/test_publication_contract.py` only accepts "limit was/at 10", so
   `make test` fails (83 of 84).
2. Commits `0826cdf` and `5fb9094` redesigned `web/src/App.vue` after SF-008 was
   marked Done, without a spec. The component no longer uses FullCalendar, yet
   `web/package.json`, SF-006, the README, the S6 card and the execution plan
   still describe a FullCalendar UI. The component and stylesheet are compressed
   into a few very long lines, and the page introduces asymmetric treatment of the
   plans (distinct pill styles, a one-directional gain bridge, asymmetric footers
   and a marketing headline), which SF-006 lists as rejection conditions.
3. `docs/bolts/README.md` and the S3 card still say S3 is in progress; the audit
   still lists the license as an open decision although `LICENSE` exists.

## Scope

- Accept the "limit of 10" phrasing in the publication contract test and commit
  the video scripts, storyboard and production plan; link the production plan
  from the README.
- Remove `@fullcalendar/vue3` and `temporal-polyfill` (decision D3) and update
  every document that names them.
- Split `App.vue` into readable components and expand `style.css`, with no
  behavior change, guarded by the five existing Playwright tests.
- Restore SF-006 neutrality: same pill and card treatment for every plan, a
  signed "difference in this fixture" instead of a one-directional gain, factual
  footers, descriptive headline; add a browser test that forbids promotional or
  claim-breaking phrases on the Evidence page.
- Update the S3 card, the bolt catalog, the audit open decisions and add an
  SF-006 addendum recording the re-evaluation.

Out of scope: any new feature, the story mode, new fixtures, new API fields.

## Acceptance criteria

- [x] `make test` passes with the committed video documents.
- [x] No reference to FullCalendar or `temporal-polyfill` remains outside
      historical audit entries and this spec.
- [x] `web/src/App.vue` is under 120 lines and no source line in `web/src`
      exceeds 160 characters.
- [x] The Evidence page gives every plan the same visual treatment and contains
      none of: "recommended", "best plan", "AI choice", "AI optimized", "fair",
      "unbiased", "bias-free", "production ready", "revenue", "more patients".
- [x] Five existing Playwright tests still pass; one new forbidden-phrase test
      passes; axe reports no serious or critical violation.
- [x] `make verify` passes and the worktree is clean.
- [x] S3 card, bolt catalog, audit, SF-006 addendum and traceability updated.

## Rejection conditions

- any plan is visually or verbally presented as recommended;
- a behavior change ships inside the "no behavior change" refactor commit;
- a dependency is removed while a document still claims it is used.

## Observed evidence

Closed 2026-10-26 at the commit that records this evidence.

- `make verify`: 84 Python tests, in-process API smoke, typed production build
  and six Playwright tests pass (five original, one new neutrality test).
- `web/src/App.vue` is 114 lines; no line in `web/src` exceeds 160 characters;
  the compressed stylesheet is one declaration per line.
- `@fullcalendar/vue3` and `temporal-polyfill` removed from `package.json` and
  the lockfile; README, SF-006, the S6 card and the execution plan updated; the
  only remaining mentions are historical (audit, SF-006 addendum, this spec).
- Evidence page: one card, pill, appointment and swatch style for every plan;
  signed "difference in this fixture"; factual footers; descriptive headline;
  forbidden-phrase test green.
- Publication contract test accepts "limit of 10"; video scripts, storyboard and
  production plan committed and linked from the README.
- S3 card and bolt catalog say "closed, terminal no-go"; audit open decision on
  the license marked resolved; SF-006 addendum written; traceability links
  SF-009.

Commits: `e8c4e17`, `b570904`, `0462075`, `0ae45a2`, `11a63fb`, `4b32c58`,
`b778f22` and the documentation commit that closes this gate.
