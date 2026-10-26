# SlotFit video script — English primary

Target: **105 seconds**. English is the primary LinkedIn version for the Canadian
market. The first 73 seconds (about 70%) explain the recognizable business problem
and show the result. Only the final 32 seconds explain the engineering decisions.

Delivery: calm, curious and conversational. Average 135–145 words per minute.
Do not sound like an advertisement. Pause briefly when the 60-minute gap appears.

## Voice-over and direction

### 0–6s — Cold open: show the finished animation

**Voice-over**

“A cancellation does not always create wasted capacity. Sometimes the scheduling
rule creates it.”

**On screen**

- Start directly on the animated agenda; no logo introduction.
- Show the empty second opening, then freeze before it is recovered.
- Caption: `Two openings · Two requests · One avoidable gap`

### 6–20s — Make the business problem concrete

**Voice-over**

“Imagine two available one-hour openings. One request is flexible and can use
either one. The other request can only use the first. This is common in scheduling:
availability looks simple until the restrictions overlap.”

**On screen**

- Reveal two openings on the left and two request cards on the right.
- Add plain-language labels: `Flexible: A or B` and `Restricted: A only`.
- Avoid technical identifiers until the evidence section.

### 20–38s — Show why a reasonable local rule fails

**Voice-over**

“A first-come rule makes a perfectly understandable choice: it puts the flexible
request first. But now the restricted request has nowhere to go. The result is one
filled opening and a 60-minute gap—even though both requests could have fitted.”

**On screen**

- Animate the flexible request into opening A.
- Try to place the restricted request in B; show `Not compatible` instead of an
  error icon.
- Pulse the unused opening once. Do not loop.

### 38–57s — Reveal the candidate schedule

**Voice-over**

“Now evaluate both openings together. Preserve the only compatible opening for
the restricted request, and move the flexible one to the second. In this synthetic
example, assigned time goes from 60 to 120 minutes, using the same capacity.”

**On screen**

- Play the implemented optimization replay.
- End on the side-by-side calendars.
- Show only three values: `60 → 120 min`, `2 requests placed`, `0 external actions`.

### 57–73s — Translate the result into business value

**Voice-over**

“The point is not to automate care or make a clinical decision. It is to give an
operations team a clearer option before capacity disappears. The software proposes
a plan; a person still accepts, rejects, or asks for another one.”

**On screen**

- Scroll to the human review controls.
- Select `Request alternative`, then show the local audit confirmation.
- Caption: `Decision support, not automatic scheduling`.

## Final 30% — engineering decisions

### 73–86s — Why no generative AI

**Voice-over**

“I deliberately did not use generative AI here. The rules are explicit, the
answer must be repeatable, and every assignment must be testable. A small
constraint-solving algorithm is a better fit than a chatbot generating a
plausible answer.”

**On screen**

- Use a simple decision card:
  `Known rules → deterministic solver → explainable plan`.
- Cross out, subtly: `Prompt → generated recommendation`.
- Lower-third: `CP-SAT · deterministic constraint solving`.

### 86–97s — Show senior engineering judgment

**Voice-over**

“I kept the scheduling rules independent from the API and interface, added
counterfactual tests for input order and identifiers, and stored human reviews as
append-only events. That makes the prototype easier to challenge, reproduce, and
replace.”

**On screen**

- Animate four small blocks: `Rules`, `API`, `Interface`, `Audit`.
- Briefly show the passing test summary; never show terminal typing.

### 97–105s — Limitation, integrity and close

**Voice-over**

“The attractive demo is not the full result. Across 40 synthetic development
runs, the closest policy reached 10.80 percentage points against a limit of 10,
so I rejected it. The code, tests, and failed experiment are all in the repository.”

**On screen**

- Show the no-go strip, then the GitHub repository end card.
- Required footer: `Synthetic POC · No booking · Development no-go`.
- Final question: `Where would you draw the line between utilization and repeated exclusion?`

## Recording checklist

- Record the application at 1920×1080 and 100% browser zoom.
- Use hard-burned English captions plus an uploaded `.srt` file.
- Keep music at least 18 dB below narration; silence is acceptable.
- Never say “AI optimized,” “fair,” “more patients,” “revenue,” or “production ready.”
- Replace the repository placeholder only after the public URL works.

