# SlotFit LinkedIn video production plan

## Objective

Create a concise, credible product explainer that lets a business audience
understand the scheduling problem before an engineering audience sees the design
choices. The video should position the author as a Senior Software Engineer who
chooses technology deliberately, validates uncomfortable results, and can explain
the work without hiding behind jargon.

## Audience

- Primary: Canadian software recruiters, engineering managers, and product-minded
  engineers in scheduling, healthcare SaaS, and operational software.
- Secondary: clinic operations and healthcare-technology professionals who
  understand the cost of an unused opening but do not need solver terminology.

## Source pattern

Reference: [Claude Makes a New Kind of Video — Full Tutorial](https://www.youtube.com/watch?v=Ge1B-Ok1Pfk).

Adopt only its workflow:

1. storyboard before motion;
2. reusable code-based visual style;
3. precise edits instead of full regeneration;
4. animation synchronized to the recorded narration;
5. a real finished example shown early.

The reference is a production-method inspiration. SlotFit must not copy its
script, frames, visual identity, music, examples, or source code.

## Format decision

### Selected: 16:9 editorial flat-vector explainer

This is preferred over vertical video because the decisive evidence is a
side-by-side calendar. In 9:16, both schedules would either become unreadable or
need to be shown sequentially, weakening the comparison. Produce the 16:9 master
first; create a square or vertical cut only after redesigning the calendar as
stacked beats.

### Visual ingredients

- 45% purpose-built vector animation of requests and openings;
- 40% screen recording of the implemented application;
- 15% simple decision and architecture graphics.

Do not use stock footage, generated people, medical imagery, animated code walls,
or a long terminal recording.

## Plain-language vocabulary

| Prefer | Avoid in the first 70% |
|---|---|
| scheduling rule | heuristic |
| opening or available time | interval/window object |
| flexible request | multi-eligible request |
| restricted request | scarcity-weighted entity |
| evaluate together | global optimization |
| known rules | hard constraints |
| repeatable answer | deterministic output |

`CP-SAT` appears only in the final 30%, after the audience already understands the
problem it solves.

## Deliberate technology message

The product experiment does **not** use a generative-AI model. This is a positive
engineering decision, not a limitation to apologize for.

The inputs and constraints are explicit, the feasible result must be repeatable,
and an invalid assignment must be provably rejected. Constraint programming fits
that job. A generative model would introduce variability and a harder validation
boundary without solving a missing-language-understanding problem.

Generative tools may assist video production or development, but they are not part
of the scheduling decision path. Keep that distinction explicit.

## Capture plan

1. Reset the local fixture to FIFO.
2. Capture the optimization replay once at normal speed and once at 75% speed.
3. Capture the side-by-side final state for a five-second hold.
4. Capture `Request alternative` and its local audit confirmation.
5. Capture the no-go strip with 10.80 p.p. and the limit at 10 visible.
6. Capture the passing test summary as a static crop.
7. Never capture personal browser tabs, notifications, secrets, or local filesystem paths.

## Audio and caption workflow

1. Record a human voice from the final script; do not synthesize Ricardo's voice.
2. Remove only obvious noise and long breaths; preserve natural pacing.
3. Produce a word-level timestamped transcript from the final take.
4. Synchronize the request movement and metric reveals to the exact words.
5. Export burned-in captions and upload a matching subtitle file to LinkedIn.

## Quality gates

- A viewer can explain the problem after watching without sound.
- The first technical acronym appears after 70% of the runtime.
- Every metric is visible in the committed application or tests.
- The 60-to-120-minute observation is labeled as a synthetic fixture result.
- The longitudinal no-go is visible and spoken.
- The video never claims clinical benefit, fairness, production readiness, revenue,
  improved access, or reduced wait time.
- The GitHub link resolves before publication.

## Files

- English narration: [`video-script-en.md`](video-script-en.md)
- Portuguese narration: [`video-script-pt.md`](video-script-pt.md)
- Shot-by-shot storyboard: [`video-storyboard.md`](video-storyboard.md)

