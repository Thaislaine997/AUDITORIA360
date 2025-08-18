# ANÁLISE COMPLEMENTAR - AUDITORIA360
**Gerado em:** Mon Aug 18 16:12:59 UTC 2025

## 📊 ESTATÍSTICAS DETALHADAS

| Métrica | Valor |
|---------|-------|
| **Total de arquivos** | 532 |
| **Arquivos de código** | 362 |
| **Arquivos de documentação** | 38 |
| **Arquivos de configuração** | 27 |

## 🔍 ANÁLISE DE DUPLICATAS

### Package.json duplicados:
- ./package.json
- ./src/frontend/package.json

### Dockerfiles múltiplos:
- ./Dockerfile
- ./deploy/Dockerfile
- ./Dockerfile.frontend

### Configurações de lint duplicadas:
- ./src/frontend/eslint.config.js
- ./eslint.config.js
- ./.eslintrc.json

## 📁 ESTRUTURA DE DIRETÓRIOS

### Frontend Legado (src/frontend/):
- Páginas legadas: 14
- Componentes legados: 13

### Frontend Moderno (pages/):
- Páginas modernas: 14
- Componentes modernos: 48

## ⚙️ ANÁLISE DE WORKFLOWS

- Total de workflows: 20

### Workflows identificados:
- atualiza-lista-arquivos
- auditoria-relatorios
- auto-checklist
- changelog
- check-docs
- ci-cd-sample
- ci-cd
- ci-rls
- codeql-analysis
- deploy-pages
- deploy
- e2e
- export-logs
- health-check
- health-monitoring
- iai-c-health-monitor
- master-checklist-validation
- notify-slack
- rls-tests
- sync-wiki

## 🗂️ ANÁLISE DE CONFIGURAÇÕES

### Arquivos de configuração por tipo:
| Tipo | Quantidade | Arquivos |
|------|------------|----------|
| JSON | 12 | ./deploy/aws/autoscaling-template.json,./config/logging_config.json,./config/oracle_singularity_validation.json,... |
| YAML | 12 | ./docker-compose.monitoring.yml,./prompts/sumario_auditoria.prompt.yml,./prompts/checklist_conformidade.prompt.yml,... |
| TOML | 3 | ./cloudflare/wrangler.toml,./pyproject.toml,./supabase/config.toml,... |

## 📚 ANÁLISE DE DOCUMENTAÇÃO

### READMEs por diretório:
- ./.github
- ./.github/workflows
- .
- ./assets
- ./cloudflare
- ./conf
- ./config
- ./config/mcp
- ./data_base
- ./data_base/migrations
- ./data_base/schemas
- ./deploy/.github
- ./deploy
- ./deploy/aws
- ./deploy/kubernetes
- ./portal_demandas
- ./prompts
- ./src/frontend
- ./supabase
- ./supabase/functions
- ./supabase/policies
- ./templates

## 🎯 RECOMENDAÇÕES ESPECÍFICAS

### Ações Imediatas:
- [ ] Consolidar package.json duplicados (2 encontrados)
- [ ] Migrar completamente o frontend legado (src/frontend/)
- [ ] Consolidar Dockerfiles múltiplos (3 encontrados)
- [ ] Otimizar workflows excessivos (20 encontrados)

### Oportunidades de Melhoria:

---
**Análise complementar gerada pelo script de diagnóstico AUDITORIA360**
