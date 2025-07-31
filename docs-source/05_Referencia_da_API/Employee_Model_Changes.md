# API Changes - Era Kairós Employee Model Simplification

## Overview
As part of the Genesis Final PR and Era Kairós implementation, the Employee model has been simplified to focus on the 7 essential fields required for payroll processing and compliance.

## Employee Model Changes

### Before (Legacy Model)
The previous Employee model contained 20+ fields including:
- Personal information (birth_date, gender, marital_status, email, phone)
- Address fields (address, city, state, zip_code)
- Employment details (department, work_schedule, termination_date)
- LGPD compliance fields (consent_given, consent_date)
- PIS/PASEP information

### After (Era Kairós - Simplified Model)
The new Employee model contains only 7 essential fields:

```python
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 7 essential fields
    nome = Column(String(255), nullable=False)              # Employee full name
    codigo = Column(String(50), unique=True, nullable=False) # Employee ID/code
    admissao = Column(DateTime, nullable=False)             # Hire date
    salario = Column(Float, nullable=False)                 # Current salary
    dependentes = Column(Integer, default=0)                # Number of dependents
    cpf = Column(String(14), unique=True, nullable=False)   # Brazilian tax ID
    cargo = Column(String(100), nullable=False)             # Job position
    cbo = Column(String(10))                                # Brazilian Occupation Classification
    
    # Essential audit fields
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
```

## API Endpoint Changes

### Employee Creation/Update Endpoints

**POST /api/v1/employees**
**PUT /api/v1/employees/{id}**

#### New Request Body Schema:
```json
{
  "nome": "João da Silva",
  "codigo": "EMP001",
  "admissao": "2024-01-15T00:00:00Z",
  "salario": 5000.00,
  "dependentes": 2,
  "cpf": "123.456.789-00",
  "cargo": "Analista de Sistemas",
  "cbo": "2124-05"
}
```

#### Response Schema:
```json
{
  "id": 1,
  "nome": "João da Silva",
  "codigo": "EMP001",
  "admissao": "2024-01-15T00:00:00Z",
  "salario": 5000.00,
  "dependentes": 2,
  "cpf": "123.456.789-00",
  "cargo": "Analista de Sistemas",
  "cbo": "2124-05",
  "is_active": true,
  "created_at": "2025-07-31T19:15:00Z",
  "updated_at": "2025-07-31T19:15:00Z"
}
```

### Breaking Changes

#### Removed Fields
The following fields are no longer available and will return 400 Bad Request if included in requests:

- `birth_date`
- `gender` 
- `marital_status`
- `email`
- `phone`
- `address`
- `city`
- `state`
- `zip_code`
- `department`
- `work_schedule`
- `termination_date`
- `pis_pasep`
- `consent_given`
- `consent_date`

#### Field Mappings
For clients upgrading from the legacy model:

| Legacy Field | New Field | Notes |
|-------------|-----------|--------|
| `full_name` | `nome` | Direct mapping |
| `employee_id` | `codigo` | Direct mapping |
| `hire_date` | `admissao` | Direct mapping |
| `salary` | `salario` | Direct mapping |
| `cpf` | `cpf` | Direct mapping |
| `position` | `cargo` | Direct mapping |
| N/A | `dependentes` | New field, defaults to 0 |
| N/A | `cbo` | New field, optional |

## Migration Strategy

### Database Migration
1. The migration script `002_simplify_employee_model.sql` handles the data transformation
2. Essential data is preserved and mapped to the new schema
3. Non-essential data is archived in a backup table

### Client Migration
1. **Immediate**: Update API calls to use new field names
2. **Remove**: Remove references to deprecated fields
3. **Validate**: Ensure all required fields are provided in requests

### Backward Compatibility
- **Breaking Change**: This is a breaking change requiring client updates
- **No Legacy Support**: Legacy field names are not supported
- **Migration Period**: Clients should update immediately after deployment

## Validation Rules

### Required Fields
- `nome`: Must be non-empty string, max 255 characters
- `codigo`: Must be unique, non-empty string, max 50 characters  
- `admissao`: Must be valid ISO 8601 datetime
- `salario`: Must be positive decimal value
- `cpf`: Must be valid Brazilian CPF format (XXX.XXX.XXX-XX)
- `cargo`: Must be non-empty string, max 100 characters

### Optional Fields
- `dependentes`: Integer, defaults to 0, must be >= 0
- `cbo`: String, max 10 characters, follows Brazilian CBO format

## Benefits of Simplification

1. **Performance**: Reduced database storage and faster queries
2. **Simplicity**: Easier to understand and maintain
3. **Focus**: Aligned with core payroll processing needs
4. **Compliance**: Maintains essential fields for Brazilian labor law
5. **API Efficiency**: Smaller request/response payloads

## Support

For questions about the migration or API changes:
- Technical Documentation: [API Reference](../05_Referencia_da_API/README.md)
- Support: suporte@auditoria360.com
- Issues: [GitHub Issues](https://github.com/Thaislaine997/AUDITORIA360/issues)