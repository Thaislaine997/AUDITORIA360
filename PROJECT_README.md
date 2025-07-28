# AUDITORIA360 - Portal de Gestão da Folha, Auditoria 360 e CCT

Portal seguro, inteligente e integrado para centralizar, automatizar e auditar todos os processos de folha de pagamento, obrigações sindicais e convenções coletivas.

## 🎯 Objetivo

Desenvolver um portal completo que elimina processos manuais e riscos de não conformidade através de:
- Centralização e automação de processos de folha de pagamento
- Gestão inteligente de documentos e CCTs
- Sistema avançado de auditoria e compliance
- IA e chatbot para assistência especializada

## 🏗️ Arquitetura

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

## 📋 Módulos Implementados

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

### 5. 🔔 Notificações e Eventos
- **Canais**: Push, email, SMS integrados
- **Templates**: Sistema de templates configuráveis
- **Regras**: Automação baseada em eventos
- **Preferências**: Controle individual por usuário
- **Central**: Dashboard unificado de notificações

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

## 🚀 Como Executar

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- Conta na Neon (PostgreSQL)
- Conta no Cloudflare R2
- Chave da OpenAI (opcional)

### Backend (API)

1. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

2. **Configurar variáveis de ambiente**:
```bash
cp .env.example .env
# Editar .env com suas credenciais
```

3. **Executar API**:
```bash
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

4. **Acessar documentação**:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Frontend (React)

1. **Navegar para frontend**:
```bash
cd src/frontend
```

2. **Instalar dependências**:
```bash
npm install
```

3. **Executar aplicação**:
```bash
npm run dev
```

4. **Acessar aplicação**:
- Frontend: http://localhost:3000

## 📊 Endpoints da API

### Autenticação
- `POST /api/v1/auth/login` - Login de usuário
- `GET /api/v1/auth/me` - Dados do usuário atual
- `POST /api/v1/auth/users` - Criar usuário (admin)

### Folha de Pagamento
- `GET /api/v1/payroll/employees` - Listar funcionários
- `POST /api/v1/payroll/employees` - Criar funcionário
- `GET /api/v1/payroll/competencies` - Listar competências
- `POST /api/v1/payroll/calculate` - Calcular folha

### Documentos
- `POST /api/v1/documents/upload` - Upload de documento
- `GET /api/v1/documents/` - Listar documentos
- `GET /api/v1/documents/{id}` - Obter documento

### CCT
- `GET /api/v1/cct/` - Listar CCTs
- `POST /api/v1/cct/` - Criar CCT
- `POST /api/v1/cct/{id}/compare/{other_id}` - Comparar CCTs

### IA e Chatbot
- `POST /api/v1/ai/chat` - Conversar com chatbot
- `GET /api/v1/ai/recommendations` - Obter recomendações
- `GET /api/v1/ai/knowledge-base/search` - Buscar na base

## 🗄️ Modelos de Dados

### Principais Entidades
- **User**: Usuários com permissões granulares
- **Employee**: Funcionários com dados completos
- **PayrollCompetency**: Competências de folha
- **PayrollItem**: Itens individuais de folha
- **Document**: Documentos com versionamento
- **CCT**: Convenções coletivas de trabalho
- **Notification**: Sistema de notificações
- **AuditExecution**: Execuções de auditoria
- **ComplianceRule**: Regras de compliance

## 🔧 Configuração

### Variáveis de Ambiente

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

# AI Services
OPENAI_API_KEY=your_openai_key

# Notifications
SENDGRID_API_KEY=your_sendgrid_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

## 🧪 Testes

```bash
# Executar testes unitários
pytest tests/ -v

# Executar com cobertura
pytest --cov=src --cov-report=html

# Testes E2E
pytest e2e_tests/ -v
```

## 📦 Deploy

### Vercel (Recomendado)

1. **Conectar repositório** ao Vercel
2. **Configurar variáveis** no painel da Vercel
3. **Deploy automático** via GitHub Actions

### Manual

```bash
# Build do frontend
cd src/frontend && npm run build

# Deploy da API
vercel --prod
```

## 🔐 Segurança

### Autenticação
- JWT tokens com expiração
- Refresh tokens seguros
- Rate limiting

### Dados
- Criptografia AES-256 para dados sensíveis
- Hashing bcrypt para senhas
- Backup criptografado

### LGPD
- Consentimento explícito registrado
- Anonimização automática
- Direito ao esquecimento

## 📈 Monitoramento

- **Logs**: Estruturados com rastreabilidade
- **Métricas**: Performance e uso
- **Alertas**: Notificações automáticas
- **Health Checks**: Verificação contínua

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é proprietário. Todos os direitos reservados.

## 📞 Suporte

- **Email**: support@auditoria360.com
- **Documentação**: [Portal de Documentação]
- **Issues**: GitHub Issues para reportar bugs

---

**AUDITORIA360** - Transformando a gestão de folha de pagamento com tecnologia avançada e conformidade total.