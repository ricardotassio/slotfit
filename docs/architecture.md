# Proposed architecture

Current evidence-backed flow:

```text
single- or multi-slot scenario
  -> immutable domain objects
  -> eligibility evaluation
  -> chronological FIFO or best-fit strategy
  -> candidate plan
  -> CLI JSON output
```

Current optimizer boundary:

```text
multi-slot scenario
  -> shared eligibility evaluations
  -> CP-SAT eligible-pair variables
  -> recovered minutes (phase 1)
  -> requests served (phase 2)
  -> wait-age tie-break (phase 3)
  -> structured plan + phase evidence
```

Planned application flow, explicitly not implemented yet:

```text
Vue calendar
  -> FastAPI/Pydantic
  -> eligibility service
  -> FIFO | best-fit | CP-SAT
  -> explanation builder
  -> human review
  -> PostgreSQL audit event
```

## Boundaries

- Domain objects do not import web, database or solver frameworks.
- Strategies receive a scenario and return a plan.
- Eligibility returns reason codes; it does not silently filter.
- Greedy strategies evaluate every request/interval pair and assign a request at
  most once.
- Persistence and HTTP will be adapters around the domain.

## Failure stories

- Invalid time window: reject construction.
- No eligible request: return an empty plan with exclusions.
- Solver limit reached: return its explicit status and never report a baseline as
  the optimized plan.
- No feasible optimized plan: return `INFEASIBLE`; do not relax hard constraints.
