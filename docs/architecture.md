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

Planned flow, explicitly not implemented yet:

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
- Solver unavailable in a future Bolt: baselines remain executable.
- No feasible optimized plan: return `infeasible`; do not relax hard constraints.
