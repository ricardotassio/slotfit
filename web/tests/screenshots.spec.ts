// Generates the README screenshots from the running application (SF-015).
// Every capture must show the no-go strip; nothing here is taken by hand.
import { expect, test } from '@playwright/test'

const OUT = '../docs/images'

test('captures the evidence screens for the README', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 })
  await page.goto('/')
  await expect(page.getByTestId('research-no-go')).toBeVisible()
  await page.waitForTimeout(800) // let fonts settle

  // 1. Hero + no-go strip + plan comparison, as the first screen a visitor sees
  await page.screenshot({ path: `${OUT}/01-first-screen.png`, fullPage: false })

  // 2. The no-go strip alone
  await page.getByTestId('research-no-go').screenshot({ path: `${OUT}/02-no-go-strip.png` })

  // 3. Side-by-side schedules (baseline vs candidate) on the global-conflict fixture
  const comparison = page.locator('article.schedule').first().locator('xpath=ancestor::section[1]')
  await comparison.screenshot({ path: `${OUT}/03-plan-comparison.png` })

  // 4. Evidence section with the CP-SAT plan selected: assignments and reason codes
  await page.getByRole('radio').nth(2).check()
  await expect(page.getByTestId('recovered-minutes')).toHaveText('120 min')
  const evidence = page.getByRole('table', { name: 'Selected plan assignments' }).locator('xpath=ancestor::section[1]')
  await evidence.screenshot({ path: `${OUT}/04-evidence-cp-sat.png` })

  // 5. Simulated human review: the only write, with "No external action occurred"
  const reviewButton = page.getByRole('button', { name: /accept/i }).first()
  await reviewButton.click()
  await expect(page.getByText(/No external action occurred/)).toBeVisible()
  const review = reviewButton.locator('xpath=ancestor::section[1]')
  await review.screenshot({ path: `${OUT}/05-human-review.png` })

  // 6. Whole page, for the architecture section
  await page.screenshot({ path: `${OUT}/06-full-page.png`, fullPage: true })
})
