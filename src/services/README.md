# 🔧 AUDITORIA360 - Serviços e Lógica de Negócio

> **⚙️ Camada de serviços** com toda a lógica de negócio e integrações do sistema AUDITORIA360

Este módulo centraliza toda a lógica de negócio, processamento de dados e integrações com serviços externos, mantendo a separação clara entre apresentação e regras de negócio.

## 🏗️ **ARQUITETURA DE SERVIÇOS**

### 📋 **Estrutura Organizacional**
```
src/services/
├── 🔐 auth_service.py        # Autenticação e autorização
├── 💼 payroll_service.py     # Processamento de folha
├── 📄 document_service.py    # Gestão de documentos
├── 📝 cct_service.py         # Convenções coletivas
├── 🔍 audit_service.py       # Sistema de auditoria
├── 🔔 notification_service.py # Envio de notificações
├── 🤖 ai_service.py          # Serviços de IA/ML
├── 💾 cache_service.py       # Sistema de cache
├── 📊 duckdb_optimizer.py    # Otimização DuckDB
└── 🔌 integration_service.py # Integrações externas
```

## 🎯 **SERVIÇOS PRINCIPAIS**

### 🔐 **Auth Service** - Autenticação
**Responsabilidades:**
- Gerenciamento de JWT tokens
- Validação de credenciais
- Controle de acesso (RBAC)
- Integração OAuth2

**Exemplo de uso:**
```python
from src.services.auth_service import AuthService

auth_service = AuthService()

# Autenticar usuário
token = auth_service.authenticate_user(
    email="user@empresa.com",
    password="senha123"
)

# Validar token
user_data = auth_service.validate_token(token)

# Verificar permissão
has_permission = auth_service.check_permission(
    user_id=1,
    resource="payroll",
    action="read"
)
```

### 💼 **Payroll Service** - Folha de Pagamento
**Responsabilidades:**
- Cálculos de folha de pagamento
- Validação de dados trabalhistas
- Geração de relatórios
- Integração com sistemas externos

**Exemplo de uso:**
```python
from src.services.payroll_service import PayrollService

payroll_service = PayrollService()

# Calcular folha
resultado = payroll_service.calculate_payroll(
    employee_id=123,
    competency="2025-01",
    base_salary=5000.00
)

# Gerar holerite
holerite = payroll_service.generate_payslip(
    employee_id=123,
    competency="2025-01"
)

# Validar cálculos
validation = payroll_service.validate_calculations(resultado)
```

### 📄 **Document Service** - Gestão de Documentos
**Responsabilidades:**
- Upload e armazenamento seguro
- Processamento OCR
- Versionamento de documentos
- Indexação e busca

**Exemplo de uso:**
```python
from src.services.document_service import DocumentService

doc_service = DocumentService()

# Upload de documento
document = doc_service.upload_document(
    file_path="/path/to/document.pdf",
    category="contracts",
    metadata={"empresa": "ACME Corp"}
)

# Processar OCR
ocr_result = doc_service.process_ocr(document.id)

# Buscar documentos
results = doc_service.search_documents(
    query="contrato trabalho",
    filters={"category": "contracts"}
)
```

### 📝 **CCT Service** - Convenções Coletivas
**Responsabilidades:**
- Processamento de CCTs
- Extração de cláusulas
- Comparação entre documentos
- Scraping automático

**Exemplo de uso:**
```python
from src.services.cct_service import CCTService

cct_service = CCTService()

# Processar CCT
cct = cct_service.process_cct_document(
    document_path="/path/to/cct.pdf",
    sindicate_id=1
)

# Extrair cláusulas
clauses = cct_service.extract_clauses(cct.id)

# Comparar CCTs
comparison = cct_service.compare_ccts(
    cct_id_1=1,
    cct_id_2=2
)
```

### 🔍 **Audit Service** - Sistema de Auditoria
**Responsabilidades:**
- Execução de auditorias
- Aplicação de regras de compliance
- Detecção de anomalias
- Geração de relatórios

**Exemplo de uso:**
```python
from src.services.audit_service import AuditService

audit_service = AuditService()

# Executar auditoria
audit_execution = audit_service.run_audit(
    company_id=1,
    audit_type="payroll_compliance",
    period="2025-01"
)

# Verificar compliance
compliance_status = audit_service.check_compliance(
    company_id=1,
    rules=["FGTS", "INSS", "IRRF"]
)

# Gerar relatório
report = audit_service.generate_audit_report(
    execution_id=audit_execution.id
)
```

### 🔔 **Notification Service** - Notificações
**Responsabilidades:**
- Envio de emails
- Notificações SMS
- Push notifications
- Templates personalizados

**Exemplo de uso:**
```python
from src.services.notification_service import NotificationService

notification_service = NotificationService()

# Enviar email
notification_service.send_email(
    to="user@empresa.com",
    template="audit_complete",
    data={"audit_id": 123, "status": "concluída"}
)

# Enviar SMS
notification_service.send_sms(
    phone="+5511999999999",
    message="Auditoria concluída com sucesso!"
)

# Notificação push
notification_service.send_push_notification(
    user_id=1,
    title="Nova Notificação",
    body="Sua auditoria foi finalizada"
)
```

### 🤖 **AI Service** - Inteligência Artificial
**Responsabilidades:**
- Chatbot interactions
- Processamento de linguagem natural
- Recomendações automáticas
- Análise preditiva

**Exemplo de uso:**
```python
from src.services.ai_service import AIService

ai_service = AIService()

# Interação com chatbot
response = ai_service.chat_interaction(
    user_message="Como calcular FGTS?",
    context={"user_role": "contador"}
)

# Gerar recomendações
recommendations = ai_service.generate_recommendations(
    user_id=1,
    context="payroll_review"
)

# Análise de documento
analysis = ai_service.analyze_document(
    document_path="/path/to/contract.pdf"
)
```

## 🔌 **INTEGRAÇÕES EXTERNAS**

### 🌐 **APIs Integradas**
```python
# Receita Federal
def consultar_cnpj(cnpj: str):
    """Consulta dados da empresa na Receita Federal"""
    # Implementação da integração
    pass

# eSocial
def enviar_evento_esocial(evento_data: dict):
    """Envia evento para o eSocial"""
    # Implementação da integração
    pass

# Banco Central
def consultar_taxa_selic():
    """Consulta taxa SELIC atual"""
    # Implementação da integração
    pass
```

### 📧 **Serviços de Comunicação**
```python
# SendGrid (Email)
def send_email_via_sendgrid(to: str, subject: str, content: str):
    """Envia email via SendGrid"""
    # Implementação
    pass

# Twilio (SMS)
def send_sms_via_twilio(phone: str, message: str):
    """Envia SMS via Twilio"""
    # Implementação
    pass
```

## 💾 **CACHE E PERFORMANCE**

### 🚀 **Cache Service**
```python
from src.services.cache_service import CacheService

cache = CacheService()

# Cachear resultado
cache.set("payroll_123_2025-01", payroll_data, ttl=3600)

# Recuperar do cache
cached_data = cache.get("payroll_123_2025-01")

# Invalidar cache
cache.delete("payroll_123_*")
```

### 📊 **DuckDB Optimizer**
```python
from src.services.duckdb_optimizer import DuckDBOptimizer

optimizer = DuckDBOptimizer()

# Otimizar consulta
optimized_query = optimizer.optimize_query(
    original_query="SELECT * FROM payroll WHERE date > '2025-01-01'"
)

# Criar índices automáticos
optimizer.create_auto_indexes(table_name="payroll")
```

## 🧪 **PADRÕES DE DESENVOLVIMENTO**

### 🏗️ **Estrutura de Serviço**
```python
from abc import ABC, abstractmethod
from typing import Optional, List

class BaseService(ABC):
    """Classe base para todos os serviços"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.cache = CacheService()
    
    @abstractmethod
    def validate_input(self, data: dict) -> bool:
        """Valida dados de entrada"""
        pass
    
    def _setup_logger(self):
        """Configura logger do serviço"""
        pass

class PayrollService(BaseService):
    """Implementação específica para folha"""
    
    def validate_input(self, data: dict) -> bool:
        # Validação específica para folha
        return True
    
    def calculate_payroll(self, employee_id: int, period: str):
        # Implementação do cálculo
        pass
```

### 📊 **Tratamento de Erros**
```python
from src.core.exceptions import (
    ServiceError,
    ValidationError,
    ExternalAPIError
)

class PayrollService:
    def calculate_payroll(self, employee_id: int):
        try:
            # Validar entrada
            if not self.validate_employee(employee_id):
                raise ValidationError("Funcionário inválido")
            
            # Processar cálculo
            result = self._perform_calculation(employee_id)
            
            return result
            
        except ValidationError:
            raise  # Re-propagar erro de validação
        except Exception as e:
            self.logger.error(f"Erro no cálculo: {e}")
            raise ServiceError("Falha no cálculo da folha")
```

### 🔄 **Dependency Injection**
```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    # Configuração
    config = providers.Configuration()
    
    # Database
    database = providers.Singleton(Database, config.database.url)
    
    # Services
    auth_service = providers.Factory(
        AuthService,
        database=database
    )
    
    payroll_service = providers.Factory(
        PayrollService,
        database=database,
        auth_service=auth_service
    )
```

## 🧪 **TESTES DE SERVIÇOS**

### 📊 **Testes Unitários**
```python
import pytest
from unittest.mock import Mock, patch
from src.services.payroll_service import PayrollService

class TestPayrollService:
    @pytest.fixture
    def payroll_service(self):
        return PayrollService()
    
    def test_calculate_payroll_success(self, payroll_service):
        """Testa cálculo bem-sucedido"""
        result = payroll_service.calculate_payroll(
            employee_id=1,
            competency="2025-01"
        )
        
        assert result is not None
        assert result.total > 0
    
    @patch('src.services.payroll_service.external_api_call')
    def test_calculate_with_external_api(self, mock_api, payroll_service):
        """Testa integração com API externa"""
        mock_api.return_value = {"selic": 0.1075}
        
        result = payroll_service.calculate_with_taxes(1)
        
        assert mock_api.called
        assert result.taxes_calculated
```

### 🔄 **Testes de Integração**
```python
import pytest
from src.services.auth_service import AuthService
from src.services.payroll_service import PayrollService

class TestServicesIntegration:
    def test_auth_and_payroll_integration(self):
        """Testa integração entre serviços"""
        auth_service = AuthService()
        payroll_service = PayrollService()
        
        # Autenticar usuário
        token = auth_service.authenticate_user("test@test.com", "pass")
        
        # Usar token para acessar folha
        with auth_service.user_context(token):
            result = payroll_service.calculate_payroll(1, "2025-01")
        
        assert result is not None
```

## 📖 **DOCUMENTAÇÃO E APIS**

### 🔗 **Links Relacionados**
- **[🏗️ Arquitetura](../../docs/tecnico/arquitetura/visao-geral.md)** - Visão geral do sistema
- **[🔌 APIs](../../docs/tecnico/apis/api-documentation.md)** - Documentação de endpoints
- **[📊 Modelos](../models/README.md)** - Estrutura de dados
- **[🧪 Testes](../../docs/qualidade/estrategia-testes.md)** - Estratégia de testes

### 📚 **Boas Práticas**
1. **Single Responsibility**: Cada serviço tem uma responsabilidade clara
2. **Dependency Injection**: Use injeção de dependências
3. **Error Handling**: Trate erros de forma consistente
4. **Logging**: Registre operações importantes
5. **Testing**: Mantenha cobertura de testes alta
6. **Caching**: Cache operações custosas
7. **Documentation**: Documente APIs e métodos públicos

---

> **💡 Dica**: Mantenha os serviços desacoplados e testáveis. Use interfaces para facilitar mocking em testes.

**Última atualização**: Janeiro 2025 | **Status**: Documentação Atualizada
