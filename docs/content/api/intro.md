# Documentação da API AUDITORIA360

Esta seção contém a documentação completa da API do sistema AUDITORIA360.

## Visão Geral

O AUDITORIA360 é um sistema modular para auditoria e compliance, composto por diversos módulos integrados:

### Módulos Principais

1. **Autenticação e Autorização** (`src.auth`)
   - Sistema unificado de autenticação JWT e SSO
   - Gestão de usuários e permissões
   - Controle de acesso baseado em roles (RBAC)

2. **Modelos de Dados** (`src.models`)
   - Modelos SQLAlchemy para todas as entidades do sistema
   - Relacionamentos e validações de dados
   - Suporte a múltiplos bancos de dados

3. **Serviços de Negócio** (`src.services`)
   - Lógica de negócio centralizada
   - Serviços de cache para otimização
   - Processamento de folha de pagamento

4. **APIs REST** (`src.api`)
   - Endpoints RESTful completos
   - Documentação automática com FastAPI
   - Validação de entrada com Pydantic

5. **Utilitários** (`src.utils`)
   - Ferramentas de performance e monitoramento
   - Integrações com sistemas externos
   - Funcionalidades de apoio

## Arquitetura

```
src/
├── auth/           # Sistema de autenticação
├── models/         # Modelos de dados SQLAlchemy
├── services/       # Lógica de negócio
├── api/           # Endpoints da API REST
├── schemas/       # Esquemas Pydantic
├── core/          # Configurações centrais
├── utils/         # Utilitários e ferramentas
└── mcp/           # Integração MCP
```

## Documentação Automática

A documentação é gerada automaticamente a partir dos docstrings do código-fonte usando:

- **Sphinx** para documentação técnica detalhada
- **MkDocs** para documentação de usuário
- **FastAPI** para documentação interativa da API

## Como Usar

Para acessar a documentação interativa da API:

1. Execute o servidor: `uvicorn api.index:app --reload`
2. Acesse: `http://localhost:8000/docs` (Swagger UI)
3. Ou: `http://localhost:8000/redoc` (ReDoc)

Para gerar a documentação offline:

```bash
# Documentação Sphinx
make docs-build

# Documentação MkDocs
make docs-deploy
```
