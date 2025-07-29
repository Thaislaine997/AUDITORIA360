# AUDITORIA360 - Portal de Gestão da Folha, Auditoria 360 e CCT

> **🎯 PROJETO 96% CONCLUÍDO** - Sistema completo de auditoria e gestão de folha de pagamento com tecnologia serverless

Portal seguro, inteligente e integrado para centralizar, automatizar e auditar todos os processos de folha de pagamento, obrigações sindicais e convenções coletivas.

## 📚 **NAVEGAÇÃO DA DOCUMENTAÇÃO**

### 🚀 **Acesso Rápido**
- **[📋 ÍNDICE PRINCIPAL](docs/00-INDICE_PRINCIPAL.md)** ⭐ - **Portal central** de toda documentação
- **[🏁 INÍCIO RÁPIDO](docs/01-INICIO_RAPIDO.md)** ⭐ - **Guia 5 minutos** para começar
- **[📊 STATUS PROJETO](docs/relatorios/status-projeto.md)** - Situação atual detalhada

### 👥 **Por Perfil de Usuário**
- **👤 Usuários**: [Manual Completo](docs/usuario/manual-usuario.md) | [FAQ](docs/usuario/faq.md) | [Instalação](docs/usuario/guia-instalacao.md)
- **👨‍💻 Desenvolvedores**: [Guia Dev](docs/tecnico/desenvolvimento/dev-guide.md) | [APIs](docs/tecnico/apis/api-documentation.md) | [Arquitetura](docs/tecnico/arquitetura/visao-geral.md)
- **👔 Gestores**: [Análise Estratégica](docs/estrategico/analise-consolidada.md) | [Roadmap](docs/estrategico/roadmap-estrategico.md)
- **🔍 Auditores**: [Compliance](docs/compliance/auditoria/checklist-auditoria.md) | [LGPD](docs/compliance/lgpd/)

### 📖 **Documentação Técnica**
- **[🏗️ Arquitetura](docs/tecnico/arquitetura/visao-geral.md)** - Visão geral do sistema
- **[🔌 APIs](docs/tecnico/apis/api-documentation.md)** - Documentação completa de endpoints
- **[🚀 Deploy](docs/tecnico/deploy/deploy-checklist.md)** - Guia de implantação
- **[📊 Módulos](src/README.md)** - Documentação dos módulos do sistema

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

**📖 Documentação Unificada**: [**ÍNDICE PRINCIPAL**](docs/00-INDICE_PRINCIPAL.md) | [**Status Detalhado**](docs/relatorios/status-projeto.md)

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

### 👥 **Por Perfil de Usuário**
- **👤 Usuários**: [Manual do Usuário](docs/usuario/manual-usuario.md) | [FAQ](docs/usuario/faq.md)
- **👨‍💻 Desenvolvedores**: [Guia Dev](docs/tecnico/desenvolvimento/dev-guide.md) | [APIs](docs/tecnico/apis/api-documentation.md)
- **👔 Gestores**: [Análise Estratégica](docs/estrategico/analise-consolidada.md) | [Roadmap](docs/estrategico/roadmap-estrategico.md)
- **🔍 Auditores**: [Compliance](docs/compliance/auditoria/checklist-auditoria.md) | [LGPD](docs/compliance/lgpd/)

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

### 5. 📬 Central de Notificações
- **Dashboard unificado** de notificações
- **Alertas personalizados** por usuário/grupo
- **Integração** com email e SMS

### 6. 🔍 Auditoria e Compliance
- **Execuções**: Auditorias periódicas e por evento
- **Regras**: Motor configurável de compliance
- **Achados**: Detecção automática de não conformidades
- **Relatórios**: Exportação em múltiplos formatos
- **Riscos**: Avaliação e monitoramento contínuo

### 7. 🤖 IA, Chatbot e Bots Inteligentes
- **Chatbot**: Assistente treinado com base de conhecimento
- **OpenAI**: Integração para respostas contextuais
- **Recomendações**: Sistema de sugestões automáticas
- **Aprendizado**: Melhoria contínua baseada em feedback
- **Knowledge Base**: Base de conhecimento searchável

## 🚀 **INSTALAÇÃO E EXECUÇÃO**

> **💡 Para guia detalhado**: consulte [**Guia de Instalação**](docs/usuario/guia-instalacao.md) | [**Setup Desenvolvimento**](docs/tecnico/desenvolvimento/setup-ambiente.md)

### ⚡ **Início Rápido**
```bash
# 1. Clone e acesse o repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# 2. Instalar dependências
make install
# ou: pip install -r requirements.txt

# 3. Configurar ambiente
cp .env.example .env
# Editar .env com suas credenciais

# 4. Executar aplicação
make run
# ou: uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

### 📋 **Pré-requisitos**
- **Python 3.12+**
- **Node.js 18+** (para frontend)
- **Conta na Neon** (PostgreSQL serverless)
- **Conta no Cloudflare R2** (armazenamento)
- **Chave da OpenAI** (opcional, para IA)

### 🔧 **Configuração Detalhada**

#### Backend (API)
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Executar API
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

**Acessar documentação:**
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Frontend (React)
```bash
# Navegar para frontend
cd src/frontend

# Instalar dependências
npm install

# Executar aplicação
npm run dev
```

**Acessar aplicação:**
- **Frontend**: http://localhost:3000

## 📊 **ENDPOINTS DA API**

> **📖 Documentação completa**: [**API Documentation**](docs/tecnico/apis/api-documentation.md) | [**Exemplos Práticos**](docs/tecnico/apis/exemplos-praticos.md)

### 🔐 **Autenticação**
- `POST /api/v1/auth/login` - Login de usuário
- `GET /api/v1/auth/me` - Dados do usuário atual
- `POST /api/v1/auth/users` - Criar usuário (admin)

### 💼 **Folha de Pagamento**
- `GET /api/v1/payroll/employees` - Listar funcionários
- `POST /api/v1/payroll/employees` - Criar funcionário
- `GET /api/v1/payroll/competencies` - Listar competências
- `POST /api/v1/payroll/calculate` - Calcular folha

### 📄 **Documentos**
- `POST /api/v1/documents/upload` - Upload de documento
- `GET /api/v1/documents/` - Listar documentos
- `GET /api/v1/documents/{id}` - Obter documento

### 📝 **CCT (Convenções Coletivas)**
- `GET /api/v1/cct/` - Listar CCTs
- `POST /api/v1/cct/` - Criar CCT
- `POST /api/v1/cct/{id}/compare/{other_id}` - Comparar CCTs

### 🤖 **IA e Chatbot**
- `POST /api/v1/ai/chat` - Conversar com chatbot
- `GET /api/v1/ai/recommendations` - Obter recomendações
- `GET /api/v1/ai/knowledge-base/search` - Buscar na base

## 🗄️ **MODELOS DE DADOS**

> **📖 Documentação técnica**: [**Arquitetura**](docs/tecnico/arquitetura/visao-geral.md) | [**Banco de Dados**](docs/tecnico/banco-dados/)

### 📊 **Principais Entidades**
- **User**: Usuários com permissões granulares
- **Employee**: Funcionários com dados completos
- **PayrollCompetency**: Competências de folha
- **PayrollItem**: Itens individuais de folha
- **Document**: Documentos com versionamento
- **CCT**: Convenções coletivas de trabalho
- **Notification**: Sistema de notificações
- **AuditExecution**: Execuções de auditoria
- **ComplianceRule**: Regras de compliance

## 🔧 **CONFIGURAÇÃO**

> **📖 Guia completo**: [**Setup Ambiente**](docs/tecnico/desenvolvimento/setup-ambiente.md)

### 🔑 **Variáveis de Ambiente**
```bash
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

# AI Services
OPENAI_API_KEY=your_openai_key

# Notifications
SENDGRID_API_KEY=your_sendgrid_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

## 🧪 **TESTES**

> **📖 Documentação**: [**Estratégia de Testes**](docs/qualidade/estrategia-testes.md) | [**QA Checklist**](docs/qualidade/qa-checklist.md)

```bash
# Executar testes unitários
pytest tests/ -v

# Executar com cobertura
pytest --cov=src --cov-report=html

# Testes E2E
pytest e2e_tests/ -v
```

## 📦 **DEPLOY**

> **📖 Guia completo**: [**Deploy Checklist**](docs/tecnico/deploy/deploy-checklist.md) | [**Monitoramento**](docs/tecnico/deploy/monitoring-setup-guide.md)

### 🚀 **Vercel (Recomendado)**
1. Conectar repositório ao Vercel
2. Configurar variáveis no painel da Vercel  
3. Deploy automático via GitHub Actions

### 🔧 **Manual**
```bash
# Build do frontend
cd src/frontend && npm run build

# Deploy da API
vercel --prod
```

## 🔐 **SEGURANÇA E COMPLIANCE**

> **📖 Documentação**: [**Políticas Segurança**](docs/compliance/seguranca/politicas-seguranca.md) | [**LGPD**](docs/compliance/lgpd/)

### 🔒 **Autenticação**
- **JWT tokens** com expiração configurável
- **Refresh tokens** seguros e rotativos
- **Rate limiting** anti-abuso

### 🛡️ **Proteção de Dados**
- **Criptografia AES-256** para dados sensíveis
- **Hashing bcrypt** para senhas
- **Backup criptografado** automatizado

### ⚖️ **LGPD Compliance**
- **Consentimento explícito** registrado
- **Anonimização automática** de dados
- **Direito ao esquecimento** implementado

## 📈 **MONITORAMENTO**

### 📊 **Métricas e Observabilidade**
- **Logs estruturados** com rastreabilidade completa
- **Métricas de performance** e uso em tempo real  
- **Alertas automáticos** personalizáveis
- **Health Checks** contínuos de todos os serviços

## 🤝 **CONTRIBUIÇÃO**

> **📖 Guia completo**: [**Como Contribuir**](docs/tecnico/desenvolvimento/contribuicao.md)

1. **Fork** o repositório
2. **Crie** uma branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Add nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

## 📄 **LICENÇA**
Este projeto é proprietário. Todos os direitos reservados.

## 📞 **SUPORTE**

### 🆘 **Canais de Suporte**
- **Email**: support@auditoria360.com
- **Documentação**: [Portal Documentação](docs/00-INDICE_PRINCIPAL.md)
- **Issues**: [GitHub Issues](https://github.com/Thaislaine997/AUDITORIA360/issues) para reportar bugs
- **FAQ**: [Perguntas Frequentes](docs/usuario/faq.md)

### 🔧 **Resolução de Problemas**
- **Troubleshooting**: [Guia de Problemas](docs/usuario/troubleshooting.md)
- **FAQ Técnico**: [Dúvidas Desenvolvimento](docs/tecnico/desenvolvimento/faq-tecnico.md)

---

## 📚 **DOCUMENTAÇÃO CONSOLIDADA**

### 🎯 **Documentos Principais**
- **[📋 ÍNDICE PRINCIPAL](docs/00-INDICE_PRINCIPAL.md)** - Portal central de navegação
- **[🏁 INÍCIO RÁPIDO](docs/01-INICIO_RAPIDO.md)** - Guia 5 minutos para começar  
- **[📊 STATUS PROJETO](docs/relatorios/status-projeto.md)** - Situação atual (96% concluído)
- **[📈 ANÁLISE ESTRATÉGICA](docs/estrategico/analise-consolidada.md)** - Visão executiva completa

### 🗂️ **Por Categoria**
- **[🛠️ Técnico](docs/tecnico/)** - APIs, arquitetura, desenvolvimento
- **[👥 Usuário](docs/usuario/)** - Manuais, FAQ, tutoriais
- **[✅ Compliance](docs/compliance/)** - Auditoria, LGPD, segurança
- **[📊 Relatórios](docs/relatorios/)** - Status, performance, métricas

---

> **🚀 AUDITORIA360** - Transformando a gestão de folha de pagamento com tecnologia serverless avançada e conformidade total.
