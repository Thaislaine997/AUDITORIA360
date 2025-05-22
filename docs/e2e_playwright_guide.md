# Guia de Testes E2E com Playwright – AUDITORIA360

## 1. Instalação e Configuração

- Instale o Playwright:

```bash
pip install playwright
playwright install
```

- Configure o ambiente de testes no arquivo `.env`.

## 2. Estrutura dos Testes

- Os testes ficam em `e2e_tests/`
- Use nomes descritivos para os arquivos e funções de teste
- Exemplo de teste básico:

```python
def test_login_sucesso(page):
    page.goto("https://app.auditoria360.com/login")
    page.fill("#username", "usuario_teste")
    page.fill("#password", "senha_teste")
    page.click("button[type=submit]")
    assert page.url == "https://app.auditoria360.com/dashboard"
```

## 3. Boas Práticas

- Use fixtures para setup/teardown
- Separe testes críticos dos opcionais
- Utilize comandos de espera explícita para elementos dinâmicos

## 4. Execução dos Testes

- Para rodar todos os testes:

```bash
pytest e2e_tests/
```

- Para rodar um teste específico:

```bash
pytest e2e_tests/test_login.py::test_login_sucesso
```

## 5. Relatórios e Debug

- Gere relatórios HTML com:

```bash
pytest --html=report.html
```

- Use `--headed` para visualizar o navegador durante o teste
- Utilize `page.screenshot()` para capturar falhas

---

**Dica:** Mantenha os testes E2E atualizados a cada release e integre-os ao pipeline de CI/CD para garantir qualidade contínua.
