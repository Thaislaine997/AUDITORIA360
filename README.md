# AUDITORIA360 🔍

> **Plataforma Integrada de Auditoria, Gestão da Folha e Compliance**

Uma solução completa e moderna para auditoria de folha de pagamento, análise de CCTs (Convenções Coletivas de Trabalho), e gestão de compliance trabalhista.

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Frontend Tests](https://img.shields.io/badge/frontend%20tests-passing-brightgreen)]()

## 🚀 Funcionalidades Principais

- **📊 Dashboard Executivo**: Métricas e indicadores de performance em tempo real
- **💰 Gestão de Folha**: Análise completa da folha de pagamento e identificação de inconsistências
- **📋 Análise de CCTs**: Revisão automática de cláusulas e sugestões de compliance
- **🔍 Auditoria Inteligente**: Identificação automática de riscos e irregularidades
- **🤖 Assistente AI**: Chatbot integrado para consultas e orientações
- **📄 Geração de Relatórios**: Templates personalizáveis para diferentes tipos de auditoria
- **🔐 Multi-tenancy**: Isolamento seguro de dados por empresa/cliente

## 🏗️ Arquitetura


### Frontend
- **React 18**: Interface moderna e responsiva
- **TypeScript**: Tipagem estática para maior robustez
- **Material-UI**: Componentes de interface profissionais
- **Zustand**: Gerenciamento de estado global simplificado
- **Vite**: Build tool ultra-rápido

### Infraestrutura
- **Docker**: Containerização da aplicação
- **Cloudflare R2**: Armazenamento de arquivos
- **GitHub Actions**: CI/CD automatizado
- **Streamlit**: Dashboards administrativos

## 📦 Instalação Rápida

### Pré-requisitos
- Node.js 18+
- Python 3.12+
- Docker (opcional)

### 1. Clone o repositório
```bash
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
```

### 2. Configuração do Backend
```bash
# Instalar dependências Python
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.template .env
# Edite o arquivo .env com suas configurações
```

### 3. Configuração do Frontend
```bash
# Navegar para o frontend
cd src/frontend

# Instalar dependências
npm install

# Executar em modo de desenvolvimento
npm run dev
```

### 4. Execução
```bash
# Backend (raiz do projeto)
python test_api_server.py

# Frontend (em outro terminal)
cd src/frontend && npm run dev
```

Acesse:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8001
- **Documentação da API**: http://localhost:8001/docs

## 🔧 Configuração

### Variáveis de Ambiente Essenciais

```bash
# Segurança
SECRET_KEY=sua_chave_secreta_aqui_minimo_32_caracteres
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Banco de Dados
DATABASE_URL=postgresql://username:password@host:port/database

# OpenAI
OPENAI_API_KEY=sua_chave_openai_aqui

# Multi-tenant
ENABLE_TENANT_ISOLATION=true
ENFORCE_COMPANY_FILTERING=true
```

Consulte o arquivo `.env.template` para uma lista completa das configurações disponíveis.

## 📁 Estrutura do Projeto

```
AUDITORIA360/
├── 📂 apps/                    # Módulos organizados da aplicação
│   ├── auth/                   # Sistema de autenticação
│   ├── core/                   # Funcionalidades centrais
│   ├── models/                 # Modelos de dados
│   └── services/               # Camada de serviços
├── 📂 config/                  # Configurações unificadas
├── 📂 src/frontend/            # Aplicação React
│   ├── components/             # Componentes reutilizáveis
│   ├── pages/                  # Páginas da aplicação
│   ├── stores/                 # Gerenciamento de estado (Zustand)
│   └── modules/                # Módulos específicos
├── 📂 docs-source/             # Documentação centralizada
├── 📂 tests/                   # Testes automatizados
└── 📂 .github/workflows/       # Automações CI/CD
```

## 🧪 Testes

### Backend
```bash
# Executar todos os testes
python -m pytest

# Testes específicos
python -m pytest tests/unit/
python -m pytest tests/integration/
```

### Frontend
```bash
cd src/frontend

# Executar testes
npm run test

# Testes com cobertura
npm run test:coverage

# Testes em modo watch
npm run test:ui
```

## 📚 Documentação

A documentação completa está disponível em:
- **[Wiki do GitHub](https://github.com/Thaislaine997/AUDITORIA360/wiki)** (sincronizada automaticamente)
- **[Documentação de Desenvolvimento](docs-source/developer-guides/)**
- **[Guias do Usuário](docs-source/user-manuals/)**
- **[Referência da API](docs-source/api-reference/)**

## 🔒 Segurança

### Recursos de Segurança Implementados
- ✅ Isolamento multi-tenant automático
- ✅ Autenticação JWT com expiração
- ✅ Validação de entrada em todas as APIs
- ✅ Headers de segurança configurados
- ✅ Rate limiting implementado
- ✅ Logs de auditoria completos

### Boas Práticas
- Todas as senhas são hashadas com bcrypt
- Secrets gerenciados via variáveis de ambiente
- Validação de permissões em tempo de execução
- Isolamento de dados por empresa garantido

## 🚀 Deploy

### Produção com Docker
```bash
# Build das imagens
docker-compose build

# Executar em produção
docker-compose up -d
```

### Deploy na Nuvem
Consulte o [Guia de Deploy](docs-source/DEPLOYMENT_GUIDE.md) para instruções específicas de cada provedor.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

Consulte [CONTRIBUTING.md](docs-source/developer-guides/contributing.md) para diretrizes detalhadas.

## 🏆 Status do Projeto

### ✅ Concluído
- [x] Estrutura do projeto reorganizada
- [x] Frontend com React + TypeScript funcionando
- [x] Sistema de autenticação robusto
- [x] Gerenciamento de estado com Zustand
- [x] Testes automatizados frontend/backend
- [x] Documentação centralizada
- [x] CI/CD com GitHub Actions

### 🚧 Em Desenvolvimento
- [ ] Implementação completa da análise de CCTs
- [ ] Dashboard de métricas em tempo real
- [ ] Integração com mais provedores de dados
- [ ] Relatórios avançados com BI

### 📋 Roadmap
- [ ] Aplicativo móvel (React Native)
- [ ] Integração com sistemas ERP
- [ ] Machine Learning para detecção de anomalias
- [ ] API pública para integrações

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 📞 Suporte

- **📧 Email**: suporte@auditoria360.com
- **💬 Issues**: [GitHub Issues](https://github.com/Thaislaine997/AUDITORIA360/issues)
- **📖 Wiki**: [Documentação Completa](https://github.com/Thaislaine997/AUDITORIA360/wiki)

---

**Desenvolvido com ❤️ pela equipe AUDITORIA360**

*"Transformando a auditoria trabalhista através da tecnologia"*