import { test, expect } from '@playwright/test'

test('criar auditoria simples', async ({ page }) => {
  await page.goto('http://localhost:3000')
  // Assumindo usuário já logado via fixtures ou rota
  await page.click('text=Nova Auditoria')
  await page.fill('input[name="titulo"]', 'Auditoria Exemplo')
  await page.click('text=Iniciar')
  await expect(page.locator('text=Auditoria criada')).toBeVisible()
})
