# SlotFit repository instructions

## Mission

Build a small, reproducible experiment that compares explainable scheduling strategies on synthetic clinic calendars. Optimize for Senior Software Engineer judgment: explicit contracts, simple baselines, measured trade-offs and honest failure reporting.

## Source of truth

Read these sources before changing code, in this order:

1. the active file under `specs/`;
2. `aidlc-docs/state.md` and `aidlc-docs/requirements.md`;
3. `docs/fairness-and-bias-plan.md` and `docs/architecture.md`;
4. relevant ADRs and existing tests.

If they conflict, stop implementation, identify the conflict and update the owning document before code. Do not copy requirements between files when a link is sufficient.

## Product and claim boundary

- Use synthetic data only.
- Never add real patient, clinic, provider or company data.
- Never send messages, book appointments or integrate with a real scheduling system.
- Never infer clinical urgency. A priority may only be an explicit synthetic human input.
- Never claim that a system is bias-free. Detect, measure and mitigate specified failure modes.
- Describe observed controlled results only; do not convert them into financial, access or clinical claims.
- A human owns every simulated scheduling choice.

## Spec-driven workflow

1. Select exactly one active spec and read its dependencies.
2. Perform a read-only preflight: current behavior, affected files, risks and commands.
3. Start with the smallest failing test or invariant in the spec.
4. Implement only enough behavior to pass it.
5. Refactor without expanding scope.
6. Run focused tests, then `make test`; run `make demo` when observable output changes.
7. Record observed evidence in the spec and update AI-DLC traceability when the gate closes.
8. Stop at the next spec boundary. Do not silently begin a later Bolt.

No spec may be marked `Done` while an acceptance criterion, required evidence item or human gate is unresolved.

## Bias and fairness controls

- Keep decision attributes separate from audit-only slice metadata.
- Do not add demographic fields or proxies to the objective.
- Evaluate utilization together with selection, exposure, waiting, starvation and worst-slice results.
- Add metamorphic tests for opaque identifiers, input order and irrelevant ineligible records.
- Freeze thresholds, distributions and objective settings before the final test run.
- Reject a strategy that violates a hard constraint or a predeclared guardrail, even if utilization improves.

## Engineering conventions

- Python 3.12; typed standard-library domain core.
- Keep domain behavior independent from FastAPI, persistence and UI frameworks.
- Prefer pure functions and immutable domain values.
- Use stable reason codes instead of free-form control flow.
- Every behavior change requires an executable test and a documented failure mode.
- Add an ADR only for a material dependency, architecture, safety or evaluation decision.
- Add dependencies only in the Bolt that demonstrates their need.

## Agent roles

- `spec-reviewer`: checks scope, acceptance criteria and traceability before implementation.
- `risk-reviewer`: challenges bias, privacy, safety, leakage and claim boundaries.
- `test-reviewer`: checks invariants, regressions and evidence after implementation.

These roles are read-only reviewers. The primary agent or worker implements the approved spec. Reviewer output is advice until incorporated into the repository by the primary agent.

## External and Git actions

- Do not read secrets or commit `.env` files.
- Do not push, publish, deploy, contact external systems or mutate real data without explicit authorization.
- Preserve user changes and do not use destructive Git or filesystem commands.
