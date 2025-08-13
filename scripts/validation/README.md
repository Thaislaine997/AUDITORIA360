# AUDITORIA360 - Validation System

Sistema de validação operacional abrangente para garantir que todas as funcionalidades estejam operando corretamente antes da implantação em produção.

## 🎯 Visão Geral

Este sistema implementa o checklist operacional completo com 14 seções de validação, focando na prioridade máxima para validação visual do frontend e conformidade LGPD através de testes RLS.

## 📁 Estrutura dos Scripts

```
scripts/validation/
├── master_validation.py        # Orquestrador principal - executa todas as validações
├── health_checks.py           # Validação de saúde do backend (FastAPI)
├── rls_security.py            # Validação crítica de RLS multi-tenant (LGPD)
├── frontend_visual_qa.py      # Validação visual do frontend (PRIORIDADE MÁXIMA)
├── e2e_validation.py          # Validação de testes E2E com Playwright
└── README.md                  # Esta documentação
```

## 🚀 Uso Rápido

### Executar Validação Completa

```bash
# Ambiente local (padrão)
python scripts/validation/master_validation.py

# Ambiente de staging
python scripts/validation/master_validation.py --staging

# Salvar resultados em arquivo
python scripts/validation/master_validation.py --output validation_results.json

# Pular seções específicas (ex: E2E e observabilidade)
python scripts/validation/master_validation.py --skip 6,7
```

### Scripts Individuais

```bash
# Validação de saúde do backend
python scripts/validation/health_checks.py

# Validação RLS (crítica para LGPD)
python scripts/validation/rls_security.py

# Validação visual do frontend (PRIORIDADE MÁXIMA)
python scripts/validation/frontend_visual_qa.py --url http://localhost:3000

# Validação E2E
python scripts/validation/e2e_validation.py
```

## 📋 Seções de Validação

### ✅ Seções Implementadas

1. **CI/CD Pipeline Status** - Verificação do status dos workflows do GitHub
2. **Backend Health Checks** - Endpoints de saúde e funcionalidade da API FastAPI
3. **Database & RLS Security** - Isolamento multi-tenant crítico para LGPD
4. **API Connectivity** - Conectividade Frontend-Backend e CORS
5. **Frontend Visual QA** - 🔥 **PRIORIDADE MÁXIMA** - Build, deploy e consistência visual
6. **E2E Testing** - Execução da suíte de testes Playwright
7. **Integration Tests** - Suíte completa de testes de integração

### 🚧 Seções Planejadas (Para Implementação Futura)

8. **Observability** - Validação de logs, métricas e rastreamento
9. **Security Scanning** - Escaneamento de segredos e cabeçalhos de segurança
10. **Performance & Bundle Analysis** - Auditorias Lighthouse e análise de tamanho do bundle
11. **Accessibility Testing** - Validação A11y e verificações de conformidade
12. **Environment Validation** - Variáveis de ambiente e configuração
13. **Deployment Readiness** - Checklist final de prontidão para deployment
14. **Cleanup Operations** - Remoção de pastas temporárias e limpeza

## 🎨 Frontend Visual QA (PRIORIDADE MÁXIMA)

A validação visual do frontend é marcada como **PRIORIDADE MÁXIMA** no checklist operacional. Este script verifica:

### ✅ Checklist Visual por Página

- [ ] Página carrega em ≤ 3s (desktop)
- [ ] Nenhum erro ou warning vermelho no Console (DevTools → Console)
- [ ] Nenhuma requisição de recurso retorna 404/500 (Network tab)
- [ ] CSS carregado (não ver "unstyled" HTML ou sem CSS)
- [ ] Imagens e ícones renderizam (sem broken image icon)
- [ ] Fontes carregadas (sem fallback cascades visíveis)
- [ ] Layout responsivo ao redimensionar (320px / 768px / 1024px / 1440px)
- [ ] Componentes dinâmicos (modals, toasts, dropdowns) funcionando
- [ ] Botões e formulários funcionam (submissões, validações do lado cliente)
- [ ] Links internos (router) não quebram

### 📱 Páginas Prioritárias Testadas

- `/` - Dashboard
- `/login` - Login
- `/contabilidades` - Contabilidades
- `/auditorias` - Auditorias
- `/relatorios` - Relatórios
- `/admin/users` - Admin Users

## 🔒 RLS Security Validation (Crítico LGPD)

A validação RLS é **crítica para conformidade LGPD** e verifica:

### 🛡️ Testes de Isolamento Multi-Tenant

1. **Isolamento Principal**: Tenant B NÃO deve acessar dados do Tenant A
2. **Isolamento Bidirecional**: Verificação em ambas as direções
3. **Isolamento de Listagem**: Endpoints de lista mostram apenas dados do tenant

### ⚠️ Critérios Críticos

- Tenant B recebe **403 ou 404** ao tentar acessar dados de A
- **NUNCA 200** com dados de outro tenant (violação LGPD crítica)
- Listas não mostram dados sobrepostos entre tenants

## 🎭 E2E Testing com Playwright

Sistema automatizado para:

- Instalação e configuração do Playwright
- Descoberta de testes E2E existentes
- Execução de testes com relatórios
- Criação de testes básicos se não existirem

### 🔧 Configuração Automática

O sistema cria automaticamente:
- `playwright.config.ts`
- Testes básicos de sanidade
- `package.json` para dependências E2E

## 📊 Códigos de Saída

- `0` - Sucesso: Todas as validações críticas passaram
- `1` - Falha: Algumas validações falharam
- `2` - Falha Crítica: Falhas críticas detectadas (não implantar)

## 🚨 Triggers de Rollback

O sistema detecta automaticamente condições que exigem rollback imediato:

- Erro 5xx > 1% e não diminuindo
- Latência P95 > 3x baseline
- Falhas massivas de login / vazamentos RLS detectados
- Frontend branco / exceções JS em >5% das sessões

## 📈 Exemplo de Saída

```
🚀 AUDITORIA360 - Master Validation Orchestrator
================================================================================
📅 Started: 2024-12-19T10:30:00.000Z
🌐 Environment: local
🔗 Backend URL: http://localhost:8000
🎨 Frontend URL: http://localhost:3000
================================================================================

📋 Section 1: CI/CD Pipeline Status
   Check GitHub Actions workflows and CI status
✅ Section 1: CI/CD Pipeline Status - PASS

📋 Section 2: Backend Health Checks
   FastAPI health endpoints and API functionality
❌ Section 2: Backend Health Checks - FAIL
   Error: API server not accessible

📋 Section 3: Database & RLS Security
   Multi-tenant isolation and LGPD compliance
🔴 CRITICAL Section 3: Database & RLS Security - CRITICAL_FAIL
   Error: RLS violation detected - LGPD compliance issue

...

================================================================================
📊 FINAL VALIDATION REPORT
================================================================================
🎯 Overall Status: CRITICAL_FAIL
✅ Sections Passed: 5/14
❌ Failed Sections: 9
🔴 Critical Failures: 2

🚨 ROLLBACK TRIGGERS DETECTED (2):
   • Database & RLS Security: RLS violation detected - LGPD compliance issue
   • Frontend Visual QA: Critical pages not accessible

🚫 DEPLOYMENT DECISION: DO NOT DEPLOY
   Critical issues must be resolved before deployment
```

## 🔧 Desenvolvimento

### Adicionando Nova Seção de Validação

1. Criar script individual em `scripts/validation/`
2. Adicionar método de validação em `master_validation.py`
3. Atualizar a lista `validation_sections`
4. Testar individualmente e em conjunto

### Padrões de Script

Todos os scripts seguem o padrão:
- Classe principal com métodos de teste
- Logging estruturado de resultados
- Códigos de saída consistentes
- Saída JSON opcional
- Tratamento de exceções robusto

## 📚 Dependências

- `requests` - Para testes HTTP
- `subprocess` - Para execução de comandos
- `pathlib` - Para manipulação de arquivos
- `playwright` - Para testes E2E (instalado automaticamente)

## 🤝 Contribuição

Para contribuir com o sistema de validação:

1. Mantenha o foco na automação completa
2. Implemente validações que correspondam ao checklist operacional
3. Use códigos de saída consistentes
4. Adicione logging detalhado para debugging
5. Teste tanto cenários de sucesso quanto falha

## 📞 Suporte

Para problemas com o sistema de validação:

1. Verifique logs detalhados com `--output results.json`
2. Execute scripts individuais para isolamento de problemas
3. Confirme que ambiente está configurado corretamente
4. Revise dependências e permissões de arquivo