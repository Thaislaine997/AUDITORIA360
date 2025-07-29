# 📊 AUDITORIA360 - Modelos de Dados

> **🗄️ Camada de dados** com modelos Pydantic e ORM para todo o sistema AUDITORIA360

Este módulo centraliza todos os modelos de dados do sistema, proporcionando validação automática, tipagem forte e estrutura consistente entre backend e frontend.

## 🏗️ **ARQUITETURA DOS MODELOS**

### 📋 **Estrutura Organizacional**
```
src/models/
├── 🔐 auth_models.py         # Autenticação e usuários
├── 💼 payroll_models.py      # Folha de pagamento
├── 📄 document_models.py     # Gestão de documentos
├── 📝 cct_models.py          # Convenções coletivas
├── 🔍 audit_models.py        # Sistema de auditoria
├── 🔔 notification_models.py # Notificações
├── 🤖 ai_models.py          # Modelos de IA/ML
└── 🗄️ database.py          # Configuração do banco
```

## 📊 **MODELOS PRINCIPAIS**

### 🔐 **Auth Models** - Autenticação
```python
# Principais entidades
- User: Usuários do sistema
- Token: Tokens JWT
- UserRole: Papéis de usuário
- Permission: Permissões granulares
```

**Exemplo de uso:**
```python
from src.models.auth_models import User, UserCreate

# Criar usuário
novo_usuario = UserCreate(
    nome="João Silva",
    email="joao@empresa.com",
    papel="rh_manager"
)
```

### 💼 **Payroll Models** - Folha de Pagamento
```python
# Principais entidades
- Employee: Funcionários
- PayrollCompetency: Competências de folha
- PayrollItem: Itens da folha
- PayrollCalculation: Cálculos automáticos
```

**Exemplo de uso:**
```python
from src.models.payroll_models import Employee, PayrollItem

# Criar funcionário
funcionario = Employee(
    nome="Maria Santos",
    cpf="123.456.789-00",
    cargo="Analista",
    salario_base=5000.00
)
```

### 📄 **Document Models** - Documentos
```python
# Principais entidades
- Document: Documentos do sistema
- DocumentVersion: Versionamento
- DocumentCategory: Categorias
- DocumentMetadata: Metadados
```

### 📝 **CCT Models** - Convenções Coletivas
```python
# Principais entidades
- CCT: Convenção coletiva
- Clause: Cláusulas específicas
- Sindicate: Sindicatos
- CCTComparison: Comparações entre CCTs
```

### 🔍 **Audit Models** - Auditoria
```python
# Principais entidades
- AuditExecution: Execuções de auditoria
- ComplianceRule: Regras de compliance
- AuditFinding: Achados de auditoria
- RiskAssessment: Avaliação de riscos
```

### 🔔 **Notification Models** - Notificações
```python
# Principais entidades
- Notification: Notificações
- NotificationTemplate: Templates
- NotificationChannel: Canais (email, SMS)
- NotificationHistory: Histórico
```

### 🤖 **AI Models** - Inteligência Artificial
```python
# Principais entidades
- ChatSession: Sessões de chat
- AIRecommendation: Recomendações
- KnowledgeBaseEntry: Base de conhecimento
- MLPrediction: Predições ML
```

## 🔧 **PADRÕES E VALIDAÇÕES**

### ✅ **Validações Automáticas**
```python
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class EmployeeBase(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    salario_base: float
    
    @validator('cpf')
    def validate_cpf(cls, v):
        # Validação personalizada de CPF
        return validate_cpf_format(v)
    
    @validator('salario_base')
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError('Salário deve ser positivo')
        return v
```

### 📊 **Tipos Personalizados**
```python
# Tipos customizados para o domínio
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    RH_MANAGER = "rh_manager"
    CONTADOR = "contador"
    COLABORADOR = "colaborador"
    SINDICATO = "sindicato"

class PayrollStatus(str, Enum):
    DRAFT = "rascunho"
    CALCULATED = "calculada"
    APPROVED = "aprovada"
    PAID = "paga"
```

### 🔗 **Relacionamentos**
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    
    # Relacionamento
    company = relationship("Company", back_populates="employees")
    payroll_items = relationship("PayrollItem", back_populates="employee")
```

## 📦 **CONFIGURAÇÃO DO BANCO**

### 🗄️ **Database Setup**
```python
# src/models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração para Neon PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://user:pass@host/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### 🔄 **Migrations**
```bash
# Criar migration
alembic revision --autogenerate -m "Add new models"

# Aplicar migrations
alembic upgrade head
```

## 🧪 **EXEMPLOS PRÁTICOS**

### 📝 **Criar e Validar Modelo**
```python
from src.models.payroll_models import PayrollItem
from decimal import Decimal

# Criar item de folha
item = PayrollItem(
    employee_id=1,
    competency="2025-01",
    description="Salário Base",
    value=Decimal("5000.00"),
    type="provento"
)

# Validação automática acontece na criação
print(f"Item válido: {item.dict()}")
```

### 🔍 **Consultas com ORM**
```python
from src.models.database import SessionLocal
from src.models.payroll_models import Employee

def get_employees_by_company(company_id: int):
    db = SessionLocal()
    try:
        employees = db.query(Employee)\
                     .filter(Employee.company_id == company_id)\
                     .all()
        return employees
    finally:
        db.close()
```

### 📊 **Serialização para API**
```python
from src.models.auth_models import User

def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "ativo": user.ativo,
        "created_at": user.created_at.isoformat()
    }
```

## 🔧 **UTILITÁRIOS E HELPERS**

### 🛠️ **Funções de Validação**
```python
# Validações comuns
def validate_cpf_format(cpf: str) -> str:
    """Valida formato do CPF"""
    # Implementação da validação
    pass

def validate_email_domain(email: str) -> str:
    """Valida domínio do email"""
    # Implementação da validação
    pass
```

### 📅 **Utilitários de Data**
```python
from datetime import datetime, timezone

def get_current_timestamp():
    """Retorna timestamp atual UTC"""
    return datetime.now(timezone.utc)

def format_competency(year: int, month: int) -> str:
    """Formata competência YYYY-MM"""
    return f"{year:04d}-{month:02d}"
```

## 🧪 **TESTES**

### 📊 **Testes de Modelo**
```python
import pytest
from src.models.payroll_models import Employee

def test_employee_creation():
    """Testa criação de funcionário"""
    employee = Employee(
        nome="Test User",
        cpf="123.456.789-00",
        email="test@example.com"
    )
    assert employee.nome == "Test User"
    assert employee.ativo is True  # valor padrão

def test_employee_validation():
    """Testa validação de funcionário"""
    with pytest.raises(ValueError):
        Employee(
            nome="",  # nome vazio deve falhar
            cpf="invalid",
            email="invalid-email"
        )
```

## 📖 **DOCUMENTAÇÃO ADICIONAL**

### 🔗 **Links Relacionados**
- **[🏗️ Arquitetura](../../docs/tecnico/arquitetura/visao-geral.md)** - Visão geral do sistema
- **[🔌 APIs](../../docs/tecnico/apis/api-documentation.md)** - Documentação de endpoints
- **[🗄️ Banco de Dados](../../docs/tecnico/banco-dados/)** - Schema e configuração
- **[🧪 Testes](../../docs/qualidade/estrategia-testes.md)** - Estratégia de testes

### 📚 **Boas Práticas**
1. **Tipagem**: Use type hints em todos os campos
2. **Validação**: Implemente validadores customizados quando necessário
3. **Documentação**: Documente campos e relacionamentos
4. **Consistência**: Mantenha padrões de nomenclatura
5. **Performance**: Use lazy loading para relacionamentos grandes

---

> **💡 Dica**: Para mudanças nos modelos, sempre crie migrations e execute testes completos antes do deploy.

**Última atualização**: Janeiro 2025 | **Status**: Documentação Atualizada
