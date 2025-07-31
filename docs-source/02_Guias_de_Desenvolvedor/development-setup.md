# 🔧 Setup do Ambiente de Desenvolvimento

> **Guia completo para configurar o ambiente local do AUDITORIA360**

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
VS_Code: "Latest"  # Recomendado
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
# Verificar versão do Python
python --version  # Deve ser 3.11+

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/macOS)
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip
```

### 3️⃣ **Dependências Python**
```bash
# Instalar dependências de desenvolvimento
make install-dev

# Ou manualmente:
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-ml.txt
```

### 4️⃣ **Node.js e Frontend**
```bash
# Verificar versão do Node.js
node --version  # Deve ser 18.x+

# Instalar dependências
npm install

# Verificar instalação
npm run --silent
```

### 5️⃣ **Configuração do Ambiente**
```bash
# Copiar template de configuração
cp .env.template .env

# Editar variáveis de ambiente
nano .env  # ou seu editor preferido
```

#### **Variáveis Principais (.env)**
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
NEON_DATABASE_URL=postgresql://...

# Storage
CLOUDFLARE_R2_ACCESS_KEY_ID=your_key
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_secret

# IA e ML
OPENAI_API_KEY=sk-...
VERTEX_AI_PROJECT_ID=your_project

# Autenticação
JWT_SECRET_KEY=your_secure_secret
OAUTH_CLIENT_ID=your_oauth_client

# Monitoramento (opcional)
SENTRY_DSN=https://...
```

---

## 🐳 **DOCKER (Opcional)**

### **Setup com Docker**
```bash
# Build da imagem
docker build -t auditoria360 .

# Executar com docker-compose
docker-compose up -d

# Verificar containers
docker ps
```

### **Docker Compose**
```yaml
# docker-compose.yml (simplificado)
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - .:/app
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=auditoria360
      - POSTGRES_USER=dev
      - POSTGRES_PASSWORD=dev123
```

---

## 🧪 **VERIFICAÇÃO DA INSTALAÇÃO**

### **Testes de Sistema**
```bash
# Verificar configuração
make check

# Executar testes
make test

# Verificar cobertura
pytest --cov=src --cov-report=html

# Linting
make lint

# Formatação
make format
```

### **Iniciar Servidor de Desenvolvimento**
```bash
# Backend (FastAPI)
make run
# ou
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000

# Frontend (se aplicável)
npm run dev

# Streamlit (dashboard)
streamlit run portal_demandas/main.py
```

### **URLs de Desenvolvimento**
- **API**: http://localhost:8001
- **Docs**: http://localhost:8001/docs
- **Dashboard**: http://localhost:8501
- **Frontend**: http://localhost:3000 (se aplicável)

---

## 🔧 **CONFIGURAÇÃO DA IDE**

### **VS Code (Recomendado)**

#### **Extensões Essenciais**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8", 
    "ms-python.black-formatter",
    "ms-python.isort",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "esbenp.prettier-vscode"
  ]
}
```

#### **Settings.json**
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### **PyCharm (Alternativa)**
```bash
# Configurações importantes:
# - Python Interpreter: ./venv/bin/python
# - Code Style: Black
# - Inspections: Enable all Python inspections
# - Run Configuration: FastAPI app
```

---

## 🗄️ **CONFIGURAÇÃO DO BANCO**

### **Neon (Produção)**
```bash
# Conectar com Neon PostgreSQL
export DATABASE_URL="postgresql://user:pass@host.neon.tech/db"

# Executar migrações
python -m alembic upgrade head
```

### **Local (Desenvolvimento)**
```bash
# PostgreSQL local
docker run -d \
  --name postgres-dev \
  -e POSTGRES_DB=auditoria360 \
  -e POSTGRES_USER=dev \
  -e POSTGRES_PASSWORD=dev123 \
  -p 5432:5432 \
  postgres:15

# Variável local
export DATABASE_URL="postgresql://dev:dev123@localhost:5432/auditoria360"
```

### **DuckDB (Testes)**
```python
# Para testes rápidos
import duckdb
conn = duckdb.connect('test.db')
```

---

## 🧩 **ESTRUTURA DO PROJETO**

```
AUDITORIA360/
├── 📁 api/                     # FastAPI backend
├── 📁 src/                     # Core business logic
│   ├── 📁 models/             # Data models
│   ├── 📁 services/           # Business services
│   └── 📁 utils/              # Utilities
├── 📁 portal_demandas/        # Streamlit dashboard
├── 📁 tests/                  # Test suites
│   ├── 📁 unit/              # Unit tests
│   ├── 📁 integration/       # Integration tests
│   └── 📁 e2e/               # End-to-end tests
├── 📁 docs-source/           # Documentation source
├── 📁 scripts/               # Utility scripts
├── 📄 Makefile               # Development commands
├── 📄 pyproject.toml         # Python configuration
└── 📄 requirements*.txt      # Dependencies
```

---

## 🔍 **DEBUGGING**

### **Configuração do Debugger**

#### **VS Code launch.json**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["api.index:app", "--reload"],
      "jinja": true,
      "console": "integratedTerminal"
    },
    {
      "name": "Streamlit",
      "type": "python", 
      "request": "launch",
      "module": "streamlit",
      "args": ["run", "portal_demandas/main.py"]
    }
  ]
}
```

### **Logs e Monitoramento**
```python
# Configuração de logs
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🚨 **TROUBLESHOOTING**

### **Problemas Comuns**

#### **❌ ImportError: No module named 'xxx'**
```bash
# Verificar ambiente virtual ativo
which python
pip list

# Reinstalar dependências
pip install -r requirements.txt
```

#### **❌ Port already in use**
```bash
# Encontrar processo usando porta
lsof -i :8000

# Matar processo
kill -9 <PID>
```

#### **❌ Database connection error**
```bash
# Verificar DATABASE_URL
echo $DATABASE_URL

# Testar conexão
python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')"
```

#### **❌ Git permission denied**
```bash
# Configurar SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
gh auth login
```

### **Performance Issues**
```bash
# Monitorar recursos
htop  # CPU/Memory
iotop # Disk I/O

# Profiling Python
python -m cProfile your_script.py
```

---

## 📚 **PRÓXIMOS PASSOS**

Após configurar o ambiente:

1. **[📖 Guia de Desenvolvimento](./development-guide)** - Workflow e práticas
2. **[🏗️ Arquitetura](./architecture-overview)** - Como o sistema funciona  
3. **[📡 APIs](./api-documentation)** - Documentação das APIs
4. **[🧪 Testes](./testing-guide)** - Como escrever e executar testes
5. **[🤝 Contribuição](./contributing)** - Como contribuir com o projeto

---

## 📞 **Suporte**

### **Problemas de Setup**
- **[🐛 Issues](https://github.com/Thaislaine997/AUDITORIA360/issues)**
- **[💬 Discussions](https://github.com/Thaislaine997/AUDITORIA360/discussions)**
- **[📧 Email](mailto:dev@auditoria360.com.br)**

### **Documentação Adicional**
- **[🔧 Makefile Commands](../../README.md#commands)**
- **[🐳 Docker Guide](./docker-guide)**
- **[☁️ Cloud Setup](./cloud-setup)**

---

> **💡 Dica**: Mantenha sempre seu ambiente atualizado! Execute `git pull && make install-dev` regularmente.