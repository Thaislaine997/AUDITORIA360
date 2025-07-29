# Testes Frontend - AUDITORIA360

## Visão Geral

Este documento descreve a estrutura e implementação dos testes unitários para o frontend do sistema AUDITORIA360, incluindo testes para componentes React/TypeScript e templates HTML.

## Estrutura de Testes

### 1. Testes React/TypeScript

**Localização**: `src/frontend/src/test/`

**Estrutura**:

```
src/frontend/src/test/
├── setup.ts                     # Configuração global dos testes
├── components/                  # Testes de componentes React
│   ├── Navbar.test.tsx
│   ├── Navbar.simple.test.tsx
│   └── Sidebar.test.tsx
├── hooks/                       # Testes de hooks customizados
│   └── useAuth.test.tsx
└── pages/                       # Testes de páginas
    └── Dashboard.test.tsx
```

**Tecnologias Utilizadas**:

- **Vitest**: Framework de testes
- **Testing Library**: Utilitários para testes de componentes React
- **jsdom**: Ambiente DOM para testes

### 2. Testes de Templates HTML

**Localização**: `tests/frontend/`

**Estrutura**:

```
tests/frontend/
└── test_html_templates.py      # Testes para templates HTML
```

**Tecnologias Utilizadas**:

- **pytest**: Framework de testes Python
- **BeautifulSoup**: Parser HTML para validação de estrutura

## Configuração

### Frontend React/TypeScript

1. **Dependências instaladas**:

   ```json
   {
     "vitest": "^3.2.4",
     "@testing-library/react": "^latest",
     "@testing-library/jest-dom": "^latest",
     "@testing-library/user-event": "^latest",
     "jsdom": "^latest"
   }
   ```

2. **Configuração no `vite.config.ts`**:

   ```typescript
   export default defineConfig({
     plugins: [react()],
     test: {
       globals: true,
       environment: "jsdom",
       setupFiles: ["./src/test/setup.ts"],
       css: true,
     },
   });
   ```

3. **Scripts disponíveis**:
   ```bash
   npm test          # Executa testes em modo watch
   npm run test:run  # Executa testes uma vez
   npm run test:ui   # Interface gráfica dos testes
   ```

### Templates HTML

1. **Dependências Python**:

   ```bash
   pip install pytest beautifulsoup4
   ```

2. **Execução**:
   ```bash
   python -m pytest tests/frontend/ -v
   ```

## Tipos de Testes Implementados

### 1. Testes de Componentes React

#### Navbar Component

- ✅ Renderização básica
- ✅ Conteúdo do título
- ✅ Estrutura com Material-UI

#### Sidebar Component

- ✅ Renderização de itens de menu
- ✅ Navegação por clique
- ✅ Estado ativo do menu

#### Dashboard Page

- ✅ Estados de carregamento
- ✅ Renderização de métricas
- ✅ Tratamento de erros

#### useAuth Hook

- ✅ Estados de autenticação
- ✅ Carregamento inicial
- ✅ Tratamento de erros

### 2. Testes de Templates HTML

#### Estrutura e Sintaxe

- ✅ Validação de elementos HTML
- ✅ Sintaxe Handlebars correta
- ✅ Atributos obrigatórios

#### Acessibilidade

- ✅ Atributos ARIA
- ✅ Roles semânticos
- ✅ Estrutura de navegação

#### Integração

- ✅ Existência de todos os templates
- ✅ Codificação UTF-8
- ✅ Consistência entre arquivos

## Cobertura de Testes

### Componentes Testados

- **Navbar**: 3 testes ✅
- **Sidebar**: 5 testes (4 ✅, 1 em ajuste)
- **Dashboard**: 5 testes (4 ✅, 1 em ajuste)
- **useAuth**: 4 testes (3 ✅, 1 em ajuste)

### Templates Testados

- **navigation.html**: ✅ Estrutura, sintaxe e acessibilidade
- **header.html**: ✅ Existência e estrutura básica
- **footer.html**: ✅ Existência e estrutura básica
- **status-indicator.html**: ✅ Estrutura básica
- **metric-card.html**: ✅ Estrutura básica
- **alert-container.html**: ✅ Estrutura básica

## Integração com CI/CD

### Pipeline GitHub Actions

O arquivo `.github/workflows/ci-cd.yml` foi atualizado para incluir:

```yaml
frontend-tests:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: "20"
    - name: Install frontend dependencies
      run: cd src/frontend && npm ci
    - name: Run frontend linting
      run: cd src/frontend && npm run lint
    - name: Run frontend tests
      run: cd src/frontend && npm test -- --run
    - name: Build frontend
      run: cd src/frontend && npm run build
```

### Validações Automáticas

- **Linting**: ESLint para código TypeScript/React
- **Testes**: Execução automática em PRs e pushes
- **Build**: Verificação de que o projeto compila
- **Templates**: Validação de estrutura HTML

## Executando os Testes

### Localmente

1. **Testes React**:

   ```bash
   cd src/frontend
   npm install
   npm test
   ```

2. **Testes Templates**:
   ```bash
   pip install pytest beautifulsoup4
   python -m pytest tests/frontend/ -v
   ```

### No CI/CD

Os testes são executados automaticamente em:

- Pull Requests para `main`
- Pushes para `main` e `develop`

## Próximos Passos

### Melhorias Planejadas

1. **Cobertura de Código**: Configurar relatórios de cobertura
2. **Testes E2E**: Implementar testes end-to-end com Playwright
3. **Visual Regression**: Testes de regressão visual
4. **Performance**: Testes de performance frontend

### Expansão dos Testes

1. **Mais Componentes**: Testar todos os componentes do sistema
2. **Integração**: Testes de integração entre componentes
3. **Acessibilidade**: Testes automatizados de acessibilidade
4. **Responsividade**: Testes em diferentes dispositivos

## Manutenção

### Atualizando Testes

- Manter testes sincronizados com mudanças nos componentes
- Atualizar mocks quando APIs mudarem
- Revisar cobertura periodicamente

### Boas Práticas

- Testes devem ser independentes
- Usar dados mock realistas
- Manter testes rápidos e focados
- Documentar casos complexos

---

**Data de Última Atualização**: Dezembro 2024  
**Responsável**: Equipe Frontend AUDITORIA360
