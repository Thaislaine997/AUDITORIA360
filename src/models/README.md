# src/models/

Modelos Pydantic e ORM compartilhados entre backend e frontend.

## Recomendações

- Centralize validações e tipos comuns aqui
- Importe nos microserviços e dashboards conforme necessário

## Exemplos

### Modelo Pydantic

```python
from pydantic import BaseModel, EmailStr

class Cliente(BaseModel):
    nome: str
    email: EmailStr
    ativo: bool = True
```

### Modelo ORM (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClienteORM(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    ativo = Column(Boolean, default=True)
```

## Exemplo de uso

```python
from .user import User
usuario = User(nome="João", email="joao@exemplo.com")
print(usuario)
```

## Onboarding rápido

1. Instale dependências: `pip install -r requirements.txt`
2. Importe o model desejado:

```python
from .user import User
usuario = User(nome="João", email="joao@exemplo.com")
print(usuario)
```

## Boas práticas

- Use tipos explícitos e validações automáticas
- Documente campos obrigatórios e opcionais
- Mantenha exemplos de uso para facilitar integração
