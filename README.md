# AUDITORIA360 - Portal de Gestão da Folha, Auditoria 360 e CCT

> **🎯 PROJETO 96% CONCLUÍDO** - Consulte **[📚 Documentação Unificada](docs/00-INDICE_PRINCIPAL.md)** para navegação completa | **[🚀 Início Rápido](docs/01-INICIO_RAPIDO.md)** para começar

Portal seguro, inteligente e integrado para centralizar, automatizar e auditar todos os processos de folha de pagamento, obrigações sindicais e convenções coletivas.

## 📊 Status Atual
- ✅ **Migração serverless**: 100% concluída
- ✅ **API e portal demandas**: 100% funcionais  
- ✅ **Dashboards configurados**: 100% implementados
- ✅ **Documentação**: 100% unificada e organizada
- ⏳ **4% restante**: Testes finais (90%→95%), otimizações

**📋 Para verificar progresso:**
```bash
# Status geral do projeto
python scripts/verificar_progresso.py

# Cobertura de testes (205 testes implementados)
pytest --cov=src --cov-report=html --cov-fail-under=90
```

**📖 Documentação Unificada**: [**ÍNDICE PRINCIPAL**](docs/00-INDICE_PRINCIPAL.md) | [**Diagnóstico Inicial**](docs/diagnostico-inicial.md) | [**Status Detalhado**](docs/relatorios/status-projeto.md)

## 🎯 Objetivo

Desenvolver um portal completo que elimina processos manuais e riscos de não conformidade através de:

- **Centralização** e automação de processos de folha de pagamento
- **Gestão inteligente** de documentos e CCTs
- **Sistema avançado** de auditoria e compliance
- **IA e chatbot** para assistência especializada

## 🏗️ Arquitetura Serverless

### Stack Tecnológica
- **Frontend**: React.js + TypeScript + Material UI
- **Backend**: FastAPI (Python)
- **Banco de Dados**: Neon (PostgreSQL serverless)
- **Armazenamento**: Cloudflare R2
- **Analytics**: DuckDB (embedded)
- **OCR**: PaddleOCR
- **IA**: OpenAI GPT Integration
- **Deploy**: Vercel + GitHub Actions
- **Monitoramento**: Sentry, Grafana, Prometheus

### Segurança e Compliance
- **Autenticação**: OAuth2 + JWT
- **Criptografia**: Dados sensíveis criptografados
- **LGPD**: Consentimento explícito e anonimização
- **Backup**: Automatizado para Neon e R2
- **Firewall**: Cloudflare (DDoS protection)

## 📚 Navegação da Documentação

### 🚀 **Acesso Rápido**
- **[📋 Índice Principal](docs/00-INDICE_PRINCIPAL.md)** - Navegação completa da documentação
- **[🏁 Início Rápido](docs/01-INICIO_RAPIDO.md)** - Guia para começar em 5 minutos
- **[📊 Status do Projeto](docs/relatorios/status-projeto.md)** - Situação atual detalhada
- **[📁 Documentos Organizados](docs/documentos/README.md)** - Estrutura centralizada de documentação

### 👥 **Por Perfil de Usuário**
- **👤 Usuários**: [Manual do Usuário](docs/usuario/manual-usuario.md) | [Guia de Instalação](docs/usuario/guia-instalacao.md) | [FAQ](docs/usuario/faq.md)
- **👨‍💻 Desenvolvedores**: [Guia Dev](docs/tecnico/desenvolvimento/dev-guide.md) | [Módulos](docs/tecnico/modulos-principais.md) | [APIs](docs/tecnico/apis/api-documentation.md) | [**Exemplos Práticos**](docs/tecnico/exemplos-praticos-uso.md)
- **👔 Gestores**: [Análise Estratégica](docs/estrategico/analise-consolidada.md) | [Roadmap](docs/estrategico/roadmap-estrategico.md)
- **🔍 Auditores**: [Compliance](docs/compliance/auditoria/checklist-auditoria.md) | [LGPD](docs/compliance/lgpd/)

## 💡 Exemplos de Uso e Fluxo Prático

### 🚀 Caso de Uso 1: Processamento de Folha Mensal

```bash
# 1. Configurar sistema
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
make install-dev

# 2. Iniciar serviços
make run  # Terminal 1
cd src/frontend && npm run dev  # Terminal 2

# 3. Acessar sistema
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

**Fluxo no Sistema:**
1. **Login** → Dashboard principal
2. **Funcionários** → Verificar cadastros atualizados
3. **Folha** → Criar nova competência (ex: Jan/2024)
4. **Calcular** → Processamento automático
5. **Revisar** → Validar cálculos e exceções
6. **Aprovar** → Gerar holerites e relatórios
7. **Exportar** → PDF, Excel para contabilidade

### 📄 Caso de Uso 2: Gestão de Documentos CCT

```python
# Exemplo de API para upload de CCT
import requests

# Upload documento CCT
files = {'file': open('cct_sindicato_2024.pdf', 'rb')}
response = requests.post(
    'http://localhost:8000/api/v1/cct/upload',
    files=files,
    headers={'Authorization': 'Bearer your_token'}
)

# Extrair cláusulas automaticamente (IA + OCR)
cct_id = response.json()['id']
clausulas = requests.get(f'http://localhost:8000/api/v1/cct/{cct_id}/clausulas')
```

**Fluxo no Sistema:**
1. **CCT** → Upload de nova convenção
2. **Processamento** → OCR + IA extrai cláusulas
3. **Revisão** → Validar extração automática
4. **Comparação** → Comparar com CCT anterior
5. **Notificação** → Alertar sobre mudanças críticas
6. **Compliance** → Auditar conformidade automática

### 🔍 Caso de Uso 3: Auditoria Automatizada

```python
# Exemplo de execução de auditoria via API
audit_request = {
    "tipo": "folha_pagamento",
    "periodo": {"inicio": "2024-01-01", "fim": "2024-12-31"},
    "regras": ["inss", "fgts", "irrf", "clt_compliance"]
}

response = requests.post(
    'http://localhost:8000/api/v1/auditorias/executar',
    json=audit_request,
    headers={'Authorization': 'Bearer your_token'}
)

# Acompanhar progresso
audit_id = response.json()['id']
status = requests.get(f'http://localhost:8000/api/v1/auditorias/{audit_id}/status')
```

**Fluxo no Sistema:**
1. **Auditoria** → Configurar escopo e regras
2. **Execução** → Motor de compliance automatizado
3. **Análise** → IA identifica não conformidades
4. **Relatório** → Achados com recomendações
5. **Plano de Ação** → Priorização por risco
6. **Acompanhamento** → Status de correções

### 🤖 Caso de Uso 4: Assistente de IA

```python
# Exemplo de interação com chatbot
chat_request = {
    "pergunta": "Como calcular adicional noturno para funcionário CLT?",
    "contexto": "empresa_categoria_a",
    "cct_aplicavel": "sindicato_metalurgicos_sp"
}

response = requests.post(
    'http://localhost:8000/api/v1/ai/chat',
    json=chat_request,
    headers={'Authorization': 'Bearer your_token'}
)

resposta = response.json()['resposta']
# Retorna: "Para adicional noturno CLT, aplicar 20% sobre hora normal..."
```

**Fluxo no Sistema:**
1. **Chat IA** → Pergunta sobre legislação
2. **Processamento** → IA consulta base de conhecimento
3. **Resposta** → Contextualizada com CCT específica
4. **Referências** → Links para artigos relevantes
5. **Aprendizado** → Sistema melhora com feedback

## 🔄 Fluxo de CI/CD em Ação

### Pipeline Automatizado (GitHub Actions)

```yaml
# Exemplo de execução automática
push main → Trigger Pipeline:
  ✅ Pre-commit hooks (formatação, linting)  
  ✅ Testes unitários (205 testes, 90%+ cobertura)
  ✅ Testes integração (API + DB)
  ✅ Testes frontend (React + TypeScript)
  ✅ Build produção
  ✅ Deploy Vercel automático
  ✅ Health checks pós-deploy
  ✅ Notificação Slack/email
```

### Monitoramento Contínuo

```bash
# Comandos de monitoramento
python scripts/verificar_progresso.py  # Status geral
python scripts/health_check.py         # Saúde do sistema  
python scripts/performance_monitor.py  # Métricas de performance

# Relatórios automáticos
pytest --cov=src --cov-report=html     # Cobertura de testes
make backup-db                         # Backup automático
```

### Desenvolvimento em Equipe

```bash
# Fluxo de desenvolvimento colaborativo
git checkout -b feature/nova-funcionalidade
git commit -m "feat: adicionar validação INSS"
git push origin feature/nova-funcionalidade

# PR automático disparará:
# - Testes em múltiplas versões Python (3.11, 3.12)
# - Verificação de conflitos
# - Review automático de código
# - Deploy preview no Vercel
```

## 📋 Funcionalidades Principais

### 1. 🔐 Gestão de Usuários e Permissões
- **Perfis**: Administrador, RH, Contador, Colaborador, Sindicato
- **Autenticação**: OAuth2/JWT com tokens seguros
- **Permissões**: Sistema granular por recurso e ação
- **Auditoria**: Logs completos de acesso e alterações

### 2. 💼 Gestão de Folha de Pagamento
- **Funcionários**: Cadastro completo com validação CPF/PIS
- **Competências**: Controle por ano/mês/tipo de folha
- **Cálculos**: Automação de férias, 13º, INSS, FGTS, IRRF
- **Importação**: Suporte a CSV, XLSX e API
- **Validação**: Motor de regras para detectar inconsistências
- **Relatórios**: Holerites, sintéticos e detalhados

### 3. 📄 Gestão de Documentos
- **Upload**: Múltiplos arquivos (PDF, DOCX, XLSX, imagens)
- **Armazenamento**: Seguro no Cloudflare R2
- **Versionamento**: Controle completo de versões
- **Permissões**: Acesso granular por usuário/documento
- **OCR**: Processamento automático com PaddleOCR
- **Busca**: Indexação avançada por conteúdo e metadados

### 4. 📝 Base de Convenções Coletivas (CCTs)
- **Sindicatos**: Cadastro de entidades sindicais
- **CCTs**: Gestão completa de convenções coletivas
- **Cláusulas**: Extração e indexação automática
- **Comparação**: Sistema de comparação entre CCTs
- **Atualizações**: Scraping automático de novas versões
- **Histórico**: Controle de versões e alterações
Central: Dashboard unificado de notificações
6. 🔍 Auditoria e Compliance
Execuções: Auditorias periódicas e por evento
Regras: Motor configurável de compliance
Achados: Detecção automática de não conformidades
Relatórios: Exportação em múltiplos formatos
Riscos: Avaliação e monitoramento contínuo
7. 🤖 IA, Chatbot e Bots Inteligentes
Chatbot: Assistente treinado com base de conhecimento
OpenAI: Integração para respostas contextuais
Recomendações: Sistema de sugestões automáticas
Aprendizado: Melhoria contínua baseada em feedback
Knowledge Base: Base de conhecimento searchável
Pré-requisitos
Python 3.12+
Node.js 18+
Conta na Neon (PostgreSQL)
Conta no Cloudflare R2
Chave da OpenAI (opcional)
Backend (API)
Instalar dependências:
pip install -r requirements.txt
Configurar variáveis de ambiente:
cp .env.example .env
# Editar .env com suas credenciais
Executar API:
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
Acessar documentação:
API Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/health
Frontend (React)
Navegar para frontend:
cd src/frontend
Instalar dependências:
npm install
Executar aplicação:
npm run dev
Acessar aplicação:
Frontend: http://localhost:3000

### 📋 Exemplos Práticos

**Executar exemplos de uso:**
```bash
# Exemplo básico de autenticação
python examples/api_authentication_example.py

# Exemplo de gestão de folha de pagamento
python examples/api_payroll_example.py

# Exemplo de processamento de documentos
python examples/api_documents_example.py

# Exemplo de IA e chatbot
python examples/ai_chatbot_example.py

# Exemplo de analytics avançado
python examples/duckdb_example.py

# Exemplo de OCR
python examples/ocr_paddle_example.py caminho/para/imagem.png

# Workflow completo de auditoria
python examples/complete_workflow_example.py
```

**Documentação completa de exemplos:** [**Exemplos Práticos de Uso**](docs/tecnico/exemplos-praticos-uso.md)
=======
## 🚀 Como Executar

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- Conta na Neon (PostgreSQL)
- Conta no Cloudflare R2
- Chave da OpenAI (opcional)

### 🔧 Instalação Rápida

#### Método 1: Usando Makefile (Recomendado)
```bash
# Clonar repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# Instalar dependências de desenvolvimento
make install-dev

# Configurar hooks de qualidade
make setup-hooks

# Verificar instalação
make check
```

#### Método 2: Manual
```bash
# Instalar dependências Python
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Instalar dependências Frontend
cd src/frontend
npm install
cd ../..
```

### ⚙️ Configuração

1. **Configurar variáveis de ambiente:**
```bash
cp .env.example .env
# Editar .env com suas credenciais
```

2. **Variáveis essenciais:**
```env
# Database
DATABASE_URL=postgresql://user:pass@host/db

# Storage
R2_ENDPOINT_URL=https://account.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=auditoria360-storage

# Security
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256

# AI Services (opcional)
OPENAI_API_KEY=your_openai_key
```

### 🏃‍♂️ Execução

#### Backend (API)
```bash
# Método 1: Usando Makefile
make run

# Método 2: Direto
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (React)
```bash
cd src/frontend
npm run dev
```

#### Acessar aplicação:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Frontend**: http://localhost:3000

### 🧪 Testes

#### Executar todos os testes
```bash
# Usando Makefile
make test

# Com cobertura detalhada
pytest --cov=src --cov=api --cov=automation --cov-report=html --cov-fail-under=90

# Testes específicos
pytest tests/unit/ -v          # Testes unitários
pytest tests/integration/ -v   # Testes de integração
pytest tests/e2e/ -v          # Testes end-to-end
```

#### Verificar qualidade do código
```bash
# Formatação e linting
make quality

# Verificar sem modificar
make check
```

### 🔄 CI/CD Pipeline

O projeto possui pipeline automatizado configurado no GitHub Actions com as seguintes etapas:

#### 1. **Verificações de Qualidade**
- Pre-commit hooks (formatação, linting)
- Análise estática de código
- Verificação de imports e dependências

#### 2. **Testes Automatizados**
```yaml
# Matriz de testes
python-version: [3.11, 3.12]
test-types:
  - unit: Testes unitários com cobertura
  - integration: Testes de integração
  - frontend: Testes React/TypeScript  
  - automation: Testes de automação serverless
  - api-health: Verificações de saúde da API
```

#### 3. **Deploy Automatizado**
- **Staging**: Deploy automático na branch `develop`
- **Production**: Deploy automático na branch `main`
- **Plataforma**: Vercel com otimizações serverless

#### 4. **Monitoramento**
- Cobertura de código via Codecov
- Health checks contínuos
- Métricas de performance

### 📊 Comandos de Monitoramento
# Status geral do projeto
python scripts/verificar_progresso.py

# Gerar relatório de saúde
python scripts/health_check.py

# Backup do banco
make backup-db

# Limpeza de cache
make clea

Autenticação
POST /api/v1/auth/login - Login de usuário
GET /api/v1/auth/me - Dados do usuário atual
POST /api/v1/auth/users - Criar usuário (admin)
Folha de Pagamento
GET /api/v1/payroll/employees - Listar funcionários
POST /api/v1/payroll/employees - Criar funcionário
GET /api/v1/payroll/competencies - Listar competências
POST /api/v1/payroll/calculate - Calcular folha
Documentos
POST /api/v1/documents/upload - Upload de documento
GET /api/v1/documents/ - Listar documentos
GET /api/v1/documents/{id} - Obter documento
CCT
GET /api/v1/cct/ - Listar CCTs
POST /api/v1/cct/ - Criar CCT
POST /api/v1/cct/{id}/compare/{other_id} - Comparar CCTs
IA e Chatbot
POST /api/v1/ai/chat - Conversar com chatbot
GET /api/v1/ai/recommendations - Obter recomendações
GET /api/v1/ai/knowledge-base/search - Buscar na base
🗄️ Modelos de Dados
Principais Entidades
User: Usuários com permissões granulares
Employee: Funcionários com dados completos
PayrollCompetency: Competências de folha
PayrollItem: Itens individuais de folha
Document: Documentos com versionamento
CCT: Convenções coletivas de trabalho
Notification: Sistema de notificações
AuditExecution: Execuções de auditoria
ComplianceRule: Regras de compliance
🔧 Configuração
Variáveis de Ambiente
# Database
DATABASE_URL=******host/db

# Storage
R2_ENDPOINT_URL=https://account.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=auditoria360-storage

# Security
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256

# AI Services
OPENAI_API_KEY=your_openai_key

# Notifications
SENDGRID_API_KEY=your_sendgrid_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
🧪 Testes
# Executar testes unitários
pytest tests/ -v

# Executar com cobertura
pytest --cov=src --cov-report=html

# Testes E2E
pytest e2e_tests/ -v
📦 Deploy
Vercel (Recomendado)
Conectar repositório ao Vercel
Configurar variáveis no painel da Vercel
Deploy automático via GitHub Actions
Manual
# Build do frontend
cd src/frontend && npm run build

# Deploy da API
vercel --prod
🔐 Segurança
Autenticação
JWT tokens com expiração
Refresh tokens seguros
Rate limiting
Dados
Criptografia AES-256 para dados sensíveis
Hashing bcrypt para senhas
Backup criptografado
LGPD
Consentimento explícito registrado
Anonimização automática
Direito ao esquecimento
📈 Monitoramento
Logs: Estruturados com rastreabilidade
Métricas: Performance e uso
Alertas: Notificações automáticas
Health Checks: Verificação contínua
🤝 Contribuição
Fork o repositório
Crie uma branch para feature (git checkout -b feature/nova-funcionalidade)
Commit suas mudanças (git commit -am 'Add nova funcionalidade')
Push para a branch (git push origin feature/nova-funcionalidade)
Abra um Pull Request
📄 Licença
Este projeto é proprietário. Todos os direitos reservados.

📞 Suporte
Email: support@auditoria360.com
Documentação: [Portal de Documentação]
Issues: GitHub Issues para reportar bugs

📚 Documentação Consolidada
📋 **[RELATÓRIO UNIFICADO](docs/RELATORIO_UNIFICADO_AUDITORIA360.md)** - Status consolidado do projeto, arquitetura e roadmap
📁 **[Documentação Completa](docs/README.md)** - Índice de todos os documentos técnicos

AUDITORIA360 - Transformando a gestão de folha de pagamento com tecnologia avançada e conformidade total.
