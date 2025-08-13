import { test, expect } from '@playwright/test'

test('login e navegação para dashboard', async ({ page }) => {
  await page.goto('http://localhost:3000')
  await page.click('text=Entrar')
  await page.fill('input[name="email"]', 'contab_a@demo.local')
  await page.fill('input[name="password"]', 'demo123')
  await page.click('button[type="submit"]')
  await expect(page.locator('text=Dashboard')).toBeVisible()
})
