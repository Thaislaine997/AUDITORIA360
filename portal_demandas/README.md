# 🎫 Portal Demandas - Sistema de Gestão de Tickets

Portal integrado para gerenciamento de demandas e tickets do AUDITORIA360, agora completamente migrado para SQLAlchemy + Neon PostgreSQL.

## 🚀 Características

### ✅ **Migração Completa SQLAlchemy + Neon**

- ✅ Modelos Pydantic robustos com validação
- ✅ SQLAlchemy ORM com PostgreSQL otimizado
- ✅ Conexão Neon PostgreSQL serverless
- ✅ API FastAPI moderna e async
- ✅ Paginação, filtros e busca avançada
- ✅ Sistema de comentários
- ✅ Estatísticas e relatórios
- ✅ Operações em lote
- ✅ Tratamento robusto de erros

### 📊 **Funcionalidades**

- **CRUD Completo**: Criar, listar, atualizar e deletar tickets
- **Filtros Avançados**: Status, prioridade, categoria, responsável, etapa
- **Busca Textual**: Busca no título e descrição
- **Paginação**: Listagem paginada com controle de itens por página
- **Comentários**: Sistema de comentários por ticket
- **Estatísticas**: Dashboards e métricas em tempo real
- **Operações em Lote**: Atualização de múltiplos tickets
- **Auditoria**: Logs de criação e atualização

## 🏗️ Arquitetura

### Stack Tecnológica

- **Backend**: FastAPI + SQLAlchemy
- **Database**: Neon PostgreSQL (serverless)
- **Validação**: Pydantic models
- **ORM**: SQLAlchemy 2.0
- **Documentação**: OpenAPI/Swagger automática

### Estrutura de Arquivos

```
portal_demandas/
├── __init__.py              # Módulo principal
├── api.py                   # FastAPI application
├── models.py                # Pydantic models
├── db.py                    # SQLAlchemy models + DB config
├── tests/                   # Testes automatizados
│   ├── __init__.py
│   ├── test_api.py          # Testes da API
│   ├── test_models.py       # Testes dos models
│   └── conftest.py          # Configuração de testes
└── README.md                # Este arquivo
```

## 📋 Modelos de Dados

### Ticket (Modelo Principal)

```python
class Ticket:
    id: int                          # ID único
    titulo: str                      # Título do ticket
    descricao: Optional[str]         # Descrição detalhada
    etapa: str                       # Etapa do processo
    prazo: datetime                  # Prazo para conclusão
    responsavel: str                 # Responsável pelo ticket
    status: TicketStatus             # pendente, em_andamento, concluido, etc.
    prioridade: TicketPrioridade     # baixa, media, alta, critica
    categoria: TicketCategoria       # geral, auditoria, folha, etc.
    tags: Optional[str]              # Tags separadas por vírgula
    comentarios_internos: Optional[str]  # Comentários internos
    arquivo_anexo: Optional[str]     # Caminho do arquivo anexo
    tempo_estimado: Optional[int]    # Tempo estimado (horas)
    tempo_gasto: Optional[int]       # Tempo gasto (horas)
    criado_em: datetime              # Data de criação
    atualizado_em: datetime          # Data de atualização
```

### Enumerações

- **TicketStatus**: `pendente`, `em_andamento`, `aguardando`, `concluido`, `cancelado`
- **TicketPrioridade**: `baixa`, `media`, `alta`, `critica`
- **TicketCategoria**: `geral`, `auditoria`, `folha`, `documentos`, `cct`, `sistema`

## 🔌 API Endpoints

### Tickets

| Método   | Endpoint               | Descrição                    |
| -------- | ---------------------- | ---------------------------- |
| `POST`   | `/tickets/`            | Criar novo ticket            |
| `GET`    | `/tickets/`            | Listar tickets (com filtros) |
| `GET`    | `/tickets/{id}`        | Obter ticket específico      |
| `PATCH`  | `/tickets/{id}`        | Atualizar ticket             |
| `DELETE` | `/tickets/{id}`        | Deletar ticket               |
| `PATCH`  | `/tickets/bulk/status` | Atualizar status em lote     |

### Comentários

| Método | Endpoint                  | Descrição            |
| ------ | ------------------------- | -------------------- |
| `POST` | `/tickets/{id}/comments/` | Adicionar comentário |
| `GET`  | `/tickets/{id}/comments/` | Listar comentários   |

### Estatísticas

| Método | Endpoint  | Descrição                 |
| ------ | --------- | ------------------------- |
| `GET`  | `/stats/` | Obter estatísticas gerais |

### Utilitários

| Método | Endpoint  | Descrição    |
| ------ | --------- | ------------ |
| `GET`  | `/health` | Health check |

## 📝 Exemplos de Uso

### 1. Criar Ticket

```bash
curl -X POST "http://localhost:8001/tickets/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Auditoria de Folha - Janeiro 2024",
    "descricao": "Revisar cálculos da folha de pagamento de janeiro",
    "etapa": "Análise Inicial",
    "prazo": "2024-02-15T10:00:00",
    "responsavel": "João Silva",
    "prioridade": "alta",
    "categoria": "auditoria",
    "tempo_estimado": 8
  }'
```

### 2. Listar Tickets com Filtros

```bash
curl "http://localhost:8001/tickets/?status=pendente&prioridade=alta&page=1&per_page=10"
```

### 3. Buscar Tickets

```bash
curl "http://localhost:8001/tickets/?search=auditoria&sort_by=criado_em&sort_order=desc"
```

### 4. Atualizar Status

```bash
curl -X PATCH "http://localhost:8001/tickets/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "em_andamento",
    "comentarios_internos": "Iniciando análise dos dados"
  }'
```

### 5. Adicionar Comentário

```bash
curl -X POST "http://localhost:8001/tickets/1/comments/" \
  -H "Content-Type: application/json" \
  -d '{
    "autor": "Maria Santos",
    "comentario": "Encontrada inconsistência no cálculo de horas extras",
    "tipo": "comentario"
  }'
```

### 6. Obter Estatísticas

```bash
curl "http://localhost:8001/stats/"
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
pytest portal_demandas/tests/

# Testes específicos
pytest portal_demandas/tests/test_api.py -v
pytest portal_demandas/tests/test_models.py -v

# Com cobertura
pytest portal_demandas/tests/ --cov=portal_demandas --cov-report=html
```

### Estrutura de Testes

- **test_api.py**: Testes de endpoints da API
- **test_models.py**: Testes de validação dos models
- **conftest.py**: Configuração de fixtures de teste

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
NEON_DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/db

# API
API_HOST=localhost
API_PORT=8001
```

### Configuração de Desenvolvimento

```python
# .env.local
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/portal_dev
DEBUG=true
LOG_LEVEL=INFO
```

## 🚀 Execução

### Servidor de Desenvolvimento

```bash
# Usando uvicorn diretamente
uvicorn portal_demandas.api:app --reload --host 0.0.0.0 --port 8001

# Usando o módulo
python -m portal_demandas.api

# Via Makefile (se configurado)
make run-portal
```

### Docker (Opcional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "portal_demandas.api:app", "--host", "0.0.0.0", "--port", "8001"]
```

## 📊 Monitoramento

### Health Check

```bash
curl http://localhost:8001/health
```

### Métricas Disponíveis

- Total de tickets por status
- Distribuição por prioridade e categoria
- Tempo médio de conclusão
- Tickets criados por período
- Performance de responsáveis

## 🔒 Segurança

### Implementado

- ✅ Validação de entrada com Pydantic
- ✅ Sanitização de queries SQL
- ✅ CORS configurável
- ✅ Tratamento de erros robusto
- ✅ Logs de auditoria

### Próximos Passos

- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Permissões baseadas em roles
- [ ] Criptografia de dados sensíveis

## 🚧 Roadmap

### v1.1 (Próxima Release)

- [ ] Sistema de notificações
- [ ] Upload de arquivos anexos
- [ ] Templates de tickets
- [ ] Dashboard visual
- [ ] Relatórios em PDF

### v1.2 (Futuro)

- [ ] Integração com calendário
- [ ] Automação de workflows
- [ ] Integração com Slack/Teams
- [ ] API GraphQL
- [ ] Mobile app

## 🤝 Contribuição

### Como Contribuir

1. Fork do repositório
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Criar Pull Request

### Padrões de Código

- Seguir PEP 8
- Usar type hints
- Documentar funções públicas
- Escrever testes para novas funcionalidades
- Usar pre-commit hooks

---

## 📞 Suporte

- **Documentação**: Acesse `/docs` quando o servidor estiver rodando
- **Issues**: [GitHub Issues](https://github.com/seu-repo/issues)
- **API Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
