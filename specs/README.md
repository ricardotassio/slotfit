# SlotFit specifications

Specifications are the implementation contract between product intent, code and evidence. They are intentionally smaller than the project roadmap.

## Status vocabulary

- `Draft`: incomplete or still contains unresolved design choices.
- `Ready`: bounded, traceable and eligible for implementation.
- `In progress`: implementation has started.
- `Verification`: code exists; required evidence or review remains.
- `Accepted with follow-up`: progression was explicitly authorized after machine
  evidence passed, while a non-safety learning exercise remains open.
- `Done`: every acceptance criterion and gate has observed evidence.

## Order

| Spec | Status | Purpose |
|---|---|---|
| [`SF-001`](001-domain-and-baselines.md) | Accepted with follow-up | Validate the deterministic domain and first baselines already implemented |
| [`SF-002`](002-scenarios-and-fairness-controls.md) | Done | Add real seeded variation, audit-only slices and invariance controls |
| [`SF-003`](003-optimizer-and-evaluation.md) | Done — terminal no-go | Compared four optimizer candidates; none passed the fixed development guardrails |
| [`SF-004`](004-api-boundary.md) | Ready | Expose deterministic demos and the terminal research decision through a read-only API |

## Working rule

Only one spec may be active. Future specs may document dependencies and open decisions, but must not authorize early implementation.

The roadmap remains in [`../aidlc-docs/execution-plan.md`](../aidlc-docs/execution-plan.md). Safety and fairness definitions remain in [`../docs/fairness-and-bias-plan.md`](../docs/fairness-and-bias-plan.md).
