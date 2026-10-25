# Video storyboard

## Objective

Demonstrate Senior Software Engineer judgment through a concrete scheduling problem: recover useful time after a cancellation without allowing a locally efficient rule to repeatedly overlook harder-to-place requests.

The target length is 90–110 seconds. The demo uses synthetic data and never names or imitates a specific company.

## Storyboard

| Time | Screen | English narration | Evidence shown |
|---|---|---|---|
| 0–8s | Calendar: a cancellation creates a 60-minute gap beside a 30-minute opening | “A cancellation looks like an empty slot. Operationally, it is a small constraint problem.” | Concrete problem before architecture |
| 8–20s | Three synthetic wait requests appear with availability, duration and resource needs | “The first eligible person is not always the plan that recovers the most usable time. But maximizing minutes alone can repeatedly leave harder requests behind.” | Feasibility is distinct from optimization and fairness |
| 20–38s | Run FIFO and local best-fit on the same scenario | “FIFO recovers 30 minutes. Local best-fit recovers 75 here. Both are understandable baselines, and both encode a policy.” | Actual measured values from `make demo` |
| 38–55s | Architecture flow: scenario → eligibility → strategies → explanations → human review | “I kept the core deterministic and framework-independent, with stable reason codes and a human decision boundary.” | Engineering structure and restraint |
| 55–73s | Fairness dashboard mock or implemented view: utilization, exposure, wait and worst slice | “The next candidate only qualifies if it improves utilization without crossing predeclared starvation and worst-slice guardrails.” | Separate metrics; do not show a composite magic score |
| 73–88s | A counterfactual test passes; one stress scenario or rejected strategy fails | “Changing an opaque ID must never change the plan. And if a strategy wins on utilization but fails the fairness gate, I reject it.” | Invariance plus an honest failure |
| 88–101s | Reviewer compares plans and chooses or rejects one | “This is decision support, not automatic booking. No patient contact, urgency inference or schedule mutation is part of the POC.” | Human control and safety boundary |
| 101–110s | Repository structure, test command and evaluation artifact | “The repository contains the assumptions, tests, frozen scenarios and trade-offs—not just a polished demo.” | Reproducible GitHub artifact |

## Portuguese adaptation

The Portuguese version should preserve the same evidence and change only the narration, not the claims:

> “Um cancelamento parece apenas um horário vazio, mas operacionalmente é um pequeno problema de restrições. FIFO e melhor encaixe são baselines compreensíveis, porém ambos carregam uma política. Por isso, eu só considero uma estratégia melhor quando ela respeita as restrições, melhora a utilização e não ultrapassa limites previamente definidos de espera e exclusão recorrente. Esta POC usa apenas dados sintéticos e apoia uma decisão humana; ela não agenda, não contata pacientes e não infere prioridade clínica.”

## Recording rules

- Show the real-life problem in the first frame.
- Use only values produced by a committed command or evaluation artifact.
- Label future UI frames as mockups until they are implemented.
- Include one failed or rejected case; do not present a perfect system.
- Keep identifiers and data visibly synthetic.
- Put the architecture after the viewer understands the problem.
- End with the claim boundary and the repository, not a marketing promise.

## Claims allowed before the frozen evaluation

- “The current fixture demonstrates deterministic eligibility and two baselines.”
- “In this fixture, FIFO recovers 30 minutes and local best-fit recovers 75 minutes.”
- “The fairness evaluation is specified but not yet executed.”

Do not yet claim that SlotFit is fairer, increases clinic revenue, reduces wait time or improves access. Those statements would require evidence the current project does not have.
