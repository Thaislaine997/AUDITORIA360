# 🔧 Setup do Ambiente de Desenvolvimento

> **Guia completo para configurar o ambiente local** do AUDITORIA360

---

## 📋 **PRÉ-REQUISITOS**

### 💻 **Sistema Operacional**
- **Windows**: 10/11 (64-bit)
- **macOS**: 10.15+ (Catalina ou superior)
- **Linux**: Ubuntu 20.04+, CentOS 8+, Debian 11+

### 🛠️ **Ferramentas Essenciais**
```yaml
Git: "v2.40+"
Node.js: "v18.x LTS"
Python: "v3.11+"
Docker: "v24.0+"
Docker_Compose: "v2.20+"
VS_Code: "Latest" # Recomendado
```

### 🔑 **Credenciais Necessárias**
- **GitHub**: Acesso ao repositório
- **Neon**: Database credentials
- **Cloudflare**: R2 storage keys
- **OpenAI**: API key para IA
- **Vercel**: Deploy credentials (opcional)

---

## 🚀 **INSTALAÇÃO PASSO A PASSO**

### 1️⃣ **Clone do Repositório**
```bash
# Clone do repositório principal
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# Configurar upstream (contribuidores)
git remote add upstream https://github.com/Thaislaine997/AUDITORIA360.git
git remote -v
```

### 2️⃣ **Python Environment**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3️⃣ **Node.js Dependencies**
```bash
# Frontend (React)
cd dashboards
npm install

# Voltar para root
cd ..
```

### 4️⃣ **Configuração de Ambiente**
```bash
# Copiar template de configuração
cp .env.example .env

# Editar variáveis (ver seção abaixo)
# Windows
notepad .env
# macOS/Linux
nano .env
```

---

## ⚙️ **CONFIGURAÇÃO DE VARIÁVEIS**

### 🔐 **Arquivo .env Principal**
```bash
# Database (Neon PostgreSQL)
DATABASE_URL="postgresql://username:password@host:5432/database?sslmode=require"
NEON_DATABASE_URL="postgresql://..."

# Storage (Cloudflare R2)
CLOUDFLARE_R2_ENDPOINT="https://..."
CLOUDFLARE_R2_ACCESS_KEY="..."
CLOUDFLARE_R2_SECRET_KEY="..."
CLOUDFLARE_R2_BUCKET="auditoria360-docs"

# OpenAI Integration
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-4-turbo-preview"

# Authentication
JWT_SECRET="your-super-secret-jwt-key-here"
JWT_ALGORITHM="HS256"
JWT_EXPIRE_MINUTES=1440

# Environment
ENVIRONMENT="development"
DEBUG=true
LOG_LEVEL="DEBUG"

# API Configuration
API_HOST="0.0.0.0"
API_PORT=8000
CORS_ORIGINS="http://localhost:3000,http://localhost:8000"

# Monitoring (opcional para dev)
SENTRY_DSN=""
GRAFANA_URL=""
```

### 🗄️ **Database Configuration**
```bash
# Local PostgreSQL (alternativa ao Neon)
LOCAL_DATABASE_URL="postgresql://postgres:password@localhost:5432/auditoria360_dev"

# BigQuery (para testes)
GOOGLE_CLOUD_PROJECT="your-project-id"
BIGQUERY_DATASET="auditoria360_dev"
```

---

## 🐳 **DOCKER SETUP (Recomendado)**

### 📄 **docker-compose.dev.yml**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: auditoria360_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: devpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: 
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://postgres:devpassword@postgres:5432/auditoria360_dev
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
```

### 🚀 **Comandos Docker**
```bash
# Subir ambiente completo
docker-compose -f docker-compose.dev.yml up -d

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f api

# Parar ambiente
docker-compose -f docker-compose.dev.yml down

# Rebuild após mudanças
docker-compose -f docker-compose.dev.yml up --build
```

---

## 🗄️ **DATABASE SETUP**

### 📊 **Migração Inicial**
```bash
# Ativar ambiente Python
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Executar migrações
alembic upgrade head

# Popular dados de exemplo (opcional)
python scripts/seed_database.py
```

### 🔧 **Scripts Úteis**
```bash
# Backup database
python scripts/backup_database.py

# Reset database (CUIDADO!)
python scripts/reset_database.py

# Verificar conexão
python scripts/test_database.py
```

---

## 🚀 **EXECUTANDO O SISTEMA**

### 1️⃣ **Backend (API)**
```bash
# Ativar ambiente
source venv/bin/activate

# Executar API em desenvolvimento
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Ou usar script helper
python scripts/run_api.py
```

### 2️⃣ **Frontend (Dashboard)**
```bash
# Ir para pasta frontend
cd dashboards

# Executar em desenvolvimento
npm run dev

# Ou build para produção
npm run build
```

### 3️⃣ **Verificar Setup**
```bash
# API Health Check
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000

# Database connectivity
python scripts/test_connections.py
```

---

## 🧪 **TESTES E VALIDAÇÃO**

### ✅ **Executar Suite de Testes**
```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_api/
pytest tests/test_models/

# Testes E2E (requer frontend rodando)
pytest tests/e2e/
```

### 🔍 **Linting e Formatação**
```bash
# Python - Black formatter
black src/ tests/

# Python - Flake8 linter
flake8 src/ tests/

# TypeScript - ESLint
cd dashboards
npm run lint
npm run lint:fix

# TypeScript - Prettier
npm run format
```

---

## 🛠️ **FERRAMENTAS DE DESENVOLVIMENTO**

### 💻 **VS Code Extensions**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "ms-vscode-remote.remote-containers"
  ]
}
```

### 📄 **VS Code Settings**
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

### 🐳 **Dev Containers (Opcional)**
```json
{
  "name": "AUDITORIA360 Dev",
  "dockerComposeFile": "docker-compose.dev.yml",
  "service": "api",
  "workspaceFolder": "/app",
  "extensions": [
    "ms-python.python",
    "ms-python.black-formatter"
  ]
}
```

---

## 🔧 **TROUBLESHOOTING DE SETUP**

### ❌ **Problemas Comuns**

#### 🐍 **Python Issues**
```bash
# ModuleNotFoundError
pip install -r requirements.txt --force-reinstall

# Virtual environment issues
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 📦 **Node.js Issues**
```bash
# Node modules corruption
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Version mismatch
nvm use 18  # Se usando nvm
```

#### 🗄️ **Database Issues**
```bash
# Connection refused
docker-compose -f docker-compose.dev.yml up postgres -d

# Migration issues
alembic downgrade base
alembic upgrade head
```

### 🔍 **Debug Mode**
```bash
# API com debug verbose
uvicorn src.main:app --reload --log-level debug

# Frontend com debug
cd dashboards
npm run dev -- --verbose

# Database debug
export SQLALCHEMY_ECHO=true
python scripts/test_database.py
```

---

## 📚 **PRÓXIMOS PASSOS**

### 🎯 **Após Setup Completo**
1. **Explore codebase**: Veja [Guia de Desenvolvimento](dev-guide.md)
2. **Rode testes**: Garanta que tudo funciona
3. **Faça primeiro commit**: Teste workflow
4. **Configure IDE**: Extensões e settings
5. **Leia APIs**: [Documentação de APIs](../apis/api-documentation.md)

### 🤝 **Para Contribuir**
1. **Fork repositório**: Crie sua cópia
2. **Crie branch**: `git checkout -b feature/nova-funcionalidade`
3. **Desenvolva**: Siga padrões estabelecidos
4. **Teste**: Execute suite completa
5. **Pull Request**: Submeta para review

---

## 📞 **SUPORTE SETUP**

### 🆘 **Se precisar de ajuda**
- **Documentação**: [FAQ](../usuario/faq.md) | [Troubleshooting](../usuario/troubleshooting.md)
- **Issues**: Abra issue no GitHub com tag "setup"
- **Discussões**: GitHub Discussions para dúvidas
- **Contato**: Email da equipe de desenvolvimento

---

> 💡 **Dica**: Mantenha este ambiente atualizado regularmente com `git pull` e `pip install -r requirements.txt`

**Última atualização**: Janeiro 2025 | **Versão**: 4.0 | **Compatibilidade**: Python 3.11+, Node 18+