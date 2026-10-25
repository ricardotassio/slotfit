# Local demonstration runbook

## Prerequisites

- Git;
- `uv` with access to Python 3.12;
- Node.js 26 and npm 11;
- approximately 350 MB for the Playwright Chromium test browser.

No Docker, database server, cloud account, secret or external API is required.

## Locked setup

From a clean checkout:

```bash
uv sync --frozen --python 3.12
npm ci --prefix web
cd web
npx playwright install chromium
cd ..
make verify
```

`uv.lock` and `web/package-lock.json` are the dependency sources of truth. Do not
replace locked installs with unbounded upgrades while reproducing recorded
evidence.

## Run the interactive demonstration

Terminal 1:

```bash
PYTHONPATH=src uv run --python 3.12 uvicorn slotfit.api:app \
  --app-dir src --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
npm --prefix web run dev -- --host 127.0.0.1 --port 5173
```

Open `http://127.0.0.1:5173`. Keep both processes on loopback. The UI reads only
synthetic fixtures. A review click appends a local SQLite audit event under
`artifacts/reviews/` with `external_action: none`; it does not book or message.

## Ninety-second demo path

1. Start on the red-bordered development decision: no candidate passed.
2. Show FIFO and local best-fit recovering 60 minutes in the global conflict.
3. Select CP-SAT and show 120 minutes plus the synchronized assignment table.
4. Explain that fixture optimality did not pass the longitudinal exposure gate.
5. Show V4's 10.80 p.p. result against the predeclared 10 p.p. maximum.
6. Record a simulated reject and point to “No external action occurred.”
7. End on the repository tests and the claim boundary.

## Troubleshooting

- Port busy: stop the existing local process or choose matching free API/UI ports
  and update the Vite proxy for that run.
- Missing browser: run `cd web && npx playwright install chromium`.
- Lock mismatch: do not regenerate locks silently; inspect the changed dependency
  and rerun the full verification suite.
- Stale local reviews: the database is ignored by Git. Preserve it if needed for a
  demo audit; otherwise use a fresh checkout. Never place real data in it.
