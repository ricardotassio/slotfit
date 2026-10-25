import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'

import { expect, test } from '@playwright/test'

const require = createRequire(import.meta.url)
const axeSource = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8')

test('shows the no-go before a neutral, synchronized plan comparison', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByRole('heading', { name: 'SlotFit evidence lab' })).toBeVisible()
  await expect(page.getByTestId('research-no-go')).toContainText('No candidate passed')
  const planChoices = page.getByRole('radio')
  await expect(planChoices).toHaveCount(3)
  await expect(planChoices.nth(0)).toHaveAttribute('value', 'fifo-eligible@0.2.0')
  await expect(page.getByTestId('recovered-minutes')).toHaveText('60 min')
  await expect(page.getByRole('row', { name: /WR-FLEXIBLE OPEN-A/ })).toBeVisible()

  await planChoices.nth(2).check()

  await expect(page.getByTestId('recovered-minutes')).toHaveText('120 min')
  await expect(page.getByRole('table', { name: 'Selected plan assignments' })).toBeVisible()
  await expect(page.getByRole('row', { name: /CONSTRAINED OPEN-A/ })).toBeVisible()
  await expect(page.locator('.disclosure')).toContainText(/controlled counterexample/i)
})

test('records only a simulated review and disables duplicate submission', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('radio').nth(2).check()
  const rejectButton = page.getByRole('button', { name: 'Record reject' })

  await rejectButton.click()

  await expect(page.getByRole('status')).toContainText(/review (created|replayed)/i)
  await expect(page.getByRole('status')).toContainText('No external action occurred')
  await expect(rejectButton).toBeEnabled()
})

test('offers retry after an API loading failure', async ({ page }) => {
  let shouldFail = true
  await page.route('**/api/v1/demos/global-conflict', async (route) => {
    if (shouldFail) {
      shouldFail = false
      await route.abort()
      return
    }
    await route.continue()
  })

  await page.goto('/')
  await expect(page.getByRole('alert')).toContainText('Could not load')
  await page.getByRole('button', { name: 'Retry loading evidence' }).click()
  await expect(page.getByTestId('research-no-go')).toBeVisible()
})

test('reports review failure without implying an external action', async ({ page }) => {
  await page.route('**/api/v1/reviews', (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: '{}' }),
  )
  await page.goto('/')

  await page.getByRole('button', { name: 'Record reject' }).click()

  await expect(page.getByRole('alert')).toContainText('Review was not recorded')
  await expect(page.getByRole('alert')).toContainText('No external action occurred')
})

test('has no serious or critical axe violations in the main flow', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('research-no-go')).toBeVisible()
  await page.addScriptTag({ content: axeSource })

  const violations = await page.evaluate(async () => {
    const result = await (window as typeof window & { axe: { run: () => Promise<{ violations: Array<{ impact: string | null }> }> } }).axe.run()
    return result.violations.filter((item) => item.impact === 'serious' || item.impact === 'critical')
  })

  expect(violations).toEqual([])
})
