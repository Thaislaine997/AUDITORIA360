# Core Module - AUDITORIA360

Este módulo contém a funcionalidade central do sistema AUDITORIA360, incluindo configuração, validação de dados e utilitários de logging.

## Estrutura

```
src/core/
├── __init__.py          # Exportações do módulo
├── config_manager.py    # Gerenciamento de configurações
├── validators.py        # Validações de dados (CPF, CNPJ, email, etc.)
├── log_utils.py         # Utilitários de logging
└── README.md           # Esta documentação
```

## Componentes

### ConfigManager
Gerenciamento centralizado de configurações do sistema.

```python
from src.core import ConfigManager

config = ConfigManager()
```

### Validators
Funções de validação para dados brasileiros e internacionais.

```python
from src.core import validate_cpf, validate_cnpj, validate_email

# Validar CPF
if validate_cpf("123.456.789-01"):
    print("CPF válido")

# Validar CNPJ  
if validate_cnpj("12.345.678/0001-90"):
    print("CNPJ válido")
```

### Logging
Sistema centralizado de logging com suporte a arquivo CSV.

```python
from src.core import setup_logging, get_logger

logger = setup_logging()
app_logger = get_logger("my_app")
```

## Responsabilidades

O módulo `core` é responsável por:

1. **Configuração**: Carregamento e gerenciamento de configurações do sistema
2. **Validação**: Validação de dados de entrada (CPF, CNPJ, email, telefone)
3. **Logging**: Sistema centralizado de logs e auditoria
4. **Utilitários base**: Funções fundamentais utilizadas em todo o sistema

## Uso

Importe as funcionalidades necessárias:

```python
# Importação individual
from src.core import ConfigManager, validate_cpf, setup_logging

# Importação da classe de validação
from src.core import DataValidator

validator = DataValidator()
if validator.validate_cpf("12345678901"):
    print("CPF válido")
```