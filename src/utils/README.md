# src/utils/

Funções utilitárias e helpers para uso em todo o projeto.

## Exemplos

- Conversão de tipos
- Formatação de datas
- Funções de logging

### Conversão de tipos

```python
def to_int(valor):
    try:
        return int(valor)
    except Exception:
        return 0
```

### Formatação de datas

```python
from datetime import datetime

def formatar_data(dt):
    return dt.strftime('%d/%m/%Y')
```

### Função de logging

```python
import logging

def log_info(msg):
    logging.info(msg)
```

## Boas práticas

- Mantenha funções genéricas e reutilizáveis
- Documente exemplos de uso
- Evite dependências desnecessárias

## Onboarding rápido

1. Instale dependências: `pip install -r requirements.txt`
2. Importe o utilitário desejado:

```python
from .date_utils import format_date
print(format_date("2025-07-24"))
```
