# 🔌 AUDITORIA360 - API Endpoint Reference

> **📋 Comprehensive API Documentation** - Standardized endpoints with improved error handling and validation

## 🚀 **Recent Refactoring Improvements**

### ✅ **Completed Enhancements**
- **Standardized Response Format**: All endpoints now use consistent JSON response structure
- **Enhanced Error Handling**: Structured error responses with detailed error codes
- **Input Validation**: Comprehensive request validation using Pydantic models
- **Performance Monitoring**: Request/response time tracking and slow query detection
- **Consistent URL Patterns**: All endpoints follow `/api/v1/{module}` structure
- **Middleware Integration**: Centralized error handling and logging

### 🎯 **API Standards**

#### **Response Format**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}, 
  "timestamp": "2024-01-29T10:00:00Z",
  "request_id": "req_abc123"
}
```

#### **Error Format**
```json
{
  "success": false,
  "message": "Error description",
  "error_code": "VAL_001",
  "details": [
    {
      "field": "entity_type",
      "message": "Invalid entity type",
      "code": "INVALID_INPUT",
      "value": "invalid_type"
    }
  ],
  "timestamp": "2024-01-29T10:00:00Z",
  "request_id": "req_abc123",
  "trace_id": "trace_xyz789"
}
```

#### **Pagination Format**
```json
{
  "success": true,
  "message": "Items retrieved successfully",
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 📋 **API Modules Overview**

| Module | Prefix | Description | Status |
|--------|--------|-------------|--------|
| Authentication | `/api/v1/auth` | User authentication and authorization | ✅ Active |
| Payroll | `/api/v1/payroll` | Payroll management and calculations | ✅ Active |
| Documents | `/api/v1/documents` | Document upload and management | ✅ Active |
| CCT | `/api/v1/cct` | Collective Labor Agreements | ✅ Active |
| Notifications | `/api/v1/notifications` | Notification system | ✅ Active |
| Audit | `/api/v1/auditorias` | Audit and compliance monitoring | ✅ **Refactored** |
| Compliance | `/api/v1/compliance` | Compliance checking engine | ✅ **Refactored** |
| AI | `/api/v1/ai` | AI-powered features | ✅ Active |
| Automation | `/api/v1/automation` | Serverless automation tasks | ✅ **Refactored** |

---

## 🔍 **Detailed Endpoint Documentation**

### 🔐 **Authentication Module** (`/api/v1/auth`)

#### **POST /api/v1/auth/login**
Authenticate user and obtain access token.

**Request:**
```json
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Authentication successful",
  "data": {
    "access_token": "jwt_token_here",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "id": "user123",
      "name": "User Name",
      "role": "contador"
    }
  }
}
```

---

### 🏛️ **Audit Module** (`/api/v1/auditorias`) - **REFACTORED**

#### **POST /api/v1/auditorias/execute** 
Execute audit process with enhanced error handling.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Response:**
```json
{
  "success": true,
  "message": "Audit execution initiated successfully",
  "data": {
    "audit_id": "audit_20240129_140530",
    "status": "initiated",
    "started_at": "2024-01-29T14:05:30Z",
    "estimated_completion": "2024-01-29T14:35:30Z"
  },
  "request_id": "req_abc123"
}
```

#### **GET /api/v1/auditorias/executions**
List audit executions with standardized pagination.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20, max: 100)
- `search` (string): Search term
- `active_only` (boolean): Filter only running audits
- `sort_by` (string): Field to sort by
- `sort_order` (string): "asc" or "desc"

**Response:**
```json
{
  "success": true,
  "message": "Audit executions retrieved successfully",
  "data": [
    {
      "id": "audit_1",
      "status": "completed",
      "started_at": "2024-01-29T13:05:30Z",
      "completed_at": "2024-01-29T13:25:30Z",
      "user": "System",
      "summary": {
        "total_checks": 160,
        "passed": 148,
        "failed": 12,
        "warnings": 6
      }
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 24,
    "total_pages": 2,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### ✅ **Compliance Module** (`/api/v1/compliance`) - **REFACTORED**

#### **POST /api/v1/compliance/check**
Perform compliance check with enhanced validation.

**Request:**
```json
{
  "entity_type": "payroll",
  "entity_id": "payroll_001", 
  "rule_categories": ["salary", "tax"],
  "include_resolved": false
}
```

**Validation Rules:**
- `entity_type`: Must be one of "payroll", "employee", "cct"
- `entity_id`: Required, 1-50 characters
- `rule_categories`: Optional array of rule categories
- `include_resolved`: Boolean, default false

**Response:**
```json
{
  "success": true,
  "message": "Compliance check completed successfully",
  "data": {
    "entity": {
      "type": "payroll",
      "id": "payroll_001",
      "checked_at": "2024-01-29T14:05:30Z"
    },
    "compliance_status": "NON_COMPLIANT",
    "rules_checked": ["salary", "tax"],
    "summary": {
      "total_rules_applied": 15,
      "violations_found": 1,
      "warnings_found": 0,
      "critical_violations": 0,
      "resolved_violations": 0
    },
    "violations": [
      {
        "rule_id": "SALARY_001",
        "severity": "medium",
        "title": "Minimum salary check",
        "description": "Salary below minimum wage threshold",
        "recommendation": "Review salary calculation"
      }
    ],
    "performance": {
      "check_time_seconds": 0.245,
      "optimizations": [
        "Cached rule evaluations",
        "Optimized database queries",
        "Parallel rule checking"
      ]
    }
  }
}
```

#### **GET /api/v1/compliance/rules**
List available compliance rules with filtering.

**Query Parameters:**
- `category` (string): Filter by rule category
- `active_only` (boolean): Show only active rules (default: true)

**Response:**
```json
{
  "success": true,
  "message": "Compliance rules retrieved successfully",
  "data": {
    "rules": [
      {
        "id": "SALARY_001",
        "name": "Minimum Salary Check",
        "category": "salary",
        "severity": "high",
        "active": true,
        "description": "Validates minimum wage compliance"
      }
    ],
    "total": 4,
    "categories": ["salary", "tax", "union", "cct"]
  }
}
```

#### **POST /api/v1/compliance/rules/{rule_id}/execute**
Execute specific compliance rule against multiple entities.

**Path Parameters:**
- `rule_id` (string): ID of the rule to execute

**Request:**
```json
{
  "entity_type": "payroll",
  "entity_ids": ["payroll_001", "payroll_002", "payroll_003"]
}
```

**Validation Rules:**
- `entity_type`: Must be one of "payroll", "employee", "cct"
- `entity_ids`: Array of 1-100 entity IDs

**Response:**
```json
{
  "success": true,
  "message": "Compliance rule SALARY_001 executed successfully",
  "data": {
    "rule_id": "SALARY_001",
    "entity_type": "payroll",
    "total_checked": 3,
    "execution_time_seconds": 0.125,
    "results": [
      {
        "entity_id": "payroll_001",
        "rule_id": "SALARY_001", 
        "status": "PASSED",
        "checked_at": "2024-01-29T14:05:30Z",
        "details": "Rule SALARY_001 executed successfully for payroll payroll_001"
      }
    ],
    "summary": {
      "passed": 3,
      "failed": 0,
      "warnings": 0
    }
  }
}
```

---

### 🤖 **Automation Module** (`/api/v1/automation`) - **REFACTORED**

#### **POST /api/v1/automation/reports/daily**
Trigger daily report generation via Vercel Cron.

**Response:**
```json
{
  "success": true,
  "message": "Daily reports generation started",
  "data": {
    "status": "triggered",
    "type": "daily_reports",
    "timestamp": "2024-01-29T14:05:30Z"
  }
}
```

#### **GET /api/v1/automation/status**
Get status of all automation modules.

**Response:**
```json
{
  "success": true,
  "message": "Automation status retrieved successfully",
  "data": {
    "status": "operational",
    "modules": {
      "payroll_automation": true,
      "scheduled_reports": true,
      "backup_routine": true,
      "comunicados": true
    },
    "serverless_migration": {
      "percentage": 100,
      "status": "complete"
    },
    "environment": "production",
    "vercel_cron_configured": true,
    "github_actions_configured": true
  }
}
```

---

## 🔧 **Error Codes Reference**

| Code | Type | Description |
|------|------|-------------|
| `AUTH_001` | Authentication | Authentication failed |
| `AUTH_002` | Authorization | Authorization failed |
| `AUTH_003` | Authentication | Token expired |
| `AUTH_004` | Authentication | Invalid credentials |
| `VAL_001` | Validation | Invalid input |
| `VAL_002` | Validation | Missing required field |
| `VAL_003` | Validation | Invalid format |
| `VAL_004` | Validation | Invalid range |
| `BIZ_001` | Business | Resource not found |
| `BIZ_002` | Business | Resource conflict |
| `BIZ_003` | Business | Operation not allowed |
| `BIZ_004` | Business | Business rule violation |
| `SYS_001` | System | Internal server error |
| `SYS_002` | System | Service unavailable |
| `SYS_003` | System | Database error |
| `SYS_004` | System | External service error |
| `PROC_001` | Processing | File processing error |
| `PROC_002` | Processing | OCR processing error |
| `PROC_003` | Processing | Calculation error |
| `PROC_004` | Processing | Export error |

---

## 🎯 **Common Query Parameters**

### **Pagination**
- `page` (int): Page number (1-based, default: 1)
- `page_size` (int): Items per page (1-100, default: 20)

### **Filtering**
- `search` (string): Search term (min 2 characters)
- `active_only` (boolean): Filter only active records
- `start_date` (datetime): Start date filter (ISO format)
- `end_date` (datetime): End date filter (ISO format)

### **Sorting**
- `sort_by` (string): Field to sort by
- `sort_order` (string): "asc" or "desc" (default: "asc")

---

## 🔒 **Authentication**

All endpoints (except login) require Bearer token authentication:

```http
Authorization: Bearer {jwt_token}
```

### **Role-Based Access**
- `administrador`: Full access to all endpoints
- `contador`: Access to audit, compliance, and payroll endpoints
- `usuario`: Limited access to read-only endpoints

---

## 📊 **Performance Metrics**

### **Response Time Targets**
- Compliance checks: < 1 second
- List endpoints: < 500ms
- Authentication: < 200ms
- Health checks: < 100ms

### **Monitoring Headers**
- `X-Request-ID`: Unique request identifier
- `X-Process-Time`: Processing time in seconds

---

## 🧪 **Testing Endpoints**

### **Health Check**
```http
GET /health
```

### **System Status**
```http  
GET /api/v1/system/status
```

### **API Documentation**
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

---

## 📝 **Change Log**

### **v1.0.0 - January 2024**
- ✅ Implemented standardized response format
- ✅ Added comprehensive error handling
- ✅ Enhanced input validation with Pydantic
- ✅ Standardized URL patterns to `/api/v1/{module}`
- ✅ Added performance monitoring middleware
- ✅ Implemented pagination for list endpoints
- ✅ Added request/response logging
- ✅ Enhanced authentication and authorization

### **Refactored Modules**
- ✅ Audit Module: Enhanced with standardized responses and pagination
- ✅ Compliance Module: Added request validation and structured responses  
- ✅ Automation Module: Improved error handling and status reporting