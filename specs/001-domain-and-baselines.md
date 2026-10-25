# SF-001 — Deterministic domain and baselines

- Status: Verification
- AI-DLC mapping: Bolt S1
- Owner: repository maintainer
- Depends on: accepted problem contract

## Problem

Before optimization, the project needs a small scenario whose feasibility decisions and baseline trade-offs are deterministic, explainable and executable without external services.

## In scope

- timezone-aware time windows;
- immutable scenario, interval, request, evaluation, assignment and plan values;
- stable eligibility reason codes;
- FIFO and local best-fit over the same single-interval scenario;
- a CLI that produces synthetic, machine-readable output;
- deterministic unit tests.

## Non-goals

- seeded population generation;
- fairness claims or aggregate metrics;
- multiple-interval optimization;
- API, persistence, UI, messaging or external integration.

## Behavioral contract

Given `demo-1400`:

- FIFO selects `WR-001`, recovering 30 minutes;
- local best-fit selects `WR-002`, recovering 75 minutes;
- `WR-003` is ineligible with `REQUIRED_ROOM_UNAVAILABLE`;
- a request without communication consent is never selected;
- no automatic action occurs.

The fixture demonstrates contracts only. A different seed currently changes only the scenario identifier and must not be described as a different generated population.

## Acceptance criteria

- [x] Domain rejects naive or invalid time windows.
- [x] Eligibility exposes stable reason codes.
- [x] Both strategies consume the same scenario.
- [x] `make test` passes without a network service.
- [x] `make demo` emits the expected plan values and `automatic_action: none`.
- [ ] Ricardo can explain why FIFO and best-fit encode different policies.
- [ ] Spec, traceability and AI-DLC review log agree that no fairness conclusion is supported yet.

## Required evidence

- Test command: `make test`.
- Demonstration command: `make demo`.
- Observed values recorded in the review log when the human gate closes.

## Failure modes

- Treating the fixture seed as evidence of distributional variation.
- Treating higher recovered minutes in one example as proof of a superior policy.
- Allowing an ineligible request into the candidate set.
- Hiding exclusions without a reason code.

## Exit and handoff

Close SF-001 only after the human teach-back and documentation alignment. Then activate SF-002; do not jump directly to OR-Tools.
