# Video storyboard

## Objective

Demonstrate Senior Software Engineer judgment through a concrete scheduling problem: recover useful time after a cancellation without allowing a locally efficient rule to repeatedly overlook harder-to-place requests.

The target length is 100–115 seconds. The demo uses synthetic data and never names
or imitates a specific company. Final narration is maintained in
[`video-script-en.md`](video-script-en.md) and
[`video-script-pt.md`](video-script-pt.md).

## Storyboard

| Time | Screen | English narration | Evidence shown |
|---|---|---|---|
| 0–12s | Implemented UI: two openings and two requests | Frame the global conflict and healthcare-software experience | Concrete problem before architecture |
| 12–30s | Select FIFO, then local best-fit | Both recover 60 of 120 minutes | Understandable baselines and local limitation |
| 30–46s | Select CP-SAT | The controlled plan recovers 120 minutes with three optimal phases | Constraint programming is justified by global assignment, not hype |
| 46–72s | Scroll to the no-go panel | Four development candidates were tested; V4 reached 10.80 p.p. against a fixed 10 p.p. limit and was rejected | Attractive fixture result is separated from longitudinal acceptance |
| 72–92s | Show architecture, table fallback and tests | Explain framework boundaries, counterfactuals and accessibility | Senior engineering judgment and restraint |
| 92–110s | Record a simulated reject; show repository | No external action, synthetic-only evidence and no clinical/access/revenue claim | Human control and reproducibility |

## Portuguese adaptation

The Portuguese version should preserve the same evidence and change only the narration, not the claims:

> “Um cancelamento parece apenas um horário vazio, mas operacionalmente é um pequeno problema de restrições. FIFO e melhor encaixe são baselines compreensíveis, porém ambos carregam uma política. Por isso, eu só considero uma estratégia melhor quando ela respeita as restrições, melhora a utilização e não ultrapassa limites previamente definidos de espera e exclusão recorrente. Esta POC usa apenas dados sintéticos e apoia uma decisão humana; ela não agenda, não contata pacientes e não infere prioridade clínica.”

## Recording rules

- Show the real-life problem in the first frame.
- Use only values produced by a committed command or evaluation artifact.
- Record the implemented UI; do not substitute an unlabelled mockup.
- Include one failed or rejected case; do not present a perfect system.
- Keep identifiers and data visibly synthetic.
- Put the architecture after the viewer understands the problem.
- End with the claim boundary and the repository, not a marketing promise.

## Claims allowed after the S7 gate closed

- “In the global-conflict fixture, both greedy baselines recover 60 minutes and the
  controlled CP-SAT plan recovers 120 minutes.”
- “Four candidates were evaluated on 40 synthetic development seeds and rejected
  under the fixed guardrail.”
- “V4 reached 10.80 p.p. against the predeclared 10 p.p. maximum.”
- “Calibration and the final frozen evaluation were not run because no candidate
  was eligible.”

Do not claim that SlotFit is fairer, increases clinic revenue, reduces wait time,
improves access or benefits patients. Those statements require evidence the
project does not have.
