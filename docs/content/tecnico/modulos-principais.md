# Documentação dos Módulos Principais - AUDITORIA360

## Visão Geral

Este documento fornece uma visão detalhada de todos os módulos principais do sistema AUDITORIA360, suas responsabilidades e como utilizá-los.

---

## 📁 Estrutura de Módulos

### 🧠 **src/ai_agent.py**

**Responsabilidade**: Agente de IA principal com integração MCP

```python
from src.ai_agent import AIAgent, process_user_query

# Exemplo de uso
agent = AIAgent()
response = await agent.process_query("Calcular folha de pagamento do funcionário 123")
```

**Funcionalidades**:

- Processamento de consultas em linguagem natural
- Integração com Model Context Protocol (MCP)
- Execução de ferramentas especializadas
- Interface com modelos de IA (OpenAI, etc.)

---

### 🔐 **src/auth/** - Módulo de Autenticação

#### `src/auth/unified_auth.py`

**Responsabilidade**: Sistema unificado de autenticação

```python
from src.auth.unified_auth import AuthManager, verify_token

# Verificar token JWT
user = await verify_token(token)
if user:
    print(f"Usuário autenticado: {user.email}")
```

**Funcionalidades**:

- Autenticação JWT
- Gerenciamento de sessões
- Controle de permissões
- Integração com OAuth2

---

### 🏗️ **src/core/** - Núcleo do Sistema

#### `src/core/config.py`

**Responsabilidade**: Gerenciamento centralizado de configurações

```python
from src.core.config import ConfigManager

config = ConfigManager()
database_url = config.get('DATABASE_URL')
```

#### `src/core/exceptions.py`

**Responsabilidade**: Exceções customizadas do sistema

```python
from src.core.exceptions import ValidationError, ProcessingError

try:
    # Operação que pode falhar
    process_document()
except ValidationError as e:
    logger.error(f"Erro de validação: {e}")
```

#### `src/core/security.py`

**Responsabilidade**: Funcionalidades de segurança

```python
from src.core.security import SecurityManager

security = SecurityManager()
encrypted_data = security.encrypt_sensitive_data(data)
```

---

### 🔌 **src/mcp/** - Model Context Protocol

#### `src/mcp/server.py`

**Responsabilidade**: Servidor MCP para integração com Copilot

```python
from src.mcp.server import MCPServer

server = MCPServer()
await server.start()
```

#### `src/mcp/client.py`

**Responsabilidade**: Cliente MCP para conexões externas

```python
from src.mcp.client import MCPClient

client = MCPClient("mcp://external-server")
result = await client.call_tool("calculate_payroll", params)
```

#### `src/mcp/tools.py`

**Responsabilidade**: Ferramentas MCP disponíveis

**Ferramentas Disponíveis**:

- `payroll_calculator`: Cálculo de folha de pagamento
- `compliance_checker`: Verificação de conformidade
- `audit_executor`: Execução de auditorias
- `cct_analyzer`: Análise de convenções coletivas

---

### 📊 **src/models/** - Modelos de Dados

#### `src/models/auth_models.py`

**Responsabilidade**: Modelos de autenticação e usuários

```python
from src.models.auth_models import User, Role, Permission

user = User(email="user@example.com", role="admin")
```

#### `src/models/payroll_models.py`

**Responsabilidade**: Modelos de folha de pagamento

```python
from src.models.payroll_models import Employee, PayrollCompetency, PayrollItem

employee = Employee(name="João Silva", cpf="123.456.789-00")
```

#### `src/models/document_models.py`

**Responsabilidade**: Modelos para gestão de documentos

```python
from src.models.document_models import Document, DocumentVersion

doc = Document(title="CCT 2024", type="convention")
```

#### `src/models/audit_models.py`

**Responsabilidade**: Modelos para auditoria e compliance

```python
from src.models.audit_models import AuditExecution, ComplianceRule

audit = AuditExecution(type="monthly", status="running")
```

---

### 🔧 **src/services/** - Serviços de Negócio

#### `src/services/ocr/`

**Responsabilidade**: Serviços de OCR (Optical Character Recognition)

```python
from src.services.ocr import OCRService

ocr = OCRService()
text = await ocr.extract_text_from_pdf("document.pdf")
```

#### `src/services/storage/`

**Responsabilidade**: Gerenciamento de armazenamento

```python
from src.services.storage import StorageService

storage = StorageService()
url = await storage.upload_file("file.pdf", bucket="documents")
```

---

### 🛠️ **src/utils/** - Utilitários

#### `src/utils/monitoring.py`

**Responsabilidade**: Monitoramento e métricas

```python
from src.utils.monitoring import MonitoringManager

monitor = MonitoringManager()
monitor.track_api_call("payroll_calculation", duration=1.5)
```

#### `src/utils/performance.py`

**Responsabilidade**: Otimização de performance

```python
from src.utils.performance import cache_result, measure_time

@cache_result(ttl=3600)
@measure_time
def expensive_calculation():
    # Cálculo pesado
    pass
```

---

## 🚀 **API Principal**

### `api/index.py`

**Responsabilidade**: API principal FastAPI

```python
# Endpoints principais:
# GET /health - Health check
# POST /api/v1/auth/login - Autenticação
# GET /api/v1/payroll/employees - Listar funcionários
# POST /api/v1/documents/upload - Upload de documentos
```

### `api/dashboard.py`

**Responsabilidade**: Dashboard e métricas

```python
# Endpoints do dashboard:
# GET /dashboard/metrics - Métricas principais
# GET /dashboard/charts - Dados para gráficos
```

---

## 📜 **Scripts Principais**

### `scripts/python/`

#### `deploy_production.py`

**Responsabilidade**: Deploy em produção

```bash
python scripts/python/deploy_production.py --environment prod
```

#### `setup_monitoring.py`

**Responsabilidade**: Configuração de monitoramento

```bash
python scripts/python/setup_monitoring.py --enable-alerts
```

#### `demo_mcp_integration.py`

**Responsabilidade**: Demonstração da integração MCP

```bash
python scripts/python/demo_mcp_integration.py
```

#### `onboarding_cliente.py`

**Responsabilidade**: Onboarding de novos clientes

```bash
python scripts/python/onboarding_cliente.py --client-id new-client
```

---

## 🔗 **Integração entre Módulos**

### Fluxo Típico de Processamento

1. **Requisição** → `api/index.py`
2. **Autenticação** → `src/auth/unified_auth.py`
3. **Processamento** → `src/services/` (OCR, Storage, etc.)
4. **Dados** → `src/models/` (Validação e persistência)
5. **Resposta** → JSON formatado

### Integração com IA

1. **Consulta** → `src/ai_agent.py`
2. **MCP** → `src/mcp/server.py`
3. **Ferramentas** → `src/mcp/tools.py`
4. **Execução** → Módulos específicos

---

## 📚 **Próximos Passos**

### Para Desenvolvedores

1. Consulte o [Guia de Desenvolvimento](desenvolvimento/dev-guide.md)
2. Veja exemplos práticos em [APIs](apis/exemplos-praticos.md)
3. Configure o ambiente seguindo [Setup](desenvolvimento/setup-ambiente.md)

### Para Contribuições

1. Siga os padrões em [Padrões de Código](../../qualidade/PADRONIZACAO_PYTHON.md)
2. Execute testes com `make test`
3. Use pre-commit hooks: `make setup-hooks`

---

> 📊 **Estatísticas**: 50+ módulos documentados | 8 categorias principais | Integração MCP completa | Exemplos práticos incluídos

**Última atualização**: Janeiro 2025 | **Status**: Documentação Completa
