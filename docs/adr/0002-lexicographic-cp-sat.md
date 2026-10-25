# ADR-0002 — Lexicographic CP-SAT for global slot assignment

- Status: Accepted
- Date: 2026-10-25

## Context

The single-interval fixture does not justify an optimizer. The multi-slot
counterexample introduces a global assignment conflict in which a locally sensible
choice can block the only feasible placement for another request.

A weighted blend of utilization, request count and waiting would be difficult to
explain and easy to tune after seeing favorable results. An unconstrained solver
runtime or parallel search would also weaken reproducibility.

## Decision

Use pinned OR-Tools CP-SAT only for multi-slot global assignment. Solve three
lexicographic integer objectives: recovered minutes, requests served and declared
wait-age score. Keep feasibility as hard constraints. Use one worker, a fixed seed,
bounded deterministic and wall time, and require `OPTIMAL` in every phase before
describing a result as optimized.

Evaluate repeated exclusion outside the solver through predeclared guardrails. Do
not add a fairness penalty to the first optimizer.

## Alternatives considered

- **Keep greedy strategies only:** rejected for the experiment because they cannot
  prove global optimality in the interacting-slot counterexample.
- **Weighted blended objective:** rejected because arbitrary weights can conceal
  trade-offs and invite post-result tuning.
- **ML ranking or an LLM:** rejected because this is a constrained assignment
  problem with explicit facts and no learned target.
- **LangGraph:** rejected because the workflow is deterministic and has no need for
  agentic orchestration.

## Consequences

- The reason for using CP-SAT is visible in one small scenario.
- Phase status and objective values are part of the evidence.
- A `FEASIBLE` result may be shown as limited but cannot support an optimality claim.
- The first optimizer may fail a repeated-exclusion guardrail; that failure must be
  reported rather than hidden or repaired through unplanned weight tuning.
- OR-Tools remains an adapter dependency; the domain and baselines stay executable
  without it.
