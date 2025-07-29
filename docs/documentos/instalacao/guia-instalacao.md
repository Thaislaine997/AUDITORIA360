# Manual de Instalação - AUDITORIA360

## 🎯 Objetivo

Este manual fornece instruções detalhadas para instalar e configurar o sistema AUDITORIA360 em diferentes ambientes.

## 📋 Pré-requisitos

### Sistema Operacional
- Ubuntu 20.04+ / macOS 11+ / Windows 10+ (com WSL2)
- Mínimo 4GB RAM, recomendado 8GB+
- 10GB espaço livre em disco

### Software Base
- **Python 3.12+** - Linguagem principal
- **Node.js 18+** - Frontend e ferramentas
- **Git** - Controle de versão
- **Docker** (opcional) - Para containers

### Contas de Serviços
- **Neon Database** - PostgreSQL serverless
- **Cloudflare R2** - Armazenamento de arquivos
- **OpenAI** (opcional) - Funcionalidades de IA
- **GitHub** - Repositório e CI/CD

## 🚀 Instalação Rápida

### 1. Clonar Repositório
```bash
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
```

### 2. Instalar Dependências
```bash
# Python
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Node.js (para frontend)
cd src/frontend
npm install
cd ../..
```

### 3. Configurar Ambiente
```bash
# Copiar arquivo de configuração
cp .env.example .env

# Editar variáveis (veja seção configuração)
nano .env
```

### 4. Verificar Instalação
```bash
# Verificar API
python -c "from api.index import app; print('✅ API OK')"

# Verificar testes
make test

# Verificar qualidade
make check
```

## ⚙️ Configuração Detalhada

### Variáveis de Ambiente Essenciais

```env
# === DATABASE ===
DATABASE_URL=postgresql://user:pass@host.neon.tech/dbname?sslmode=require

# === STORAGE ===
R2_ENDPOINT_URL=https://abc123.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key_id
R2_SECRET_ACCESS_KEY=your_secret_access_key
R2_BUCKET_NAME=auditoria360-storage

# === SECURITY ===
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# === AI SERVICES (opcional) ===
OPENAI_API_KEY=sk-your-openai-key

# === NOTIFICATIONS (opcional) ===
SENDGRID_API_KEY=SG.your-sendgrid-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### Configuração do Banco Neon

1. **Criar conta no Neon:**
   - Acesse https://neon.tech
   - Crie um novo projeto
   - Copie a connection string

2. **Configurar DATABASE_URL:**
   ```env
   DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
   ```

### Configuração do Cloudflare R2

1. **Criar bucket R2:**
   - Acesse Cloudflare Dashboard
   - Vá para R2 Object Storage
   - Crie um novo bucket

2. **Configurar credenciais:**
   ```env
   R2_ENDPOINT_URL=https://abc123.r2.cloudflarestorage.com
   R2_ACCESS_KEY_ID=your_key
   R2_SECRET_ACCESS_KEY=your_secret
   R2_BUCKET_NAME=auditoria360-storage
   ```

## 🏃‍♂️ Execução

### Desenvolvimento Local
```bash
# Backend
make run
# ou
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# Frontend (nova aba)
cd src/frontend
npm run dev
```

### Produção
```bash
# Build frontend
cd src/frontend
npm run build

# Deploy via Vercel
vercel --prod
```

## 🧪 Validação da Instalação

### Testes Básicos
```bash
# Testes unitários
pytest tests/unit/ -v

# Testes de integração
pytest tests/integration/ -v

# Cobertura completa
pytest --cov=src --cov-report=html
```

### Health Checks
```bash
# API Health
curl http://localhost:8000/health

# Verificar banco
python -c "from src.database.connection import test_connection; test_connection()"

# Verificar storage
python -c "from src.services.storage_service import test_connection; test_connection()"
```

## 🔧 Troubleshooting

### Problemas Comuns

#### Erro de Conexão com Banco
```bash
# Verificar conexão
ping your-neon-host.com

# Verificar SSL
openssl s_client -connect your-host:5432 -servername your-host
```

#### Problemas com Dependências
```bash
# Limpar cache pip
pip cache purge

# Reinstalar dependências
pip install --force-reinstall -r requirements.txt
```

#### Erro no Frontend
```bash
# Limpar node_modules
cd src/frontend
rm -rf node_modules package-lock.json
npm install
```

### Logs e Debugging
```bash
# Logs da API
tail -f logs/api.log

# Logs detalhados
export LOG_LEVEL=DEBUG
python -m uvicorn api.index:app --reload
```

## 📁 Estrutura de Arquivos

```
AUDITORIA360/
├── api/                 # FastAPI backend
├── src/                 # Código principal
│   ├── frontend/        # React app
│   ├── services/        # Serviços Python
│   └── models/          # Modelos de dados
├── docs/                # Documentação
├── tests/               # Testes
├── scripts/             # Scripts auxiliares
├── requirements.txt     # Dependências Python
├── Makefile            # Comandos automatizados
└── .env                # Configurações (criar)
```

## 🎉 Próximos Passos

Após instalação bem-sucedida:

1. **[Manual do Usuário](../manuais/manual-usuario.md)** - Como usar o sistema
2. **[Manual do Desenvolvedor](../manuais/manual-desenvolvedor.md)** - Desenvolvimento avançado
3. **[Configuração de Deploy](../../../tecnico/deploy/)** - Deploy em produção

---

**Suporte**: Para problemas na instalação, abra uma issue no GitHub ou consulte a [FAQ](../manuais/faq.md)