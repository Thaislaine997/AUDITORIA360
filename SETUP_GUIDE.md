# AUDITORIA360 - Guia de Configuração e Deploy

## 📋 Índice
- [Configuração Local](#configuração-local)
- [Deploy e Publicação](#deploy-e-publicação)
- [Troubleshooting](#troubleshooting)
- [Sistema de Autenticação](#sistema-de-autenticação)

## 🖥️ Configuração Local

### Pré-requisitos
- **Node.js** 18+ (recomendado 20+)
- **Python** 3.12+
- **Git**
- **Docker** (opcional)

### 1. Clone do Repositório
```bash
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
```

### 2. Configuração do Backend (Python/FastAPI)

#### Instalação das Dependências
```bash
# Instalar dependências Python
pip install -r requirements.txt

# Ou usando ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

#### Configuração das Variáveis de Ambiente
```bash
# Copiar template de configuração
cp .env.template .env

# Editar o arquivo .env com suas configurações
nano .env
```

**Variáveis Essenciais:**
```env
# Segurança (OBRIGATÓRIO)
SECRET_KEY=sua_chave_secreta_aqui_minimo_32_caracteres_muito_segura

# Autenticação
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Banco de Dados (se usando PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database

# OpenAI (opcional, para recursos de IA)
OPENAI_API_KEY=sua_chave_openai_aqui

# Multi-tenant
ENABLE_TENANT_ISOLATION=true
ENFORCE_COMPANY_FILTERING=true
```

#### Executar o Backend
```bash
# Servidor de desenvolvimento
python test_api_server.py

# Ou usando uvicorn diretamente
uvicorn test_api_server:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Configuração do Frontend (React/TypeScript)

#### Navegação para o Diretório Frontend
```bash
cd src/frontend
```

#### Instalação das Dependências
```bash
# Instalar dependências Node.js
npm install

# Ou usando yarn
yarn install
```

#### Executar o Frontend
```bash
# Servidor de desenvolvimento
npm run dev

# Ou usando yarn
yarn dev
```

### 4. Verificação da Configuração

Após executar ambos os servidores:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **Documentação da API**: http://localhost:8001/docs

## 🚀 Deploy e Publicação

### Construção para Produção

#### Frontend
```bash
cd src/frontend

# Build de produção
npm run build

# Testar build localmente
npm run preview
```

#### Backend
```bash
# Configurar variáveis de produção
export SECRET_KEY="sua_chave_production_muito_segura"
export DATABASE_URL="postgresql://user:password@prod-db:5432/auditoria360"

# Executar em produção
python test_api_server.py
```

### Deploy com Docker

#### Dockerfile Frontend (exemplo)
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY src/frontend/package*.json ./
RUN npm ci --only=production

COPY src/frontend/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose (exemplo)
```yaml
version: '3.8'
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8001:8001"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: auditoria360
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Deploy em Serviços Cloud

#### Vercel (Frontend)
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
cd src/frontend
vercel --prod
```

#### Railway/Render (Backend)
```bash
# Configurar arquivo de build (se necessário)
echo "python test_api_server.py" > Procfile
```

## 🔐 Sistema de Autenticação

### Usuários Padrão

O sistema vem configurado com usuários de exemplo para testes:

| Usuário | Senha | Tipo | Descrição |
|---------|-------|------|-----------|
| `admin` | `admin123` | `super_admin` | Acesso total ao sistema |
| `contabilidade` | `conta123` | `contabilidade` | Acesso restrito a contabilidade |

### Tipos de Usuário e Permissões

#### Super Admin (`super_admin`)
- ✅ Acesso total ao sistema
- ✅ Gestão de contabilidades
- ✅ Gestão de usuários
- ✅ Configurações globais

#### Contabilidade (`contabilidade`)
- ✅ Gestão de clientes próprios
- ✅ Relatórios da contabilidade
- ❌ Gestão de usuários
- ❌ Acesso a outras contabilidades

#### Cliente Final (`cliente_final`)
- ✅ Visualização de dados próprios
- ✅ Download de documentos
- ❌ Gestão de usuários
- ❌ Configurações administrativas

### Fluxo de Autenticação

1. **Login**: Usuário fornece credenciais
2. **Validação**: Backend valida credenciais
3. **Token JWT**: Sistema gera token com informações do usuário
4. **Autorização**: Frontend adapta interface baseada no tipo de usuário
5. **Filtragem**: Backend filtra dados baseado no escopo do usuário

## 🛠️ Troubleshooting

### Problemas Comuns

#### Tela em Branco no Frontend
```bash
# Verificar se há erros no console do navegador
# Verificar se o backend está rodando
curl http://localhost:8001/health

# Limpar cache do navegador
# Verificar se as dependências estão instaladas
cd src/frontend && npm install
```

#### API Offline/Inacessível
```bash
# Verificar se o backend está rodando
ps aux | grep python

# Verificar logs do backend
python test_api_server.py

# Verificar conectividade
curl -I http://localhost:8001/health
```

#### Erro de CORS
```bash
# Verificar se o CORS está configurado no backend
# O arquivo test_api_server.py deve incluir:
# app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])
```

#### Build não Funciona
```bash
# Frontend
cd src/frontend
rm -rf node_modules
npm install
npm run build

# Backend
pip install -r requirements.txt
python test_api_server.py
```

### Logs e Depuração

#### Habilitar Logs Detalhados
```bash
# Backend
export LOG_LEVEL=DEBUG
python test_api_server.py

# Frontend (dev mode)
npm run dev
```

#### Verificar Configuração
```bash
# Verificar variáveis de ambiente
env | grep -E "(SECRET_KEY|DATABASE_URL|OPENAI_API_KEY)"

# Verificar conectividade do banco
python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print('DB OK' if engine else 'DB ERROR')"
```

### Comandos Úteis

```bash
# Reinstalar dependências
rm -rf node_modules package-lock.json && npm install

# Limpar cache do projeto
npm run clean  # se disponível

# Verificar status dos serviços
curl http://localhost:3000  # Frontend
curl http://localhost:8001/health  # Backend

# Executar testes
npm run test  # Frontend
python -m pytest  # Backend
```

---

## 📞 Suporte

- **📧 Issues**: [GitHub Issues](https://github.com/Thaislaine997/AUDITORIA360/issues)
- **📖 Documentação**: [Wiki do Projeto](https://github.com/Thaislaine997/AUDITORIA360/wiki)
- **🔧 Configuração**: Consulte este guia ou abra uma issue

## 📝 Checklist de Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] Dependências instaladas (frontend e backend)
- [ ] Build de produção testado
- [ ] Banco de dados configurado
- [ ] Certificados SSL configurados (produção)
- [ ] Monitoramento configurado
- [ ] Backup de dados configurado
- [ ] Logs de aplicação configurados