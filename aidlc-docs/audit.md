# AI-DLC audit

## 2026-10-25 — Repository inception

- Created as a separate local Git repository.
- Public target: vendor-neutral scheduling experiment.
- Decision: build SlotFit before SafeHandoff Lab.
- Decision: no remote repository or publication in this stage.
- Decision: use a modular monolith and keep the domain independent from frameworks.
- Decision: implement FIFO and best-fit before OR-Tools.
- Decision: use standard-library dataclasses in the first domain Bolt; Pydantic enters at the API boundary.
- Decision: no ML, LLM, message delivery or real scheduling integration.

## 2026-10-25 — Fairness and public narrative contract

- Decision: synthetic data will be used to expose assumptions and test invariants, not to claim absence of bias.
- Decision: fairness is operationally scoped to repeated exclusion across duration, availability, resource need, wait age and notice requirement.
- Decision: demographic fairness is outside the evidence boundary of the synthetic POC.
- Decision: decision attributes and audit-only slice labels remain separate.
- Decision: utilization gains cannot override hard constraints or predeclared starvation and worst-slice guardrails.
- Decision: objective weights and guardrails are frozen before the final test run.
- Decision: the video must show one failed or rejected case and state the human decision boundary.
- Evidence plan: [`../docs/fairness-and-bias-plan.md`](../docs/fairness-and-bias-plan.md) and [`../docs/video-storyboard.md`](../docs/video-storyboard.md).

## Open decisions

- Public repository license before publication — resolved in SF-008 (MIT, see `LICENSE`).

## 2026-10-25 — SF-003 design gate

- Decision: CP-SAT is justified only by a multi-slot global assignment conflict,
  not by the original single-interval example.
- Decision: pin `ortools==9.15.6755` when the dependency enters.
- Decision: use lexicographic recovered-minutes, requests-served and wait-age
  phases; do not use a blended tunable score.
- Decision: keep repeated-exclusion guardrails outside the first solver objective.
- Decision: define a controlled starvation event at three compatible opportunities
  without plan exposure and report sensitivity at two and four.
- Decision: use one worker, fixed seed, deterministic-time bound and wall-time
  ceiling; require `OPTIMAL` in every phase for an optimized claim.
- Decision: mint 400 final frozen seeds only after configuration and guardrails are
  committed. Previously exercised seeds remain regression-only.
- Evidence: the dependency entered only after the multi-slot baseline tests failed
  and then passed independently; Python is pinned to 3.12 and OR-Tools to
  `9.15.6755`.

## 2026-10-25 — Cross-agent specification workflow

- Decision: `AGENTS.md` is the canonical repository instruction file for Codex and Claude Code.
- Decision: `CLAUDE.md` imports `AGENTS.md` rather than duplicating project rules.
- Decision: specs under `specs/` own bounded implementation contracts; AI-DLC files own lifecycle state and traceability.
- Decision: read-only spec, risk and test reviewer roles are available in both agent environments.
- Decision: no model is pinned in repository configuration; the active environment chooses an available model.
- Decision: SF-001 initially remained in verification until progression was
  explicitly authorized; the teach-back remains recorded rather than silently
  treated as complete.

## 2026-10-25 — S1 progression and SF-002 implementation

- Decision: accept S1 for progression with a non-blocking personal teach-back
  follow-up; do not label it `Done`.
- Decision: use SHA-256-derived deterministic choices instead of a runtime random
  number generator so replay depends only on seed, version and field identity.
- Decision: register disjoint development, calibration, regression and challenge
  seed sets before optimizer work.
- Decision: keep operational audit slices in the manifest and outside `Scenario`,
  which is the strategy input.
- Decision: join audit metadata only in `slotfit.evaluation`, after a plan exists.
- Decision: report invalid selections as hard-constraint violations.
- Decision: do not emit simulated waiting or starvation from a single event. A
  longitudinal model is required before those measurements are meaningful.
- Decision: model repeated exposure as deterministic compatible-opportunity rounds,
  not as elapsed patient time or a real clinic calendar.
- Decision: remove a plan-exposed request before the next controlled round so one
  synthetic identity cannot receive repeated objective credit.
- Decision: emit compatible opportunities missed and first exposure round, but do
  not choose a starvation threshold inside SF-002.
- Decision: use registered development seed `1101` for the demonstrable generated
  and longitudinal examples; do not use frozen-test outcomes for configuration.
- Correction: the `3101`–`3104` seeds were exercised in routine engineering tests,
  so they are regression seeds, not a valid final frozen set. The real frozen
  manifest will be minted only after SF-003 configuration and guardrails are
  immutable.

## 2026-10-25 — SF-003 development decision

- Decision: operationalize an exposure deficit as `max(overall exposure - slice
  exposure, 0)` while retaining the signed gap in report output.
- Decision: a baseline slice may influence pass/fail only when it independently
  meets the predeclared support of 30 eligible opportunities.
- Decision: reject the first CP-SAT candidate because its worst supported
  exposure-shortfall degradation is 12.58 percentage points, above the unchanged
  10-point limit.
- Decision: do not enter calibration, freeze configuration or mint final seeds.
- Next hypothesis: use per-request compatible-opportunity debt, never audit-only
  slice labels, to make the longitudinal policy exposure-aware.

## 2026-10-25 — Bolt card catalog

- Decision: document S1–S8 with a common learning-card contract covering purpose,
  mechanics, critical complexity assessment, evidence/DoD and interview defense.
- Decision: distinguish implemented evidence (S1–S3) from roadmap contracts
  (S4–S8); a future card never implies existing functionality.
- Decision: keep the cards under `docs/bolts/` and link the catalog from the README
  and the canonical execution plan.
- Verification: all relative links resolve, `git diff --check` passes and the
  unchanged implementation suite remains at 46 passing tests.

## 2026-10-25 — Exposure-debt V2 decision

- Decision: preserve V1 and identify V2 separately rather than rewriting historical
  evidence.
- Decision: exposure debt is request-level compatible misses only; no audit slice
  may enter the optimizer.
- Observation: V2 changed zero selections across 40 development seeds and did not
  improve the failed slice guardrail.
- Decision: reject V2 and diagnose the efficiency/exposure feasible frontier before
  adding another objective or changing its priority.

## 2026-10-25 — Primary-optimal alternative diagnosis

- Decision: enumerate primary-optimal assignments from decision data before joining
  audit slices, preserving the decision/audit boundary.
- Observation: 34 of 200 rounds have residual primary-optimal choice; the failing
  moderate-notice slice has 9 local additional exposures of capacity.
- Limitation: local alternatives along the V2 cohort path are not a globally
  optimized longitudinal policy.
- Decision: test placement scarcity as a label-free V3 residual signal before
  allowing any efficiency trade-off.
- Verification: 57 tests passed and the standalone diagnostic JSON was generated
  and parsed successfully.

## 2026-10-25 — Placement-scarcity V3 decision

- Decision: compute scarcity from current eligible interval counts, never from an
  audit slice label.
- Observation: V3 changes 17 of 200 rounds and improves the worst degradation by
  0.23 percentage point while preserving primary efficiency.
- Decision: reject V3 because 12.35 p.p. remains above the 10 p.p. guardrail.
- Next gate: measure an explicit development-only efficiency/exposure frontier;
  do not add another residual heuristic without evidence.

## 2026-10-25 — Local frontier decision

- Decision: predeclare 100%, 95%, 90% and 80% local floors before observing the
  frontier.
- Observation: the highest passing target-slice floor is 90%; its realized
  aggregate recovery is 99.43%, with a 45-minute cost and three added exposures.
- Limitation: audit labels select oracle plans post hoc and the subsequent cohort
  remains V3's path.
- Decision: use the result only to specify a label-free 90%-floor V4 candidate on
  development; do not enter calibration.

## 2026-10-25 — Bounded-recovery V4 decision

- Observation: V4 improves worst supported degradation from 12.35 to 10.80 p.p.
  but fails the fixed 10 p.p. guardrail.
- Observation: realized mean utilization is 95.71%, showing the local fixed-path
  oracle cannot predict the full longitudinal path directly.
- Decision: reject V4, keep calibration closed and require a methodology/no-go
  review before any further objective or threshold change.

## 2026-10-25 — SF-003 terminal no-go

- Decision: close SF-003 as a valid negative experiment after four candidates
  failed the unchanged worst-supported-slice guardrail.
- Decision: do not create V5, enter calibration, freeze a configuration or mint a
  final frozen set under the current research line.
- Decision: allow S4 to expose deterministic demonstrations and the rejected
  research decision, but never present V4 as an accepted recommendation.
- Evidence: [`../docs/methodology-no-go-review.md`](../docs/methodology-no-go-review.md).

## 2026-10-25 — SF-004 read-only API

- Decision: expose only deterministic synthetic demos and a checked-in terminal
  research decision; do not accept arbitrary scenario or identity payloads.
- Decision: keep FastAPI/Pydantic in adapter modules and preserve the
  framework-independent domain core.
- Decision: pin FastAPI `0.162.0`, Pydantic `2.14.1` and HTTPX2 `2.13.0` for a
  reproducible API/test boundary.
- Verification: seven API contract tests, in-process smoke checks and 70 full-suite
  tests pass without network, database or external actions.

## 2026-10-25 — SF-005 append-only simulated review

- Decision: use SQLite for the single-user local POC and defer PostgreSQL until a
  shared deployment or measured contention exists; see ADR-0003.
- Decision: make review events immutable with database triggers and enforce
  idempotency through a unique constraint plus winner comparison after races.
- Decision: the only write endpoint records a simulated human review with
  `external_action: none`; it cannot book, message or mutate a schedule.
- Verification: ten focused persistence/API tests and 80 full-suite tests pass,
  including two-connection uniqueness and direct update/delete rejection.

## 2026-10-25 — SF-006 neutral comparison UI

- Decision: put the terminal no-go before plan controls and use neutral,
  baseline-first plan ordering with separate metrics.
- Decision: render assignments in both FullCalendar and a semantic table; the
  calendar is never the only evidence representation.
- Observation: TypeScript 7.0.2 is incompatible with `vue-tsc 3.3.13`; pin the
  tested TypeScript 6.0.3 instead of patching compiler internals.
- Verification: production build passes; five Playwright tests pass against real
  local API/UI processes; axe reports zero serious or critical violations in the
  main flow.

## 2026-10-25 — SF-007 frozen-evaluation gate

- Decision: close S7 without executing calibration or the 400-seed final set
  because no SF-003 candidate passed development.
- Decision: treat the nonexistent final manifest as the correct evidence-preserving
  outcome, not incomplete implementation.
- Reopening rule: require a new hypothesis and fresh development/calibration
  registries; V4 may not be relabeled or tuned against the same evidence.

## 2026-10-25 — SF-008 hardening and communication

- Decision: use lockfile-based setup without Docker and add least-privilege CI
  with no secrets or external services.
- Decision: license the repository under MIT and document the local-only security
  boundary and combined technical/evidence-integrity risk review.
- Decision: keep English and Portuguese video/post materials numerically aligned
  and automatically require synthetic-data, no-go and no-external-action language.
- Verification: frozen dependency sync/install succeeded; `make verify` passed 84
  Python tests, API smoke, production web build and five Playwright tests.
- External state: no Git remote exists; nothing was pushed, deployed or published.

## 2026-10-26 — Cycle 2 proposal (not approved)

- Observation: the working tree had an uncommitted rewrite of the video scripts
  that breaks `test_publication_contract` (English regex does not accept
  "against a limit of 10"); 83 of 84 Python tests pass, 5 Playwright tests pass.
- Observation: commits `0826cdf` and `5fb9094` changed the UI after SF-008 was
  marked Done without a spec, removed FullCalendar from the component while
  docs and `package.json` still reference it, and compressed `App.vue`.
- Decision: propose a governance-reconciliation Bolt (SF-009) before any new
  feature, then narrative/explanation Bolts SF-010 to SF-014; see
  [`refinement-plan-2026-10.md`](refinement-plan-2026-10.md).
- Decision: financial loss may not be computed or claimed by the system; the
  narrative shows undelivered capacity. Any viewer-entered monetary hypothesis
  is a human decision (D1) gated by the risk reviewer.
- Decision: constraint programming is presented as deterministic symbolic AI
  chosen for problem structure; generative AI stays outside the decision path.
- Gate: `blocking-approval` by Ricardo; nothing in cycle 2 is implemented.

## 2026-10-26 — Cycle 2 approval and SF-009 start

- Decision: Ricardo approved the cycle 2 plan and authorized SF-009. Decisions
  D1–D5 are recorded as the plan's recommendations (no money in any surface,
  functional request labels, FullCalendar removed, English-only UI, S7 closed)
  pending any contrary instruction.
- Decision: SF-009 reconciles the publication test, the unspecified UI
  redesign, the orphaned FullCalendar dependency and stale status documents
  before any cycle 2 feature.
- Gate label: `blocking-approval` given in chat; recorded here.

## 2026-10-26 — SF-009 closed

- Decision: FullCalendar and temporal-polyfill removed (D3); the hand-written
  CSS time grid is the implemented evidence surface.
- Decision: the SF-008-era UI redesign is re-evaluated under SF-006, not merely
  recorded; asymmetric plan treatment is replaced by one shared style, a signed
  difference and factual footers, enforced by a new browser test.
- Decision: the publication contract accepts "limit of 10" wording; the
  guided-story video documents are committed.
- Verification: `make verify` passes (84 Python tests, API smoke, typed build,
  six Playwright tests); no source line over 160 characters; worktree clean.
- Next: SF-010 (clinic-day fixture and explanations) awaits explicit start.

## 2026-10-26 — SF-010 start

- Decision: Ricardo authorized SF-010 ("siga para 10").
- Decision: the story fixture is a superset of `multi-slot-counterexample-1500`
  (same openings and requests plus a Room B request), seed 1600, hand-built and
  outside every evaluation registry.
- Decision: display-only context (`DayContext`) lives in its own module and is
  barred from decision modules by a source-scan test.
- Decision: explanations are a closed map over the six reason codes; copy avoids
  audit-band vocabulary; `SCHEMA_VERSION` 1.0 → 1.1 for the additive fields.

## 2026-10-26 — SF-010 closed

- Verification: `make verify` passes with 98 Python tests, API smoke, typed
  build and six Playwright tests; worktree clean after the closing commit.
- Observation: the story fixture reproduces the counterexample numbers exactly
  (60/60/120), so the story UI can read every number from the API.
- Next: SF-011 (three-screen story mode in the web app) awaits explicit start.

## 2026-10-26 — SF-015 start

- Decision: Ricardo authorized a code-organization and narrative Bolt before
  SF-011 ("carregue as skills necessarias de SOLID, Clean Code, GRASP, Object
  Calisthenics, para organizar o codigo... tire screenshots da tela e suba no
  readme... use a documentacao para explicar as camadas e cada etapa do
  experimento"). Opened as SF-015 so the cycle-2 numbering is untouched.
- Decision: refactors are behaviour-preserving only; the existing 98 Python
  tests, API smoke, typed build and Playwright tests are the safety net.
- Decision: screenshots come from a Playwright script, never by hand, and every
  capture carries the no-go strip (SF-014 capture rule applied early).
- Decision: the README names no employer or company; the only biographical fact
  is ten years building healthcare software.

## 2026-10-26 — SF-015 closed

- Verification: `make verify` passes with 99 Python tests, API smoke, typed
  build and six Playwright tests; before/after diffs of the development report,
  multi-slot demo, alternative diagnostic and exposure frontier are identical
  except solver wall time.
- Observation: nine refactor commits, no plan, metric, reason code or schema
  changed; `optimizer.py` grew to 500 lines of smaller functions.
- Observation: README and architecture now read as a sequential study; six
  screenshots generated by `make screenshots`, each with the no-go strip.
- Next: SF-011 (three-screen story mode) awaits explicit start. Remote creation
  and publication remain user-owned external actions.

## 2026-10-26 — Remote created

- Decision: Ricardo authorized the remote ("coloque no meu repositorio"). The
  private repository `ricardotassio/slotfit` was created under his personal
  GitHub account and `main` pushed; the repository URL replaced the placeholder
  in both LinkedIn drafts and the storyboard. `{VIDEO_URL}` stays until the
  video is uploaded. Making the repository public remains his decision.

## 2026-10-26 — SF-016 start

- Decision: Ricardo authorized a layered package layout, a Docker reproduction
  path and architecture documentation ("faca a atualizacao no repositorio,
  garanta que tudo esteja funcionando e rode os testes para que nao haja
  regressao, crie um ambiente com o docker para facilitar a replicacao, e
  documente a arquitetura utilizada").
- Decision: hexagonal layout (domain, application, solver, research, adapters,
  composition) chosen over feature folders because the project has one feature
  and the meaningful split is by responsibility; no interface per dependency.
- Decision: the architecture test is written first and must fail on the flat
  layout before any module moves.
