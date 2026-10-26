# SF-006 — Neutral comparison and simulated-review UI

- Status: Done
- AI-DLC mapping: Bolt S6
- Depends on: SF-004 and SF-005

## Purpose

Make the controlled assignment conflict and the terminal no-go understandable in
one local page. The interface is a comparison instrument, not a recommendation
engine: it gives equal visual treatment to plans, separates metrics and keeps a
table fallback beside the calendar.

## Primary flow

1. Load `global-conflict` and the development decision in parallel.
2. Show skeleton/loading text, then the research-outcome disclosure before plans.
3. Select a plan through a neutral radio group ordered FIFO, local best-fit, CP-SAT.
4. Render its assignments in a one-day time-grid and the same information in an
   accessible table.
5. Show recovered minutes, remaining gap and request count as separate values.
6. Expand eligibility/exclusion reason codes without hiding empty explanations.
7. Record `accept`, `reject` or `request_alternative` as a simulated review.
8. Keep one idempotency key while a submission is pending or retried; show whether
   the server created or replayed the event.

## Presentation-bias controls

- No plan is named “best”, “recommended” or “AI choice”.
- The selected default is FIFO because the declared order is baseline-first, not
  because it is the desired decision.
- Cards use the same size, typography and color treatment.
- Utilization and repeated-exclusion research results are never blended into one
  score.
- The CP-SAT counterexample disclosure and terminal research no-go are visible
  without expansion.
- Color is redundant with labels, icons/text and table values.

## States

- loading: visible status text and disabled review controls;
- success: calendar, table, metrics, reasons and no-go disclosure;
- API failure: actionable retry button and no stale plan controls;
- review pending: all decision buttons disabled;
- review success/replay: live-region confirmation with event ID;
- review conflict/failure: live-region error; no claim that an external action ran.

## Accessibility contract

- semantic heading order and landmark regions;
- keyboard-operable plan and review choices;
- visible focus indicators and minimum WCAG AA contrast targets;
- calendar has an adjacent table describing every assignment;
- status/error messages use appropriate live regions;
- automated axe scan has zero serious or critical violations in the main flow.

## Technology decision

- Vue `3.5.44` and TypeScript `6.0.3` for a small typed component. TypeScript 7
  was tested first and rejected because `vue-tsc 3.3.13` does not support its
  removed compiler subpath;
- Vite `8.3.5` and `@vitejs/plugin-vue` `6.0.10` for local build/dev proxy;
- a hand-written CSS time grid for the visual schedule (FullCalendar Vue `7.1.3`
  and `temporal-polyfill` were used until commit `0826cdf` and removed in SF-009);
- Playwright `1.64.1` and axe-core `4.14.0` for browser behavior/accessibility;
- Uvicorn `0.54.0` for the local API process used by the browser test.

No router, state library, component framework, CSS framework or client-side AI is
justified for this one-page POC.

## Acceptance criteria

- [x] Production build type-checks and bundles successfully.
- [x] Main flow loads real local API data and shows the terminal no-go first.
- [x] All three plans receive neutral treatment and are keyboard selectable.
- [x] Calendar and accessible assignment table update together.
- [x] Metrics remain separate and reason codes are inspectable.
- [x] Review creation and safe duplicate prevention/replay behavior are tested
  across browser and repository suites.
- [x] Loading, API error and review error states are browser-tested.
- [x] Axe reports no serious or critical violation in the tested main flow.
- [x] UI contains no booking, messaging or external-integration behavior.

## Observed evidence

`npm run build` completes TypeScript/Vue checking and creates the production
bundle. Five Playwright tests pass against real local Vite and Uvicorn processes:
neutral synchronized comparison, simulated review, API retry, review failure and
axe analysis. The axe result contains zero serious or critical violations. S5's
repository/API tests provide the complementary duplicate/replay proof.

## Rejection conditions

- CP-SAT is visually or verbally presented as accepted/recommended;
- a single score conceals the failed exposure guardrail;
- the calendar is the only representation of assignments;
- double submit can create multiple events;
- a control implies that a real appointment or message will be changed.
