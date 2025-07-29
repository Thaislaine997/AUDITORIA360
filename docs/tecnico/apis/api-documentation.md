# 🔌 AUDITORIA360 - Documentação Completa da API

> **🚀 API REST serverless** com FastAPI para o sistema AUDITORIA360

Esta documentação apresenta todos os endpoints disponíveis na API do AUDITORIA360, incluindo autenticação, gestão de folha, documentos, auditoria e funcionalidades de IA.

## 🏗️ **ARQUITETURA DA API**

### 📋 **Estrutura Geral**
```
api/
├── 🔐 /auth           # Autenticação e autorização
├── 💼 /payroll        # Gestão de folha de pagamento
├── 📄 /documents      # Gestão de documentos
├── 📝 /cct           # Convenções coletivas de trabalho
├── 🔍 /audit         # Sistema de auditoria
├── 🔔 /notifications # Sistema de notificações  
├── 🤖 /ai            # Integrações de IA
├── ⚙️ /automation    # Automação e workflows
└── ✅ /compliance    # Compliance e conformidade
```

### 🌐 **Base URL**
- **Desenvolvimento**: `http://localhost:8000/api/v1`
- **Produção**: `https://auditoria360.vercel.app/api/v1`

### 📊 **Formato de Resposta**
```json
{
  "success": true,
  "data": {...},
  "message": "Operação realizada com sucesso",
  "timestamp": "2025-01-29T12:00:00Z",
  "request_id": "req_12345"
}
```

## 🔐 **AUTENTICAÇÃO** `/auth`

### 🚀 **Login de Usuário**
**POST** `/auth/login`

```json
// Request
{
  "email": "user@empresa.com",
  "password": "senha123"
}

// Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "user@empresa.com",
    "name": "João Silva",
    "role": "rh_manager",
    "permissions": ["payroll:read", "payroll:write"]
  }
}
```

### 👤 **Perfil do Usuário**
**GET** `/auth/me`

*Headers:* `Authorization: Bearer {token}`

```json
// Response
{
  "id": 1,
  "email": "user@empresa.com",
  "name": "João Silva",
  "role": "rh_manager",
  "company_id": 1,
  "permissions": ["payroll:read", "payroll:write"],
  "last_login": "2025-01-29T11:30:00Z"
}
```

### 🔄 **Renovar Token**
**POST** `/auth/refresh`

```json
// Request
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

// Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

### 👥 **Criar Usuário** (Admin)
**POST** `/auth/users`

```json
// Request
{
  "email": "novo@empresa.com",
  "name": "Maria Santos",
  "password": "senha123",
  "role": "contador",
  "company_id": 1
}

// Response
{
  "id": 2,
  "email": "novo@empresa.com",
  "name": "Maria Santos",
  "role": "contador",
  "active": true,
  "created_at": "2025-01-29T12:00:00Z"
}
```

## 💼 **FOLHA DE PAGAMENTO** `/payroll`

### 👨‍💼 **Gestão de Funcionários**

#### **GET** `/payroll/employees`
Lista todos os funcionários da empresa

*Query Parameters:*
- `page` (int): Página (default: 1)
- `limit` (int): Itens por página (default: 20)
- `search` (str): Busca por nome/CPF
- `active` (bool): Apenas ativos

```json
// Response
{
  "data": [
    {
      "id": 1,
      "name": "João Silva",
      "cpf": "123.456.789-00",
      "position": "Analista",
      "department": "TI",
      "hire_date": "2024-01-15",
      "salary": 5000.00,
      "active": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

#### **POST** `/payroll/employees`
Cria novo funcionário

```json
// Request
{
  "name": "Maria Santos",
  "cpf": "987.654.321-00",
  "email": "maria@empresa.com",
  "position": "Contadora",
  "department": "Financeiro",
  "hire_date": "2025-02-01",
  "salary": 6000.00,
  "dependents": 2
}

// Response
{
  "id": 2,
  "name": "Maria Santos",
  "cpf": "987.654.321-00",
  "employee_code": "EMP-0002",
  "active": true,
  "created_at": "2025-01-29T12:00:00Z"
}
```

### 📊 **Competências e Cálculos**

#### **GET** `/payroll/competencies`
Lista competências de folha

```json
// Response
{
  "data": [
    {
      "id": "2025-01",
      "year": 2025,
      "month": 1,
      "status": "calculated",
      "employees_count": 150,
      "total_gross": 750000.00,
      "total_deductions": 180000.00,
      "total_net": 570000.00,
      "calculated_at": "2025-01-31T18:00:00Z"
    }
  ]
}
```

#### **POST** `/payroll/calculate`
Calcula folha de pagamento

```json
// Request
{
  "competency": "2025-02",
  "employee_ids": [1, 2, 3], // opcional - todos se não informado
  "recalculate": false
}

// Response
{
  "competency": "2025-02",
  "calculation_id": "calc_12345",
  "status": "processing",
  "estimated_completion": "2025-02-01T12:30:00Z",
  "employees_processed": 0,
  "total_employees": 150
}
```

#### **GET** `/payroll/payslip/{employee_id}/{competency}`
Obtém holerite do funcionário

```json
// Response
{
  "employee": {
    "id": 1,
    "name": "João Silva",
    "position": "Analista"
  },
  "competency": "2025-01",
  "earnings": [
    {
      "code": "001",
      "description": "Salário Base",
      "value": 5000.00
    },
    {
      "code": "002", 
      "description": "Horas Extras",
      "value": 300.00
    }
  ],
  "deductions": [
    {
      "code": "101",
      "description": "INSS",
      "value": 424.00
    },
    {
      "code": "102",
      "description": "IRRF",
      "value": 200.00
    }
  ],
  "net_salary": 4676.00
}
```

## 📄 **DOCUMENTOS** `/documents`

### 📁 **Upload e Gestão**

#### **POST** `/documents/upload`
Upload de documento

*Content-Type:* `multipart/form-data`

```
// Form Data
file: document.pdf
category: contracts
description: Contrato de trabalho - João Silva
metadata: {"employee_id": 1, "type": "contract"}
```

```json
// Response
{
  "id": "doc_12345",
  "filename": "document.pdf",
  "size": 2048576,
  "mimetype": "application/pdf",
  "category": "contracts",
  "status": "uploaded",
  "url": "/api/v1/documents/doc_12345/download",
  "ocr_status": "processing"
}
```

#### **GET** `/documents/`
Lista documentos

*Query Parameters:*
- `category` (str): Filtrar por categoria
- `search` (str): Busca por nome/conteúdo
- `date_from/date_to` (str): Filtro por data

```json
// Response
{
  "data": [
    {
      "id": "doc_12345",
      "filename": "contract_joao.pdf",
      "category": "contracts",
      "size": 2048576,
      "uploaded_at": "2025-01-29T10:00:00Z",
      "ocr_completed": true,
      "preview_url": "/api/v1/documents/doc_12345/preview"
    }
  ]
}
```

#### **GET** `/documents/{document_id}`
Detalhes do documento

```json
// Response
{
  "id": "doc_12345",
  "filename": "contract_joao.pdf",
  "original_name": "Contrato João Silva.pdf",
  "size": 2048576,
  "mimetype": "application/pdf",
  "category": "contracts",
  "description": "Contrato de trabalho - João Silva",
  "metadata": {"employee_id": 1, "type": "contract"},
  "versions": [
    {
      "version": 1,
      "uploaded_at": "2025-01-29T10:00:00Z",
      "uploaded_by": "admin@empresa.com"
    }
  ],
  "ocr_result": {
    "text_extracted": "CONTRATO DE TRABALHO...",
    "confidence": 0.95,
    "processed_at": "2025-01-29T10:05:00Z"
  }
}
```

### 🔍 **Busca e OCR**

#### **POST** `/documents/search`
Busca avançada em documentos

```json
// Request
{
  "query": "contrato trabalho",
  "filters": {
    "category": ["contracts", "policies"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2025-01-31"
    },
    "employee_id": 1
  },
  "sort": "relevance", // relevance, date, name
  "limit": 20
}

// Response
{
  "results": [
    {
      "document_id": "doc_12345",
      "filename": "contract_joao.pdf",
      "relevance_score": 0.95,
      "highlights": [
        "...CONTRATO DE <em>TRABALHO</em>...",
        "...regime de <em>trabalho</em> CLT..."
      ]
    }
  ],
  "total_results": 5,
  "query_time": 0.15
}
```

## 📝 **CONVENÇÕES COLETIVAS** `/cct`

### 📋 **Gestão de CCTs**

#### **GET** `/cct/`
Lista CCTs

```json
// Response
{
  "data": [
    {
      "id": 1,
      "title": "CCT 2025 - Metalúrgicos SP",
      "sindicate": "Sindicato dos Metalúrgicos",
      "validity_start": "2025-01-01",
      "validity_end": "2025-12-31",
      "status": "active",
      "clauses_count": 45,
      "last_updated": "2025-01-15T09:00:00Z"
    }
  ]
}
```

#### **POST** `/cct/`
Criar nova CCT

```json
// Request
{
  "title": "CCT 2025 - TI São Paulo",
  "sindicate_id": 1,
  "document_id": "doc_67890",
  "validity_start": "2025-01-01",
  "validity_end": "2025-12-31",
  "auto_extract_clauses": true
}

// Response
{
  "id": 2,
  "title": "CCT 2025 - TI São Paulo",
  "status": "processing",
  "extraction_status": "started",
  "estimated_completion": "2025-01-29T12:30:00Z"
}
```

#### **GET** `/cct/{cct_id}/clauses`
Lista cláusulas da CCT

```json
// Response
{
  "cct_id": 1,
  "clauses": [
    {
      "id": 1,
      "number": "1.1",
      "title": "Salário Base",
      "content": "O salário base não poderá ser inferior a R$ 2.500,00",
      "category": "remuneracao",
      "mandatory": true,
      "extracted_data": {
        "values": ["2500.00"],
        "dates": [],
        "percentages": []
      }
    }
  ]
}
```

#### **POST** `/cct/{cct_id}/compare/{other_cct_id}`
Compara duas CCTs

```json
// Response
{
  "comparison_id": "comp_12345",
  "cct_a": {"id": 1, "title": "CCT 2024"},
  "cct_b": {"id": 2, "title": "CCT 2025"},
  "differences": [
    {
      "clause_number": "1.1",
      "type": "modified",
      "old_value": "R$ 2.400,00",
      "new_value": "R$ 2.500,00",
      "impact": "positive"
    }
  ],
  "summary": {
    "total_clauses_a": 40,
    "total_clauses_b": 45,
    "added": 8,
    "removed": 3,
    "modified": 12,
    "unchanged": 25
  }
}
```

## 🔍 **AUDITORIA** `/audit`

### 🔎 **Execuções de Auditoria**

#### **POST** `/audit/execute`
Executar auditoria

```json
// Request
{
  "type": "payroll_compliance",
  "scope": {
    "company_id": 1,
    "period": "2025-01",
    "departments": ["RH", "Financeiro"],
    "employee_ids": [] // vazio = todos
  },
  "rules": ["FGTS", "INSS", "IRRF", "CLT_compliance"],
  "schedule": {
    "immediate": true,
    "scheduled_for": null
  }
}

// Response
{
  "execution_id": "audit_12345",
  "status": "started",
  "estimated_duration": "00:15:00",
  "progress_url": "/api/v1/audit/executions/audit_12345/progress"
}
```

#### **GET** `/audit/executions/{execution_id}`
Status da execução

```json
// Response
{
  "execution_id": "audit_12345",
  "status": "completed",
  "started_at": "2025-01-29T14:00:00Z",
  "completed_at": "2025-01-29T14:12:30Z",
  "progress": {
    "total_checks": 1500,
    "completed_checks": 1500,
    "percentage": 100
  },
  "results": {
    "total_findings": 25,
    "critical": 3,
    "high": 8,
    "medium": 10,
    "low": 4,
    "passed_checks": 1475
  },
  "report_url": "/api/v1/audit/executions/audit_12345/report"
}
```

### 📊 **Findings e Relatórios**

#### **GET** `/audit/findings`
Lista achados de auditoria

*Query Parameters:*
- `execution_id` (str): Filtrar por execução
- `severity` (str): critical, high, medium, low
- `status` (str): open, resolved, false_positive

```json
// Response
{
  "data": [
    {
      "id": "finding_001",
      "execution_id": "audit_12345",
      "rule_id": "FGTS_001",
      "severity": "high",
      "title": "FGTS não calculado corretamente",
      "description": "Funcionário João Silva - FGTS calculado como R$ 320,00, deveria ser R$ 400,00",
      "affected_records": 1,
      "recommendation": "Recalcular FGTS para competência 2025-01",
      "status": "open",
      "found_at": "2025-01-29T14:05:00Z"
    }
  ]
}
```

## 🔔 **NOTIFICAÇÕES** `/notifications`

### 📱 **Gestão de Notificações**

#### **GET** `/notifications/`
Lista notificações do usuário

```json
// Response
{
  "data": [
    {
      "id": "notif_001",
      "type": "audit_complete",
      "title": "Auditoria Concluída",
      "message": "Auditoria de folha janeiro/2025 foi finalizada com 25 achados",
      "priority": "normal",
      "read": false,
      "created_at": "2025-01-29T14:15:00Z",
      "action_url": "/audit/executions/audit_12345"
    }
  ],
  "unread_count": 5
}
```

#### **POST** `/notifications/send`
Enviar notificação

```json
// Request
{
  "recipients": ["user@empresa.com"],
  "type": "custom",
  "title": "Título da Notificação",
  "message": "Conteúdo da mensagem",
  "channels": ["email", "push"],
  "priority": "normal",
  "data": {"custom_field": "value"}
}

// Response
{
  "notification_id": "notif_002",
  "status": "sent",
  "recipients_count": 1,
  "sent_at": "2025-01-29T15:00:00Z"
}
```

## 🤖 **INTELIGÊNCIA ARTIFICIAL** `/ai`

### 💬 **Chatbot**

#### **POST** `/ai/chat`
Interação com chatbot

```json
// Request
{
  "message": "Como calcular FGTS para funcionário admitido no meio do mês?",
  "context": {
    "user_role": "rh_manager",
    "current_competency": "2025-02"
  },
  "session_id": "chat_session_123"
}

// Response
{
  "response": "Para funcionários admitidos no meio do mês, o FGTS deve ser calculado proporcional aos dias trabalhados...",
  "confidence": 0.95,
  "sources": [
    "Lei 8.036/90 - FGTS",
    "CCT Metalúrgicos SP 2025"
  ],
  "session_id": "chat_session_123",
  "suggestions": [
    "Como calcular férias proporcionais?",
    "Quais documentos são necessários para admissão?"
  ]
}
```

### 🎯 **Recomendações**

#### **GET** `/ai/recommendations`
Obter recomendações personalizadas

```json
// Response
{
  "recommendations": [
    {
      "id": "rec_001",
      "type": "payroll_optimization",
      "title": "Otimização de Cálculo de INSS",
      "description": "Identificamos uma oportunidade de otimizar o cálculo...",
      "priority": "medium",
      "estimated_savings": "R$ 2.500,00/mês",
      "implementation_effort": "low"
    }
  ]
}
```

### 🔍 **Análise de Documentos**

#### **POST** `/ai/analyze-document`
Análise de documento com IA

```json
// Request
{
  "document_id": "doc_12345",
  "analysis_type": "contract_review",
  "focus_areas": ["salary", "benefits", "working_hours"]
}

// Response
{
  "analysis_id": "analysis_001",
  "document_id": "doc_12345",
  "analysis_type": "contract_review",
  "results": {
    "extracted_data": {
      "salary": "R$ 5.000,00",
      "benefits": ["Vale refeição", "Plano de saúde"],
      "working_hours": "44h semanais"
    },
    "compliance_check": {
      "clt_compliant": true,
      "issues_found": [],
      "score": 0.98
    },
    "recommendations": [
      "Incluir cláusula sobre banco de horas",
      "Especificar valor do vale refeição"
    ]
  },
  "confidence": 0.92,
  "processed_at": "2025-01-29T15:30:00Z"
}
```

## ⚙️ **AUTOMAÇÃO** `/automation`

### 🔄 **Workflows**

#### **GET** `/automation/workflows`
Lista workflows disponíveis

```json
// Response
{
  "data": [
    {
      "id": "workflow_001",
      "name": "Processamento Mensal de Folha",
      "description": "Automatiza todo o processo de cálculo mensal",
      "triggers": ["monthly_schedule", "manual"],
      "steps": [
        "Validar dados funcionários",
        "Calcular folha",
        "Gerar holerites",
        "Enviar notificações"
      ],
      "status": "active",
      "last_execution": "2025-01-31T18:00:00Z"
    }
  ]
}
```

#### **POST** `/automation/workflows/{workflow_id}/execute`
Executar workflow

```json
// Request
{
  "parameters": {
    "competency": "2025-02",
    "notify_users": true,
    "auto_approve": false
  }
}

// Response
{
  "execution_id": "exec_001",
  "workflow_id": "workflow_001",
  "status": "started",
  "estimated_completion": "2025-02-01T19:00:00Z"
}
```

## ✅ **COMPLIANCE** `/compliance`

### 📋 **Regras e Verificações**

#### **GET** `/compliance/rules`
Lista regras de compliance

```json
// Response
{
  "data": [
    {
      "id": "rule_fgts_001",
      "name": "FGTS - Cálculo Correto",
      "description": "Verifica se FGTS está sendo calculado corretamente (8%)",
      "category": "payroll",
      "severity": "high",
      "active": true,
      "last_updated": "2024-12-15T10:00:00Z"
    }
  ]
}
```

#### **POST** `/compliance/check`
Verificar compliance

```json
// Request
{
  "scope": {
    "company_id": 1,
    "period": "2025-01",
    "rules": ["rule_fgts_001", "rule_inss_001"]
  }
}

// Response
{
  "check_id": "check_001",
  "status": "completed",
  "results": {
    "total_rules": 2,
    "passed": 1,
    "failed": 1,
    "details": [
      {
        "rule_id": "rule_fgts_001",
        "status": "passed",
        "checked_records": 150,
        "violations": 0
      },
      {
        "rule_id": "rule_inss_001", 
        "status": "failed",
        "checked_records": 150,
        "violations": 5
      }
    ]
  }
}
```

## 🛡️ **SEGURANÇA E AUTENTICAÇÃO**

### 🔐 **Headers Obrigatórios**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
X-Request-ID: {unique_request_id}
```

### 🔑 **Códigos de Status HTTP**
- **200** - Sucesso
- **201** - Criado com sucesso
- **400** - Erro na requisição (dados inválidos)
- **401** - Não autenticado
- **403** - Não autorizado (sem permissão)
- **404** - Recurso não encontrado
- **409** - Conflito (recurso já existe)
- **422** - Erro de validação
- **429** - Rate limit excedido
- **500** - Erro interno do servidor

### 🚨 **Tratamento de Erros**
```json
// Exemplo de resposta de erro
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados de entrada inválidos",
    "details": {
      "email": ["Email é obrigatório"],
      "cpf": ["CPF inválido"]
    }
  },
  "timestamp": "2025-01-29T15:00:00Z",
  "request_id": "req_12345"
}
```

## 🧪 **TESTES E DOCUMENTAÇÃO**

### 📊 **Swagger/OpenAPI**
- **Documentação interativa**: `/docs`
- **Schema OpenAPI**: `/openapi.json`
- **ReDoc**: `/redoc`

### 🔧 **Exemplos de Integração**

#### Python
```python
import requests

# Autenticação
auth_response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={"email": "user@empresa.com", "password": "senha123"}
)
token = auth_response.json()["access_token"]

# Usar API autenticada
headers = {"Authorization": f"Bearer {token}"}
employees = requests.get(
    "http://localhost:8000/api/v1/payroll/employees",
    headers=headers
)
```

#### JavaScript
```javascript
// Autenticação
const authResponse = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@empresa.com',
    password: 'senha123'
  })
});
const { access_token } = await authResponse.json();

// Usar API autenticada
const employees = await fetch('/api/v1/payroll/employees', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
```

## 📖 **LINKS RELACIONADOS**

### 🔗 **Documentação Adicional**
- **[🏗️ Arquitetura](../arquitetura/visao-geral.md)** - Visão geral do sistema
- **[📊 Modelos](../../models/README.md)** - Estrutura de dados
- **[🔧 Serviços](../../services/README.md)** - Lógica de negócio
- **[🚀 Deploy](../deploy/deploy-checklist.md)** - Guia de implantação

### 📚 **Recursos Externos**
- **[FastAPI Docs](https://fastapi.tiangolo.com/)** - Framework da API
- **[JWT.io](https://jwt.io/)** - Validador de tokens JWT
- **[Postman Collection](./postman_collection.json)** - Coleção para testes

---

> **💡 Dica**: Use sempre os headers de autenticação e trate adequadamente os códigos de erro. Para desenvolvimento, acesse `/docs` para interface interativa.

**Última atualização**: Janeiro 2025 | **Versão**: v1.0 | **Status**: Documentação Atualizada
  "status": "completed",
  "metrics": {
    "total_audits": 150,
    "completed_audits": 135,
    "compliance_score": 94.2
  }
}
```

### 📈 Consulta de Relatórios

#### GET `/api/v1/reports`
Lista relatórios disponíveis com paginação e filtros.

**Query Parameters**:
- `type`: Tipo de relatório
- `status`: Status do relatório
- `date_from`: Data inicial
- `date_to`: Data final
- `page`: Página (padrão: 1)
- `limit`: Itens por página (padrão: 20)

**Response**:
```json
{
  "data": [
    {
      "id": "daily_20250128_20250129",
      "type": "daily",
      "title": "Relatório Daily - AUDITORIA360",
      "generated_at": "2025-01-29T10:00:00Z",
      "status": "completed"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

### 📊 Dados de Gráficos

#### GET `/api/v1/reports/{report_id}/charts`
Obtém dados de gráficos para um relatório específico.

**Response**:
```json
{
  "audit_trends": {
    "config": {
      "type": "line",
      "title": "Tendência de Auditorias"
    },
    "data": {
      "labels": ["Semana 1", "Semana 2", "Semana 3"],
      "datasets": [
        {
          "label": "Auditorias Concluídas",
          "data": [32, 41, 35]
        }
      ]
    }
  },
  "compliance_score": {
    "config": {
      "type": "gauge",
      "title": "Score de Conformidade"
    },
    "data": {
      "value": 94.2,
      "color": "#2ca02c"
    }
  }
}
```

### 📥 Download de Relatórios

#### GET `/api/v1/reports/{report_id}/download`
Faz download do relatório no formato especificado.

**Query Parameters**:
- `format`: Formato desejado (json, html, pdf, csv, excel)

**Response**: Arquivo binário ou JSON dependendo do formato

### 🔄 Agendamento Automático

#### POST `/api/v1/reports/schedule`
Agenda geração automática de relatórios.

**Request Body**:
```json
{
  "name": "Relatório Semanal RH",
  "type": "weekly",
  "schedule": "0 8 * * 1",
  "recipients": ["admin@empresa.com"],
  "format": "pdf",
  "filters": {
    "department": ["RH"]
  }
}
```

#### GET `/api/v1/reports/schedules`
Lista agendamentos ativos.

## 🔧 Integração com Dashboard

### WebSocket para Updates em Tempo Real
```javascript
const ws = new WebSocket('wss://api.auditoria360.com/v1/reports/ws');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  if (update.type === 'report_completed') {
    // Atualizar interface com novo relatório
    refreshReportsList();
  }
};
```

### JavaScript SDK
```javascript
import { ReportsAPI } from '@auditoria360/sdk';

const api = new ReportsAPI({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.auditoria360.com'
});

// Gerar relatório
const report = await api.generateReport({
  type: 'monthly',
  includeCharts: true,
  format: 'json'
});

// Obter dados de gráficos
const charts = await api.getReportCharts(report.id);
```

## 📊 Estrutura de Dados

### ReportData
```typescript
interface ReportData {
  id: string;
  type: ReportType;
  title: string;
  generated_at: string;
  period_start: string;
  period_end: string;
  metrics: ReportMetrics;
  details: Record<string, any>;
  charts_data: Record<string, ChartData>;
  recommendations: Recommendation[];
  status: string;
}
```

### ReportMetrics
```typescript
interface ReportMetrics {
  total_audits: number;
  completed_audits: number;
  pending_audits: number;
  compliance_score: number;
  critical_issues: number;
  resolved_issues: number;
  performance_score: number;
  risk_score: number;
}
```

### ChartData
```typescript
interface ChartData {
  config: ChartConfig;
  data: Record<string, any>;
}

interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'gauge' | 'heatmap';
  title: string;
  x_axis?: string;
  y_axis?: string;
  color_scheme?: string[];
}
```

## 🔐 Autenticação

Todos os endpoints requerem autenticação via JWT token:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://api.auditoria360.com/v1/reports
```

## 📈 Rate Limiting

- **Usuários padrão**: 100 requests/minuto
- **Usuários premium**: 1000 requests/minuto
- **Geração de relatórios**: 10 requests/minuto

## 🔧 Códigos de Status

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Relatório criado |
| 202 | Processamento em andamento |
| 400 | Parâmetros inválidos |
| 401 | Não autorizado |
| 403 | Sem permissão |
| 404 | Relatório não encontrado |
| 429 | Rate limit excedido |
| 500 | Erro interno |

## 📝 Exemplos de Uso

### Gerar Relatório Mensal Completo
```bash
curl -X POST https://api.auditoria360.com/v1/reports/generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "monthly",
    "period_start": "2025-01-01T00:00:00Z",
    "period_end": "2025-01-31T23:59:59Z",
    "include_charts": true,
    "format": "json"
  }'
```

### Consultar Relatórios por Período
```bash
curl "https://api.auditoria360.com/v1/reports?date_from=2025-01-01&date_to=2025-01-31&type=monthly" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Obter Dados de Gráficos
```bash
curl https://api.auditoria360.com/v1/reports/monthly_20250101_20250131/charts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

> 📖 **Documentação Relacionada:**
> - [Exemplos de Uso](exemplos.md)
> - [Sistema de Relatórios](../relatorios/relatorio-unificado.md)
> - [Dashboard](../../dashboards/enhanced_dashboard.py)