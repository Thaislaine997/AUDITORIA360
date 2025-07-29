# 📦 AUDITORIA360 - Módulos do Sistema

> **🏗️ Arquitetura modular** do sistema AUDITORIA360 com separação clara de responsabilidades

Este diretório contém todos os módulos principais do sistema, organizados seguindo padrões de arquitetura limpa e design patterns modernos.

## 🗂️ **ESTRUTURA DOS MÓDULOS**

### 📊 **Visão Geral**
```
src/
├── 🎯 core/           # Núcleo do sistema (configurações, dependências)
├── 📋 models/         # Modelos de dados e entidades
├── 🔧 services/       # Lógica de negócio e serviços
├── 🛠️ utils/          # Utilitários e helpers
├── 📡 routers/        # Rotas da API (FastAPI)
├── 🔐 auth/           # Sistema de autenticação
├── 📄 schemas/        # Schemas Pydantic (validação)
├── 🗄️ database/       # Configuração e migrations
├── 🤖 ai/             # Integrações de IA e ML
└── 🎨 frontend/       # Aplicação React (interface)
```

## 📋 **DOCUMENTAÇÃO POR MÓDULO**

### 🎯 **Core** - Sistema Base
- **Localização**: `src/core/`
- **Responsabilidade**: Configurações centrais, dependências, setup inicial
- **Principais arquivos**:
  - `config.py` - Configurações da aplicação
  - `dependencies.py` - Injeção de dependências
  - `exceptions.py` - Exceções customizadas

### 📊 **Models** - Modelos de Dados
- **Localização**: `src/models/`
- **Documentação**: [📖 Models README](models/README.md)
- **Responsabilidade**: Definição das entidades e modelos de dados
- **Principais entidades**:
  - User, Employee, Company
  - Payroll, Document, CCT
  - Audit, Compliance, Notification

### 🔧 **Services** - Lógica de Negócio
- **Localização**: `src/services/`
- **Documentação**: [📖 Services README](services/README.md)
- **Responsabilidade**: Implementação da lógica de negócio
- **Principais serviços**:
  - Processamento de folha
  - Gestão de documentos
  - Sistema de auditoria
  - Integração com IA

### 🛠️ **Utils** - Utilitários
- **Localização**: `src/utils/`
- **Documentação**: [📖 Utils README](utils/README.md)
- **Responsabilidade**: Funções auxiliares e helpers
- **Principais utilitários**:
  - Validações e formatações
  - Helpers de data/hora
  - Utilitários de criptografia
  - Processamento de arquivos

### 📡 **Routers** - API Endpoints
- **Localização**: `src/routers/`
- **Responsabilidade**: Definição das rotas da API REST
- **Principais routers**:
  - `/auth` - Autenticação e autorização
  - `/payroll` - Gestão de folha de pagamento
  - `/documents` - Gestão de documentos
  - `/audit` - Sistema de auditoria
  - `/ai` - Endpoints de IA

### 🔐 **Auth** - Autenticação
- **Localização**: `src/auth/`
- **Responsabilidade**: Sistema de autenticação e autorização
- **Principais componentes**:
  - JWT token management
  - OAuth2 integration
  - RBAC (Role-Based Access Control)
  - Session management

### 📄 **Schemas** - Validação de Dados
- **Localização**: `src/schemas/`
- **Responsabilidade**: Schemas Pydantic para validação
- **Principais schemas**:
  - Request/Response models
  - Validation schemas
  - API documentation models

### 🗄️ **Database** - Persistência
- **Localização**: `src/database/`
- **Responsabilidade**: Configuração do banco de dados
- **Principais arquivos**:
  - Database connection setup
  - Migration scripts
  - Repository patterns

### 🤖 **AI** - Inteligência Artificial
- **Localização**: `src/ai/`
- **Responsabilidade**: Integrações de IA e Machine Learning
- **Principais componentes**:
  - Chatbot integration
  - Document processing (OCR)
  - Predictive analytics
  - Natural Language Processing

### 🎨 **Frontend** - Interface de Usuário
- **Localização**: `src/frontend/`
- **Responsabilidade**: Aplicação React para interface web
- **Stack**: React.js + TypeScript + Material UI
- **Principais componentes**:
  - Dashboard administrativo
  - Gestão de funcionários
  - Relatórios e analytics
  - Interface de auditoria

## 🔗 **DEPENDÊNCIAS E INTEGRAÇÕES**

### 📦 **Principais Dependências**
```python
# API Framework
FastAPI + Uvicorn

# Database
SQLAlchemy + PostgreSQL (Neon)
DuckDB (Analytics)

# Authentication
python-jose[cryptography]
passlib[bcrypt]

# AI/ML
OpenAI API
PaddleOCR
scikit-learn

# Storage
boto3 (Cloudflare R2)

# Validation
Pydantic
```

### 🔌 **Integrações Externas**
- **Neon PostgreSQL** - Banco principal
- **Cloudflare R2** - Armazenamento de arquivos
- **OpenAI** - Serviços de IA
- **SendGrid** - Envio de emails
- **Twilio** - Notificações SMS

## 🏗️ **PADRÕES DE ARQUITETURA**

### 🎯 **Design Patterns**
- **Repository Pattern** - Camada de acesso a dados
- **Service Layer** - Lógica de negócio isolada
- **Dependency Injection** - Injeção de dependências
- **Factory Pattern** - Criação de objetos
- **Observer Pattern** - Sistema de eventos

### 📐 **Princípios SOLID**
- **Single Responsibility** - Uma responsabilidade por classe
- **Open/Closed** - Aberto para extensão, fechado para modificação
- **Liskov Substitution** - Substituição de subtipos
- **Interface Segregation** - Interfaces específicas
- **Dependency Inversion** - Dependência de abstrações

### 🔄 **Clean Architecture**
```
┌─────────────────┐
│   🎨 Frontend   │ (UI Layer)
├─────────────────┤
│   📡 Routers    │ (Presentation Layer)
├─────────────────┤
│   🔧 Services   │ (Business Logic Layer)
├─────────────────┤
│   📊 Models     │ (Data Layer)
└─────────────────┘
```

## 🧪 **TESTES E QUALIDADE**

### 📊 **Cobertura de Testes**
- **Unit Tests** - Testes isolados por módulo
- **Integration Tests** - Testes de integração
- **E2E Tests** - Testes end-to-end com Playwright
- **Coverage**: Target 90%+

### 🔍 **Code Quality**
- **Linting**: flake8, black, isort
- **Type Checking**: mypy
- **Security**: bandit
- **Documentation**: docstrings obrigatórias

## 📖 **COMO USAR**

### 🚀 **Para Desenvolvedores**
1. **Explorar**: Comece pelos READMEs específicos de cada módulo
2. **Setup**: [Setup do Ambiente](../docs/tecnico/desenvolvimento/setup-ambiente.md)
3. **Desenvolver**: [Guia de Desenvolvimento](../docs/tecnico/desenvolvimento/dev-guide.md)
4. **Testar**: Execute `pytest` para validar mudanças

### 📚 **Documentação Adicional**
- **[🏗️ Arquitetura Geral](../docs/tecnico/arquitetura/visao-geral.md)**
- **[🔌 APIs](../docs/tecnico/apis/api-documentation.md)**
- **[🚀 Deploy](../docs/tecnico/deploy/deploy-checklist.md)**
- **[📊 Banco de Dados](../docs/tecnico/banco-dados/)**

## 🤝 **CONTRIBUIÇÃO**

### 📝 **Guidelines**
- Siga os padrões estabelecidos em cada módulo
- Mantenha a documentação atualizada
- Escreva testes para novas funcionalidades
- Use type hints em todo código Python

### 🔧 **Comandos Úteis**
```bash
# Executar testes de um módulo específico
pytest src/services/tests/

# Verificar qualidade do código
flake8 src/
black src/
mypy src/

# Executar aplicação em desenvolvimento
uvicorn api.index:app --reload
```

---

> **💡 Dica**: Cada módulo tem sua própria documentação específica. Consulte os READMEs individuais para informações detalhadas sobre implementação e uso.

**Última atualização**: Janeiro 2025 | **Versão**: 4.0 | **Status**: Documentação Atualizada