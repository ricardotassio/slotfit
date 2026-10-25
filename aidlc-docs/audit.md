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

## Open decisions

- Exact fairness guardrail after inspecting the development distribution.
- OR-Tools objective weights before the frozen test set.
- Public repository license before publication.

