# 📦 Plano AUDITORIA360 – Versão 4 (Arquitetura Moderna Serverless Vercel, Neon, Cloudflare R2, DuckDB, PaddleOCR)

> **IMPORTANTE: Este documento é o novo plano principal de evolução, implantação e governança do AUDITORIA360, substituindo as versões anteriores.**
>
> Ele incorpora todas as atualizações, decisões arquiteturais e práticas para a era serverless, conforme última migração.

---

## 1. Visão Geral, Objetivos e Metodologia

O **AUDITORIA360** agora opera sobre uma arquitetura moderna e econômica, focada em:
- **Redução radical de custos** (eliminando dependência de Google Cloud).
- **Alta escalabilidade com baixo esforço operacional**.
- **Automação, rastreabilidade, qualidade, segurança e governança**.

**Stack Atual**:
- **API/Dashboards:** Vercel (Funções Serverless com FastAPI/Streamlit)
- **Banco de Dados:** Neon (PostgreSQL Serverless)
- **Armazenamento de Arquivos:** Cloudflare R2
- **Analytics:** DuckDB (in-memory/embedded)
- **OCR:** PaddleOCR (embarcado, sem custo de API)

**Metodologia:** Incremental, ágil, com entregas semanais, documentação contínua e rastreamento via GitHub (issues, boards, milestones).

---

## 2. Checklist Granular por Diretório (Atualizado)

### 🗂️ **assets/** — Recursos Visuais
- [ ] Centralizar design system, garantir versionamento e integração com dashboards.

### 🔑 **auth/** — Autenticação
- [ ] Unificação de fluxos SSO/JWT.
- [ ] Testes e automação de logs/permissões.

### 🤖 **automation/** — Robôs & RPA
- [ ] Refatorar para integração serverless (ex: triggers GitHub Actions, jobs Vercel).

### 💾 **backups/** — Backup
- [ ] Procedimentos para Neon e R2 (utilizar scripts Python/CI para backup e restauração automatizados).

### ⚙️ **configs/** — Configurações
- [ ] Variáveis de ambiente centralizadas. Padronizar `.env.example` para uso com Vercel/Neon/R2.

### 📊 **dashboards/** — Streamlit (opcional, pode ser serviço separado na Vercel)
- [ ] Refatorar deploy para Vercel, integração via API FastAPI.

### 🗄️ **data/** — Dados
- [ ] Padrão aberto (CSV/Parquet), exemplos para testes DuckDB.

### 🚀 **deploy/** — DevOps
- [ ] Remover scripts de Cloud Run/GCP.
- [ ] Automatizar deploy via GitHub Actions e Vercel.
- [ ] Garantir variáveis de ambiente para integração com serviços externos (Neon, R2).

### 📚 **docs/** — Documentação
- [ ] Atualizar README para nova stack.
- [ ] Manter histórico de versões do plano.
- [ ] Documentar exemplos de uso da API, storage, analytics e OCR.

### 🧪 **e2e_tests/** — E2E Tests
- [ ] Garantir cobertura de todos fluxos críticos, com mocks dos serviços externos.

### 🏗️ **infra/** — Infraestrutura
- [ ] Infra migrada para serverless; manter scripts de provisionamento do mínimo necessário (ex: buckets R2).

### 🛠️ **installers/** — Setup
- [ ] Automatizar onboarding para devs: scripts para criar `.env.local`, conexão com Neon/R2.

### 🧮 **matriz/** — Regras
- [ ] Regras mantidas em SQL/Python, testadas em DuckDB.

### 📓 **notebooks/** — ML/Prototipação
- [ ] Exemplos de uso local do DuckDB, integração PaddleOCR para experimentos.

### 💼 **portal_demandas/** — Portal
- [ ] Refatorar para usar SQLAlchemy+Neon.
- [ ] Testes focados em integração serverless.

### 📝 **scripts/** — ETL/Utilitários
- [ ] Scripts para ingestão/exportação usando DuckDB e boto3 para R2.

### ⚡ **services/** — Backend/ML
- [ ] Pipelines ML/LLMOps adaptados à nova stack (sem dependências GCP).
- [ ] Endpoints FastAPI integrando Neon, DuckDB, R2, PaddleOCR.

### 🗃️ **sql/** — Modelos/Queries
- [ ] Queries atualizadas para PostgreSQL (Neon) e DuckDB.

### 🏛️ **src/** — Backend Core
- [ ] Refatoração para desacoplamento GCP.
- [ ] Cobertura de testes, documentação inline.

### 🏛️ **src_legacy_backup/** — Legado
- [ ] Manter apenas para referência/migração.

### 🧪 **tests/** — Unitários
- [ ] Cobertura >85% dos fluxos críticos.

---

## 3. Automação CI/CD

- **Deploy:** Push no GitHub aciona build na Vercel (via vercel.json).
- **Testes:** GitHub Actions para lint, testes unitários e E2E com banco Neon de dev e storage R2.
- **Ambiente:** Variáveis sensíveis (Neon, R2, SECRET_KEY) SEMPRE via painel da Vercel.

---

## 4. Itens a Eliminar (pós-migração)

**No Google Cloud:**
- [X] Cloud SQL (Postgres)
- [X] BigQuery (datasets, tabelas)
- [X] Cloud Storage (buckets/arquivos)
- [X] Cloud Run (serviços)
- [X] Document AI (instance/processors)
- [X] Scripts e contas de serviço não mais usadas

**No repositório:**
- [X] Scripts e configs GCP (`cloudrun_deploy.sh`, `auditoria_gcp.sh`, `app.yaml`, etc.)
- [X] Dependências `google-cloud-*` do requirements.txt
- [X] SQL/queries específicas do BigQuery

---

## 5. Segurança e Boas Práticas

- **Chaves/API:** Nunca commit no repositório. Gerenciar via painel da Vercel.
- **Backups:** Automatizar backups Neon/R2.
- **Documentação:** README sempre atualizado com instruções da nova stack.
- **Testes:** Cobertura mínima 85% e E2E para integrações externas.

---

## 6. Indicadores de Sucesso

- Deploys serverless estáveis, baixo custo (<R$10/mês).
- Inexistência de dependências GCP.
- Cobertura de testes >85%.
- Integração completa dos módulos (Neon, R2, DuckDB, PaddleOCR).
- Onboarding rápido (novo dev funcional <2h).
- Logs, automação e backups funcionando ponta a ponta.

---

## 7. Links Úteis

- [Documentação Neon](https://neon.tech/docs)
- [Cloudflare R2](https://developers.cloudflare.com/r2/)
- [Vercel Python](https://vercel.com/docs/runtimes#official-runtimes/python)
- [DuckDB](https://duckdb.org/docs/)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Boas Práticas Serverless Python](https://vercel.com/guides/deploying-fastapi-with-vercel)

---

## 8. Histórico de Alterações

- **Versão 4 (atual):** Migração completa para stack serverless, checklist atualizado, eliminação do GCP.
- **Versão 3:** Checklist granular por pasta, integração GCP.
- **Versão 2:** Estrutura modular, primeiros scripts de automação.
- **Versão 1:** Início do projeto.

---

> **Este plano deve ser revisado a cada ciclo de entrega, mantendo registro de todas as decisões e mudanças arquiteturais.**