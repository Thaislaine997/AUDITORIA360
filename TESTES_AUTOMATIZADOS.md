# Testes Automatizados - AUDITORIA360

## 🧪 Visão Geral dos Testes

O AUDITORIA360 possui uma suíte abrangente de testes automatizados que garantem a qualidade, segurança e confiabilidade da plataforma durante todo o processo de desenvolvimento e deploy.

## 📁 Estrutura de Testes

```
AUDITORIA360/
├── 📁 __tests__/                  # Testes globais
├── 📁 pages/__tests__/            # Testes das páginas Next.js
├── 📁 components/__tests__/       # Testes dos componentes
├── 📁 lib/__tests__/              # Testes das integrações
├── 📁 src/frontend/src/test/      # Testes do sistema legado
├── 📁 scripts/validation/         # Scripts de validação
├── 📄 jest.config.js              # Configuração Jest
└── 📄 cypress.config.js           # Configuração Cypress (E2E)
```

## 🔧 Stack de Testes

| Ferramenta | Função | Cobertura |
|------------|--------|-----------|
| **Jest** | Testes unitários e integração | Frontend + Backend |
| **React Testing Library** | Testes de componentes React | Componentes UI |
| **Cypress** | Testes end-to-end | Fluxos completos |
| **Supertest** | Testes de API | Endpoints REST |
| **Playwright** | Testes de browser | UI/UX |

## ⚙️ Configuração e Execução

### Instalação de Dependências
```bash
npm install
# ou
yarn install
```

### Comandos de Teste

```bash
# Todos os testes
npm run test

# Testes em modo watch
npm run test:watch

# Testes com cobertura
npm run test:coverage

# Testes E2E (Cypress)
npm run test:e2e

# Testes de validação completa
make validate
```

## 📊 Cobertura de Testes

### Metas de Cobertura
- **Statements**: ≥ 80%
- **Branches**: ≥ 75%
- **Functions**: ≥ 85%
- **Lines**: ≥ 80%

### Cobertura Atual

```
File                     | % Stmts | % Branch | % Funcs | % Lines
-------------------------|---------|----------|---------|--------
All files               |   78.5  |   72.3   |   82.1  |   77.9
 pages/                 |   85.2  |   78.9   |   88.7  |   84.3
 components/            |   82.1  |   75.6   |   85.4  |   81.2
 lib/                   |   79.3  |   70.2   |   83.5  |   78.8
 src/frontend/src/      |   65.4  |   58.9   |   70.2  |   64.7
```

## 🧪 Tipos de Teste

### 1. Testes Unitários

**Localização**: `components/__tests__/`, `lib/__tests__/`

```typescript
// Exemplo: lib/__tests__/supabaseClient.test.ts
import { authHelpers } from '../supabaseClient';

describe('Supabase Auth Helpers', () => {
  test('should handle login correctly', async () => {
    const mockUser = { id: '123', email: 'test@example.com' };
    const result = await authHelpers.signIn('test@example.com', 'password');
    expect(result.data.user).toEqual(mockUser);
  });
});
```

### 2. Testes de Integração

**Localização**: `pages/__tests__/`

```typescript
// Exemplo: pages/__tests__/dashboard.test.tsx
import { render, screen } from '@testing-library/react';
import Dashboard from '../dashboard';

jest.mock('../lib/supabaseClient');

describe('Dashboard Page', () => {
  test('should render dashboard for authenticated user', async () => {
    render(<Dashboard />);
    expect(screen.getByText('Dashboard AUDITORIA360')).toBeInTheDocument();
  });
});
```

### 3. Testes End-to-End

**Localização**: `cypress/e2e/`

```typescript
// Exemplo: cypress/e2e/auth-flow.cy.ts
describe('Authentication Flow', () => {
  it('should login and redirect to dashboard', () => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('admin@auditoria360.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

### 4. Testes de API

**Localização**: `src/api/tests/`

```python
# Exemplo: src/api/tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_endpoint():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## 🔒 Testes de Segurança

### RLS (Row Level Security)
```bash
# Validação de segurança RLS
make validate-rls
```

### Testes de Penetração
```bash
# Scan de vulnerabilidades
npm run security:scan
```

### Validação LGPD
```bash
# Verificar compliance LGPD
python scripts/validation/lgpd_compliance.py
```

## 🏥 Health Checks

### Monitoramento Contínuo

```bash
# Health check completo
make validate-health

# Validação de staging
make validate-staging
```

### Métricas Monitoradas

1. **Tempo de Resposta**: < 200ms (API)
2. **Uptime**: > 99.5%
3. **Erros**: < 0.1% das requests
4. **Performance**: Core Web Vitals

## 🤖 Automação CI/CD

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:coverage
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Validate system
        run: make validate
```

### Pre-commit Hooks

```bash
# Instalação
make setup-hooks

# Hooks configurados:
# - Linting (ESLint, Prettier)
# - Type checking (TypeScript)
# - Unit tests
# - Security scan
```

## 📈 Relatórios de Teste

### Formatos de Saída

```bash
# Relatório HTML
npm run test:coverage -- --reporter=html

# Relatório JSON
make checklist-json

# Relatório completo
make checklist-all
```

### Integração com Ferramentas

- **SonarQube**: Análise de qualidade de código
- **Codecov**: Cobertura de testes
- **GitHub Actions**: Automação completa
- **Slack**: Notificações de falhas

## 🛠️ Ferramentas de Debug

### Modo Debug
```bash
# Jest em modo debug
npm run test:debug

# Cypress em modo interativo
npm run cypress:open
```

### Logs e Monitoramento
```bash
# Logs de teste
npm run test -- --verbose

# Profiling de performance
npm run test:performance
```

## 📚 Documentação de Testes

### Convenções de Nomenclatura
- **Arquivos**: `*.test.ts`, `*.spec.ts`
- **E2E**: `*.cy.ts`
- **Mocks**: `__mocks__/`

### Boas Práticas
1. **AAA Pattern**: Arrange, Act, Assert
2. **Descritivos**: Nomes de teste claros
3. **Isolados**: Cada teste independente
4. **Rápidos**: < 5s por suite
5. **Determinísticos**: Resultados consistentes

## 🚀 Pipeline de Qualidade

1. **Desenvolvedor**: Testes locais + pre-commit hooks
2. **PR**: Validação completa automatizada
3. **Staging**: Testes E2E + performance
4. **Produção**: Smoke tests + monitoring

---

**Quality Assurance powered by automated testing 🧪**