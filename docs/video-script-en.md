# Video script — English primary

Target: 100–115 seconds. On-screen values must come from the committed UI or
commands. Repository/video URLs are added only after they exist.

## Script

**0–12s — Show two openings and two requests**

“After ten years working around healthcare software, I keep coming back to the
same engineering lesson: the useful solution is often not the loudest one. A
cancellation creates a small assignment problem. One request is flexible; the
other can use only the first opening.”

**12–30s — Select FIFO and local best-fit**

“FIFO and local best-fit are understandable baselines. In this controlled fixture,
both make the same local choice and recover 60 of 120 available minutes. Their
logic is explainable—but local logic cannot see the conflict across both slots.”

**30–46s — Select the CP-SAT controlled plan**

“A small constraint model moves the flexible request to the second opening and
places the constrained request in the first. It recovers 120 minutes, and all
three lexicographic phases prove optimal. No machine learning or embedded chatbot
is needed because this part of the problem is explicit assignment.”

**46–72s — Move to the development no-go panel**

“But a perfect fixture is not a responsible product claim. I tested four
longitudinal policies on 40 synthetic development seeds and measured repeated
exclusion separately from utilization. The closest candidate still degraded the
worst supported slice by 10.80 percentage points. The limit was declared at 10.
So I rejected it.”

**72–92s — Show architecture, tests and review controls**

“The domain stays independent from FastAPI, Vue and SQLite. IDs and input order
have counterfactual tests. Review events are append-only and idempotent. The UI
keeps the calendar beside an accessible table and puts the failed guardrail before
the attractive optimizer result.”

**92–110s — Record a simulated reject and show repository**

“This is a proof of engineering judgment, not automatic scheduling. It uses only
synthetic data, performs no booking or patient contact, and makes no clinical,
access or revenue claim. The repository includes the rejected experiments,
trade-offs and reproducible tests—not only the polished demo.”

## Required end card

`Synthetic POC · No external action · Development no-go · Not production ready`
