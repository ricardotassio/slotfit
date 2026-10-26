import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  // The screenshot script regenerates docs/images and records a review event; run it on purpose.
  testIgnore: process.env.SLOTFIT_SCREENSHOTS ? [] : ['**/screenshots.spec.ts'],
  fullyParallel: false,
  retries: 0,
  workers: 1,
  reporter: 'line',
  use: {
    baseURL: 'http://127.0.0.1:5173',
    trace: 'retain-on-failure',
  },
  webServer: [
    {
      command: 'uv run --directory .. --python 3.12 uvicorn slotfit.api:app --app-dir src --host 127.0.0.1 --port 8000',
      url: 'http://127.0.0.1:8000/health',
      reuseExistingServer: true,
      timeout: 30_000,
    },
    {
      command: 'npm run dev -- --host 127.0.0.1 --port 5173',
      url: 'http://127.0.0.1:5173',
      reuseExistingServer: true,
      timeout: 30_000,
    },
  ],
})
