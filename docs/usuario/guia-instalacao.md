# 📦 Guia de Instalação - AUDITORIA360

> **Guia completo para instalação e configuração** do sistema AUDITORIA360 em diferentes ambientes

---

## 🎯 **Opções de Instalação**

- **[🚀 Instalação Rápida](#instalação-rápida)** - Para usuários que querem começar rapidamente
- **[👨‍💻 Instalação para Desenvolvimento](#instalação-para-desenvolvimento)** - Para desenvolvedores
- **[🏭 Instalação para Produção](#instalação-para-produção)** - Para deploy em produção
- **[🐳 Instalação com Docker](#instalação-com-docker)** - Usando containerização

---

## 🚀 **Instalação Rápida**

### Pré-requisitos Mínimos
```yaml
Python: "3.11+"
Git: "2.40+"
```

### Passos Rápidos
```bash
# 1. Clone o repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# 2. Instalar dependências
make install

# 3. Configurar ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 4. Executar a aplicação
make run
```

### Acesso
- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 👨‍💻 **Instalação para Desenvolvimento**

### Pré-requisitos Completos
```yaml
# Essenciais
Python: "3.11+"
Node.js: "18.x LTS"
Git: "2.40+"

# Opcionais (recomendados)
Docker: "24.0+"
VS Code: "Latest"
```

### 1. Clone e Setup Inicial
```bash
# Clone do repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# Configurar upstream (para contribuidores)
git remote add upstream https://github.com/Thaislaine997/AUDITORIA360.git
```

### 2. Ambiente Python
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências de desenvolvimento
make install-dev
```

### 3. Configuração do Ambiente
```bash
# Copiar arquivo de configuração
cp .env.example .env

# Configurar variáveis (edite o arquivo .env)
nano .env
```

**Variáveis Obrigatórias**:
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Storage
R2_ENDPOINT_URL=https://account.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=auditoria360-storage

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256

# AI (opcional)
OPENAI_API_KEY=your_openai_key
```

### 4. Setup de Qualidade de Código
```bash
# Instalar pre-commit hooks
make setup-hooks

# Verificar qualidade do código
make check
```

### 5. Frontend (Opcional)
```bash
# Navegar para frontend
cd src/frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
```

### 6. Verificação da Instalação
```bash
# Executar testes
make test

# Verificar cobertura
pytest --cov=src --cov-report=html

# Executar API
make run
```

---

## 🏭 **Instalação para Produção**

### Pré-requisitos de Produção
```yaml
# Servidor
Linux: "Ubuntu 20.04+"
Python: "3.11+"
Nginx: "1.18+"
Supervisor: "4.0+"

# Databases
PostgreSQL: "13+"
Redis: "6.0+"

# Monitoramento
Prometheus: "2.40+"
Grafana: "9.0+"
```

### 1. Preparação do Servidor
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
sudo apt install -y python3.11 python3.11-venv python3-pip nginx supervisor redis-server

# Criar usuário para aplicação
sudo useradd -m -s /bin/bash auditoria360
sudo su - auditoria360
```

### 2. Deploy da Aplicação
```bash
# Clone em produção
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# Configurar ambiente de produção
python3.11 -m venv venv
source venv/bin/activate
make install

# Configurar variáveis de produção
cp .env.production .env
# Editar com dados reais de produção
```

### 3. Configuração do Nginx
```nginx
# /etc/nginx/sites-available/auditoria360
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Configuração do Supervisor
```ini
# /etc/supervisor/conf.d/auditoria360.conf
[program:auditoria360]
command=/home/auditoria360/AUDITORIA360/venv/bin/uvicorn api.index:app --host 0.0.0.0 --port 8000
directory=/home/auditoria360/AUDITORIA360
user=auditoria360
autostart=true
autorestart=true
stdout_logfile=/var/log/auditoria360.log
stderr_logfile=/var/log/auditoria360_error.log
```

### 5. Deploy com Script
```bash
# Usar script de deploy automatizado
python scripts/python/deploy_production.py --environment prod
```

---

## 🐳 **Instalação com Docker**

### Usando Docker Compose
```bash
# Clone do repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# Configurar variáveis
cp .env.example .env
# Edite as variáveis conforme necessário

# Executar com Docker
docker-compose up -d
```

### Docker Personalizado
```dockerfile
# Build da imagem
docker build -t auditoria360 .

# Executar container
docker run -d \
  --name auditoria360-app \
  -p 8000:8000 \
  --env-file .env \
  auditoria360
```

---

## ✅ **Verificação da Instalação**

### Health Check Básico
```bash
# Verificar se a API está rodando
curl http://localhost:8000/health

# Resposta esperada:
{
  "status": "healthy",
  "timestamp": "2025-01-29T12:00:00Z",
  "version": "4.0.0"
}
```

### Testes Funcionais
```bash
# Executar suite completa de testes
make test

# Testes específicos
pytest tests/integration/ -v

# Testes de performance
pytest tests/performance/ -v
```

### Verificação de Endpoints
```bash
# Listar todos os endpoints
curl http://localhost:8000/docs

# Teste de autenticação
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'
```

---

## 🛠️ **Configurações Avançadas**

### Configuração de Monitoramento
```bash
# Setup completo de monitoramento
python scripts/python/setup_monitoring.py --enable-alerts

# Configurar métricas
echo "MONITORING_ENABLED=true" >> .env
echo "PROMETHEUS_PORT=9090" >> .env
```

### Integração com MCP (GitHub Copilot)
```bash
# Configurar integração MCP
echo "MCP_ENABLED=true" >> .env
echo "MCP_SERVER_PORT=3001" >> .env

# Testar integração
python scripts/python/demo_mcp_integration.py
```

### Configuração de SSL/TLS
```bash
# Obter certificado SSL (certbot)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# Configurar renovação automática
sudo crontab -e
# Adicionar linha:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🔧 **Solução de Problemas**

### Problemas Comuns

#### 1. Erro de Dependências
```bash
# Limpar cache do pip
pip cache purge

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

#### 2. Erro de Banco de Dados
```bash
# Verificar conectividade
python -c "from src.models.database import engine; print(engine.url)"

# Aplicar migrações
python scripts/python/migrate_database.py
```

#### 3. Erro de Permissões
```bash
# Corrigir permissões de arquivos
sudo chown -R auditoria360:auditoria360 /home/auditoria360/AUDITORIA360
chmod +x scripts/python/*.py
```

### Logs e Debugging
```bash
# Ver logs da aplicação
tail -f /var/log/auditoria360.log

# Logs do Docker
docker logs auditoria360-app -f

# Debug mode
export DEBUG=true
make run
```

---

## 📞 **Suporte**

### Documentação
- **[Troubleshooting](troubleshooting.md)** - Solução de problemas
- **[FAQ](faq.md)** - Perguntas frequentes
- **[Manual do Usuário](manual-usuario.md)** - Guia completo de uso

### Contato
- **Issues**: [GitHub Issues](https://github.com/Thaislaine997/AUDITORIA360/issues)
- **Documentação**: [Portal de Docs](../00-INDICE_PRINCIPAL.md)
- **Email**: support@auditoria360.com

---

> 📊 **Tempo estimado de instalação**: 15-30 minutos (desenvolvimento) | 1-2 horas (produção)

**Última atualização**: Janeiro 2025 | **Versão**: 4.0