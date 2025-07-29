# Guia Rápido - Padrões de Código Python

## Setup Inicial (Uma vez)

```bash
# Instalar ferramentas
pip install black isort flake8 autoflake

# Configurar pre-commit (recomendado)
pip install pre-commit
pre-commit install
```

## Comandos Diários

### Antes de Commit

```bash
# Formatar código
make format

# Ou manualmente:
black .
isort .
autoflake --in-place --remove-all-unused-imports --recursive .
```

### Verificar Qualidade

```bash
# Verificar violações
flake8 .

# Verificar se formatação está correta
black --check .
isort --check-only .
```

## Configuração do Editor

### VSCode

```json
{
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=88"],
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### PyCharm

1. Settings → Tools → External Tools
2. Adicionar Black e isort como ferramentas externas
3. Configurar shortcuts para formatação

## Padrões do Projeto

### Imports

```python
# ✅ Correto
import os
import sys
from typing import List, Optional

import requests
import pandas as pd

from src.models import User
from .utils import helper_function
```

### Formatação

```python
# ✅ Correto - linha <= 88 caracteres
long_variable_name = some_function_with_long_name(
    parameter_one="value",
    parameter_two="another_value",
    parameter_three="third_value"
)

# ✅ Correto - f-strings com placeholders
message = f"User {user.name} has {user.count} items"

# ❌ Evitar - f-string sem placeholder
log_message = f"Starting process"  # Use string normal
log_message = "Starting process"   # ✅ Melhor
```

### Variáveis

```python
# ✅ Correto
def process_data(data: List[dict]) -> dict:
    result = {}
    for item in data:
        result[item['id']] = item['value']
    return result

# ❌ Evitar variáveis não utilizadas
def process_data(data: List[dict]) -> dict:
    unused_var = "something"  # Será removido por autoflake
    return {"processed": len(data)}
```

## Integração CI/CD

### GitHub Actions

```yaml
- name: Python Code Quality
  run: |
    flake8 . --count --max-line-length=88 --statistics
    black --check .
    isort --check-only .
```

### Makefile

```makefile
format:
	black .
	isort .
	autoflake --in-place --remove-all-unused-imports --recursive .

lint:
	flake8 .

check:
	black --check .
	isort --check-only .
	flake8 .
```

## Violações Comuns e Soluções

| Código | Problema                    | Solução                               |
| ------ | --------------------------- | ------------------------------------- |
| E501   | Linha muito longa           | `black .` resolve automaticamente     |
| F401   | Import não utilizado        | `autoflake` remove automaticamente    |
| E302   | Faltam linhas em branco     | `black .` adiciona automaticamente    |
| W293   | Linha em branco com espaços | `black .` limpa automaticamente       |
| F811   | Nome redefinido             | Verificar se é intencional ou remover |

## Comandos Úteis

```bash
# Contar violações antes/depois
flake8 --count .

# Ver apenas tipos de erro
flake8 . | cut -d: -f4 | cut -d' ' -f2 | sort | uniq -c

# Formatar apenas arquivos modificados
git diff --name-only --cached | grep '\.py$' | xargs black
```

## Suporte

- 📚 Documentação completa: `docs/qualidade/PADRONIZACAO_PYTHON.md`
- ⚙️ Configurações: `.flake8`, `pyproject.toml`
- 🤝 Dúvidas: Abrir issue ou contatar equipe de desenvolvimento

---

_Atualizado em conjunto com a padronização do projeto AUDITORIA360_
