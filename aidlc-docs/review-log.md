# Review and teach-back log

No Bolt has been approved yet.

## 2026-10-25 — SF-001 verification evidence

- `make test`: 5 tests passed.
- `make demo`: FIFO selected `WR-001` and recovered 30 minutes.
- `make demo`: local best-fit selected `WR-002` and recovered 75 minutes.
- `WR-003` was excluded with `REQUIRED_ROOM_UNAVAILABLE`.
- The fixture seed is not yet a population generator; this limitation is explicit in `SF-001` and `SF-002`.
- Human teach-back remains open, so S1 is not marked approved.

## Required S1 teach-back

Ricardo should be able to answer:

1. Why is FIFO necessary even if it is intentionally simple?
2. Which fields are hard constraints in the current model?
3. Why does best-fit select `WR-002`?
4. Why is `WR-003` excluded?
5. What is still missing before OR-Tools can be justified?
