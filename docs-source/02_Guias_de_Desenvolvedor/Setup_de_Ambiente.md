# 🔧 Configuração do Ambiente de Desenvolvimento

## 🎯 Visão Geral

Este guia completo orienta desenvolvedores na configuração do ambiente local para trabalhar com AUDITORIA360, desde a instalação inicial até o primeiro deploy.

## 🛠️ Pré-requisitos

### Software Obrigatório
- **Python 3.11+**
- **Node.js 18+** 
- **PostgreSQL 14+**
- **Redis 6+**
- **Docker** e **Docker Compose**
- **Git**

### Ferramentas Recomendadas
- **VS Code** com extensões Python e TypeScript
- **Postman** para testes de API
- **DBeaver** para gerenciamento do banco

## 🚀 Configuração Inicial

### 1. Clone do Repositório
```bash
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
```

### 2. Configuração do Backend

#### 2.1. Ambiente Virtual Python
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Ativar ambiente (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 2.2. Configuração de Variáveis de Ambiente
```bash
# Copiar template de configuração
cp .env.example .env

# Editar variáveis no arquivo .env
nano .env
```

**Variáveis essenciais para desenvolvimento:**
```env
# Banco de Dados
DATABASE_URL=postgresql://user:password@localhost:5432/auditoria360_dev
REDIS_URL=redis://localhost:6379/0

# Segurança
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# APIs Externas
OPENAI_API_KEY=your-openai-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token

# Desenvolvimento
DEBUG=true
ENVIRONMENT=development
```

#### 2.3. Configuração do Banco de Dados
```bash
# Criar banco de dados
createdb auditoria360_dev

# Executar migrações
python -m alembic upgrade head

# Carregar dados de exemplo (opcional)
python seed_blueprint_data.py
```

### 3. Configuração do Frontend

#### 3.1. Instalação de Dependências
```bash
cd frontend
npm install
```

#### 3.2. Configuração de Ambiente
```bash
# Copiar configuração do frontend
cp .env.example .env.local

# Editar variáveis
nano .env.local
```

**Variáveis do frontend:**
```env
VITE_API_URL=http://localhost:8000
VITE_ENVIRONMENT=development
VITE_ENABLE_DEVTOOLS=true
```

## 🏃 Executando a Aplicação

### Opção 1: Docker Compose (Recomendado)
```bash
# Na raiz do projeto
docker-compose up -d

# Verificar status
docker-compose ps

# Logs
docker-compose logs -f
```

### Opção 2: Execução Manual

#### Backend
```bash
# Terminal 1 - API
cd /caminho/para/AUDITORIA360
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Terminal 2 - Worker (opcional)
celery -A src.tasks worker --loglevel=info
```

#### Frontend
```bash
# Terminal 3 - Frontend
cd frontend
npm run dev
```

## 🔐 Configuração de Autenticação

### 1. Configuração Inicial de Auth
```bash
# Copiar templates de autenticação
cp auth/login.example.yaml auth/login.yaml
cp auth/gestor_contas.example.json auth/gestor_contas.json
```

### 2. Gerar Senhas e Chaves
```python
# Script para gerar hashes de senha
from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Gerar hash de senha
senha_hash = pwd_context.hash("sua_senha_aqui")
print(f"Hash da senha: {senha_hash}")

# Gerar chave secreta
secret_key = secrets.token_urlsafe(32)
print(f"Chave secreta: {secret_key}")
```

### 3. Configurar Usuários de Desenvolvimento
Edite `auth/gestor_contas.json`:
```json
{
  "dev_admin": {
    "password_hash": "hash_gerado_acima",
    "client_id": "dev_client",
    "role": "admin"
  }
}
```

## 🧪 Executando Testes

### Testes do Backend
```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src

# Testes específicos
pytest tests/test_auth.py
pytest tests/test_api.py -v
```

### Testes do Frontend
```bash
cd frontend

# Testes unitários
npm run test

# Testes E2E
npm run test:e2e

# Coverage
npm run test:coverage
```

## 🔍 Debugging e Desenvolvimento

### VS Code Configuration
Crie `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/src/main.py",
      "args": [],
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env"
    }
  ]
}
```

### Logs e Monitoramento
```bash
# Logs da aplicação
tail -f logs/app.log

# Monitoramento de performance
python scripts/validate_production_deploy.py

# Health check
curl http://localhost:8000/health
```

## 📋 Checklist de Validação

### ✅ Backend
- [ ] API responde em `http://localhost:8000`
- [ ] Healthcheck retorna 200: `GET /health`
- [ ] Autenticação funciona: `POST /auth/login`
- [ ] Banco de dados conectado
- [ ] Redis conectado

### ✅ Frontend  
- [ ] Interface carrega em `http://localhost:3000`
- [ ] Login funciona
- [ ] Dashboard principal carrega
- [ ] Navegação entre páginas funciona

### ✅ Integração
- [ ] Frontend consegue fazer login via API
- [ ] Dados são carregados corretamente
- [ ] Upload de arquivos funciona
- [ ] Relatórios são gerados

## 🐛 Troubleshooting

### Problemas Comuns

#### "ModuleNotFoundError"
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Ou instalar em modo desenvolvimento
pip install -e .
```

#### "Connection refused" (Banco)
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Iniciar PostgreSQL
sudo systemctl start postgresql
```

#### "Permission denied" (Docker)
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Logout e login novamente
```

## 📚 Próximos Passos

1. **Leia a [Arquitetura do Sistema](architecture-overview.md)**
2. **Consulte o [Guia de Contribuição](contributing.md)**
3. **Explore a [Documentação da API](api-documentation.md)**
4. **Configure seu [IDE para desenvolvimento](development-setup.md)**

---

💡 **Dica**: Mantenha este ambiente sempre atualizado executando `git pull` e `pip install -r requirements.txt` regularmente.

🚨 **Importante**: Nunca commite arquivos de configuração com credenciais reais (.env, auth/*.yaml, auth/*.json).