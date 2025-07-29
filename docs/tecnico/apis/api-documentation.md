# 🔌 AUDITORIA360 - API Documentation

> **📋 Complete API Documentation** - Comprehensive guide to all endpoints with refactored backend

## 🚀 **API Refactoring Status**

### ✅ **Completed Improvements**
- **Standardized Error Handling**: Consistent error responses across all endpoints
- **Enhanced Input Validation**: Comprehensive Pydantic models for request validation  
- **Unified Response Format**: Standardized JSON response structure
- **Performance Monitoring**: Request/response time tracking and optimization
- **Consistent URL Patterns**: All endpoints follow `/api/v1/{module}` structure
- **Middleware Integration**: Centralized logging and error handling

### 📊 **Progress Summary**
- ✅ **Router Import Issues**: Fixed all None router issues
- ✅ **Error Handling**: Implemented standardized error middleware
- ✅ **Validation**: Added comprehensive input validation
- ✅ **Documentation**: Updated endpoint documentation
- ✅ **Response Format**: Standardized all response structures

---

## 📚 **Documentation Structure**

### 🔗 **Quick Links**
- **[📋 Endpoint Reference](endpoint-reference.md)** - Complete endpoint documentation
- **[🔧 Error Handling Guide](error-handling.md)** - Error codes and handling
- **[📊 Performance Guide](performance.md)** - Performance optimization tips
- **[🧪 Testing Guide](testing.md)** - API testing documentation

### 📋 **API Modules**

| Module | Status | Description | Documentation |
|--------|--------|-------------|---------------|
| **Authentication** | ✅ Active | User authentication and authorization | [Auth API](auth-api.md) |
| **Payroll** | ✅ Active | Payroll management and calculations | [Payroll API](payroll-api.md) |
| **Documents** | ✅ Active | Document upload and management | [Documents API](documents-api.md) |
| **CCT** | ✅ Active | Collective Labor Agreements | [CCT API](cct-api.md) |
| **Notifications** | ✅ Active | Notification system | [Notifications API](notifications-api.md) |
| **Audit** | ✅ **Refactored** | Audit and compliance monitoring | [Audit API](audit-api.md) |
| **Compliance** | ✅ **Refactored** | Compliance checking engine | [Compliance API](compliance-api.md) |
| **AI** | ✅ Active | AI-powered features | [AI API](ai-api.md) |
| **Automation** | ✅ **Refactored** | Serverless automation tasks | [Automation API](automation-api.md) |

---
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