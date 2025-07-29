# Estrutura do Backend Modularizado

## Visão Geral

O backend do AUDITORIA360 foi reestruturado em uma arquitetura modular para melhorar a organização, manutenibilidade e escalabilidade do código.

## Módulos Principais

### 🏗️ [Core (src/core/)](../modularizacao-backend.md#src-core)
- Lógica de negócio central
- Configuração do sistema
- Segurança e validadores
- Exceções customizadas

### 🔧 [Services (src/services/)](../modularizacao-backend.md#src-services)
- Serviços de OCR
- Armazenamento de arquivos
- Autenticação
- Relatórios

### 🛠️ [Utils (src/utils/)](../modularizacao-backend.md#src-utils)
- Monitoramento
- Performance
- Integrações de API

## Documentação Completa

Para detalhes completos sobre a modularização, veja:
👉 **[Documentação da Modularização do Backend](../modularizacao-backend.md)**

## Início Rápido para Desenvolvedores

```python
# Importar do core
from src.core import ConfigManager, SecurityManager
from src.core.validators import validate_cpf

# Importar serviços  
from src.services.ocr import OCRService
from src.services.storage import StorageService

# Importar utilitários
from src.utils import MonitoringManager
```

## Estrutura de Diretórios

```
src/
├── core/           # Lógica central
├── services/       # Serviços de negócio
├── utils/          # Utilitários
├── api/            # Endpoints FastAPI
├── models/         # Modelos de dados
└── schemas/        # Esquemas Pydantic
```