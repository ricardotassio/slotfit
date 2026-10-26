# SlotFit video storyboard

## Chosen template

**Editorial flat-vector product explainer with a real UI demo.**

The reference video demonstrates a code-first animation workflow: approve a
storyboard first, reuse a working visual system, and synchronize motion to a
word-level voice-over transcript. SlotFit should borrow that production method,
not the reference video's subject, narration, or visual identity.

This template is the best fit because:

- the wide calendar comparison remains readable in a 16:9 frame;
- vector motion makes the scheduling conflict visible without stock footage;
- the real interface provides evidence instead of an invented product mockup;
- a restrained cream, navy, teal, and amber palette matches the implemented UI;
- every movement can be reproduced and edited precisely by code.

Avoid glassmorphism, photorealistic AI video, talking-head introductions, generic
healthcare stock footage, and animated technology logos.

## Structure: problem first, engineering last

| Time | Share | Visual beat | Business message | Evidence |
|---|---:|---|---|---|
| 0–6s | 6% | Gap appears in the animated agenda | A rule can create waste | Empty 60-minute opening |
| 6–20s | 13% | Two openings and two requests enter | Restrictions overlap | Flexible A/B; restricted A only |
| 20–38s | 17% | First-come rule fills A; B remains empty | A reasonable local choice can block the whole schedule | 60 of 120 minutes assigned |
| 38–57s | 18% | Flexible request moves to B; restricted enters A | Evaluate the schedule as a whole | 120 of 120 minutes in this fixture |
| 57–73s | 15% | Human review step | Decision support, not automation | No external action |
| 73–86s | 12% | Rules-to-solver decision graphic | Why a deterministic algorithm, not generative AI | Explicit/testable constraints |
| 86–97s | 10% | Four engineering layers | Reproducibility and replaceability | Rules, API, UI, append-only audit |
| 97–105s | 8% | No-go strip and repository | The failed result is part of the evidence | 40 runs; 10.80 p.p. vs limit at 10 |

## Motion language

- Use position to explain assignment: request cards physically move into openings.
- Use a single amber hatch for unused time and teal fill for assigned time.
- Animate once per beat; never keep decorative elements moving.
- Keep cuts on narration keywords: “first,” “now,” “together,” “person,” and
  “deliberately.”
- Use 250–450 ms transitions for UI elements and 700–1,000 ms for the main request
  movement.
- Show one sentence or one metric at a time. No paragraph cards.

## Frame design

- Master: 1920×1080, 30 fps, H.264, 12–18 Mbps.
- Safe area: keep text inside 120 px horizontally and 80 px vertically.
- Display type: Georgia or a metrically compatible serif used in the web demo.
- Interface type: Inter/system sans-serif.
- Captions: maximum two lines, 42–48 px, high-contrast solid background.
- Sound: quiet UI ticks for placements and one soft confirmation tone when the gap
  closes; no synthetic “AI” sound effects.

## Storyboard approval gates

1. Approve these eight static beats before producing motion.
2. Record the final human voice-over.
3. Generate a word-level transcript from that exact audio.
4. Bind each animation cue to transcript timestamps.
5. Export a silent draft and confirm the story is understandable without audio.
6. Add voice, captions, and restrained sound effects.
7. Verify every number against the committed application and tests.

## End card

`SlotFit · Synthetic scheduling experiment`

`GitHub: {GITHUB_REPOSITORY_URL}`

`Synthetic POC · No booking · Development no-go`

Question: **Where would you draw the line between utilization and repeated exclusion?**

