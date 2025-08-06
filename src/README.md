# src/ - Código-fonte Principal

## Propósito

Diretório principal contendo o código-fonte central do AUDITORIA360, incluindo utilitários, serviços, modelos e componentes principais do sistema.

## Principais Funcionalidades

- **utils/**: Utilitários e funções auxiliares compartilhadas
- **services/**: Serviços core do sistema
- **models/**: Modelos Pydantic e ORM
- **auth/**: Módulos de autenticação e autorização
- **api/**: APIs e endpoints principais
- **mcp/**: Master Collective Protocol - Sistema de inteligência de enxame
- **serverless/**: Funções serverless e arquitetura distribuída
- **schemas/**: Esquemas de validação de dados
- **monitoring/**: Sistema de monitoramento e métricas
- **frontend/**: Interface de usuário React

## Instruções de Uso

### Instalação de Dependências

```bash
# Dependências principais
pip install -r requirements.txt

# Dependências de desenvolvimento
pip install -r requirements-dev.txt

# Dependências de ML
pip install -r requirements-ml.txt
```

### Execução

```bash
# Iniciar servidor principal
python src/main.py

# Executar API FastAPI
uvicorn src.api.main:app --reload
```

## Exemplos

### Importar Utilitários

```python
from src.utils.helpers import format_data
from src.models.user import User
from src.services.audit import AuditService
```

### Usar Serviços

```python
from src.services.audit import AuditService

audit_service = AuditService()
result = audit_service.process_audit_data(data)
```

## Dependências

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Redis (opcional)

Para lista completa, consulte `requirements.txt` e arquivos relacionados.