# Project instructions

## Product boundary

- Use synthetic data only.
- Never add real patient, clinic, provider or company data.
- Never send messages, book appointments or integrate with an external scheduling system.
- Never infer clinical urgency. A priority may only be an explicit synthetic input assigned by a human.
- Describe observed simulation results only; do not convert them into financial or clinical claims.

## Development workflow

- Follow `aidlc-docs/state.md` and implement one approved Bolt at a time.
- Update `aidlc-docs/audit.md`, `traceability.md` and `review-log.md` when a Bolt closes.
- Start with the simplest baseline and add complexity only when an experiment justifies it.
- Add an ADR for a dependency or architectural choice that materially changes operation, security or the experiment.
- Every behavior change needs an executable test and a documented failure mode.
- Keep the core domain independent from FastAPI, persistence and UI frameworks.

## Current scope

- The active unit is the deterministic domain and baseline strategies.
- Do not add OR-Tools, FastAPI, PostgreSQL, Vue, messaging, ML or cloud deployment until their Bolt is active.
- Keep commands reproducible through the Makefile.

