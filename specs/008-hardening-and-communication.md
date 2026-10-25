# SF-008 — Reproducibility hardening and bilingual communication

- Status: Done
- AI-DLC mapping: Bolt S8
- Depends on: SF-006 and SF-007 gate outcome

## Purpose

Turn the local POC into a reviewable engineering artifact and an honest video/post
package. Communication must point to observed evidence, including the terminal
negative result, and must not imply publication, production readiness or clinic
impact.

## Deliverables

- clean setup/runbook covering Python, Node, browser install, API and UI;
- least-privilege CI for Python tests, web build and browser tests;
- threat/risk review and security-reporting note;
- public MIT license;
- automated publication-contract tests for required limitations;
- final English video script and LinkedIn draft;
- faithful Portuguese video script and LinkedIn draft;
- repository/status documentation updated to the actual S1–S8 outcome.

No repository, video or post is uploaded. Publication and creation of a remote
remain separate user actions.

## Claim contract

Allowed:

- two greedy baselines recover 60 minutes in the global-conflict fixture while
  the V1 CP-SAT plan recovers 120 minutes with three optimal phases;
- all four longitudinal candidates were rejected on development evidence;
- V4's worst supported degradation was 10.80 p.p. against a fixed 10 p.p. limit;
- 80 Python tests, five browser tests and the production web build pass at the
  recorded project state;
- the system uses only synthetic data and records simulated review events with
  no external action.

Not allowed:

- claims of revenue, access, wait-time or patient-safety improvement;
- “bias-free”, “fair”, “production-ready” or clinically validated language;
- presenting V1's fixture result as acceptance of V4 or longitudinal success;
- implying that the POC books, contacts or reprioritizes a person.

## Risk-review scope

Review synthetic-data leakage, accidental real identifiers, injection into review
fields, denial of service, local database permissions, dependency/CI supply chain,
presentation bias, evidence leakage and unsupported claims. Every risk receives a
current mitigation and a boundary for future shared deployment.

## Acceptance criteria

- [x] Fresh dependency sync/install commands are lockfile-based and documented.
- [x] Python tests, API smoke, web build and five Playwright tests pass.
- [x] CI uses read-only repository permissions and no secrets/services.
- [x] Threat/risk review covers technical and evidence-integrity risks.
- [x] Automated tests require no-go and safety disclosures in all public drafts.
- [x] English and Portuguese scripts use the same numbers and claim boundaries.
- [x] README links every primary evidence and runbook document.
- [x] License and security note exist.
- [x] Git worktree is clean after the final verification commit.
- [x] Nothing is pushed, deployed or published.

## Observed evidence

Locked `uv sync --frozen` and `npm ci` complete successfully. `make verify` then
passes 84 Python tests, the in-process API smoke check, the typed production web
build and five Playwright tests against local Uvicorn/Vite processes. Publication
contract tests verify bilingual numeric parity and required no-go, synthetic-data
and no-external-action disclosures. No remote is configured; no push, deployment
or publication occurred.
