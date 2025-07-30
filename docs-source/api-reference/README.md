# 📡 API Reference

> **Complete technical reference for AUDITORIA360 APIs**

---

## 🎯 **Quick Start**

```bash
# Base URL
export API_BASE="https://api.auditoria360.com"

# Authentication
curl -X POST "$API_BASE/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"

# Use API
export TOKEN="your_access_token_here"
curl -H "Authorization: Bearer $TOKEN" \
  "$API_BASE/api/v1/audits"
```

---

## 📚 **API Categories**

### **🔐 [Authentication](./authentication)**
OAuth2 flow, JWT tokens, and authorization

### **🔍 [Audits](./endpoints/audits)**
Core audit functionality and management

### **👥 [Users & Organizations](./endpoints/users)**
User management and organization settings

### **📄 [Documents](./endpoints/documents)**
Document upload, processing, and OCR

### **📊 [Reports](./endpoints/reports)**
Generated reports and analytics

### **📋 [CCT Management](./endpoints/cct)**
Collective bargaining agreements

### **🔔 [Webhooks](./endpoints/webhooks)**
Real-time event notifications

---

## 🔧 **Technical Specifications**

### **📋 General Information**
```yaml
Protocol: "HTTPS only"
Format: "JSON (application/json)"
Charset: "UTF-8"
Authentication: "OAuth2 + JWT Bearer tokens"
Rate_Limiting: "1000 requests/hour (standard)"
API_Version: "v1 (current)"
```

### **📊 Response Format**
```json
{
  "data": {...},           // Response payload
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_abc123",
    "version": "v1"
  },
  "pagination": {          // For paginated responses
    "total": 100,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

### **⚠️ Error Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid parameters provided",
    "details": [
      {
        "field": "client_id",
        "message": "This field is required",
        "code": "REQUIRED"
      }
    ],
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## 🚀 **Getting Started**

### **1. Register Application**
Contact support to register your application and receive:
- `client_id`: Your application identifier
- `client_secret`: Your application secret
- Scopes: Permissions for your application

### **2. Obtain Access Token**
```bash
curl -X POST "https://api.auditoria360.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "scope=audit:read audit:write"
```

### **3. Make API Calls**
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.auditoria360.com/api/v1/audits"
```

---

## 📊 **Common Patterns**

### **🔍 Filtering and Search**
Most list endpoints support filtering:
```bash
GET /api/v1/audits?status=completed&type=payroll&created_after=2024-01-01
```

### **📄 Pagination**
Use `limit` and `offset` for pagination:
```bash
GET /api/v1/audits?limit=50&offset=100
```

### **📋 Field Selection**
Select specific fields to reduce bandwidth:
```bash
GET /api/v1/audits?fields=id,status,created_at
```

### **🔗 Resource Expansion**
Expand related resources in a single call:
```bash
GET /api/v1/audits/123?expand=client,documents
```

---

## 🛡️ **Security**

### **🔐 Authentication Scopes**
| Scope | Description |
|-------|-------------|
| `audit:read` | View audit data |
| `audit:write` | Create and modify audits |
| `user:read` | View user information |
| `user:write` | Modify user information |
| `admin` | Full administrative access |

### **🚨 Rate Limiting**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1642176000
X-RateLimit-Scope: user
```

When rate limit is exceeded:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Try again later.",
    "retry_after": 3600
  }
}
```

---

## 📊 **Status Codes**

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | **OK** | Request successful |
| `201` | **Created** | Resource created successfully |
| `400` | **Bad Request** | Invalid request parameters |
| `401` | **Unauthorized** | Authentication required |
| `403` | **Forbidden** | Insufficient permissions |
| `404` | **Not Found** | Resource not found |
| `429` | **Too Many Requests** | Rate limit exceeded |
| `500` | **Internal Server Error** | Server error |
| `503` | **Service Unavailable** | Service temporarily unavailable |

---

## 🧪 **Testing**

### **🏖️ Sandbox Environment**
```yaml
Base_URL: "https://sandbox-api.auditoria360.com"
Rate_Limits: "None (for testing)"
Test_Data: "Pre-populated samples"
Reset: "Daily at 00:00 UTC"
```

### **🔧 Test Credentials**
```yaml
Client_ID: "test_client_123"
Client_Secret: "test_secret_456"
Test_User: "test@auditoria360.com"
```

---

## 📚 **SDKs and Examples**

### **🐍 Python**
```bash
pip install auditoria360-sdk
```

```python
from auditoria360 import Client

client = Client(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Create audit
audit = client.audits.create(
    type="payroll",
    client_id="client_123"
)

print(f"Audit created: {audit.id}")
```

### **🟨 JavaScript/Node.js**
```bash
npm install @auditoria360/sdk
```

```javascript
import { Auditoria360Client } from '@auditoria360/sdk';

const client = new Auditoria360Client({
  clientId: 'your_client_id',
  clientSecret: 'your_client_secret'
});

// Create audit
const audit = await client.audits.create({
  type: 'payroll',
  clientId: 'client_123'
});

console.log(`Audit created: ${audit.id}`);
```

---

## 🔗 **Related Resources**

### **📖 Documentation**
- **[Developer Guide](../developer-guides/api-documentation)** - Detailed API documentation
- **[Authentication Guide](./authentication)** - Auth implementation details
- **[Webhook Guide](./endpoints/webhooks)** - Real-time notifications

### **🛠️ Tools**
- **[Swagger UI](https://api.auditoria360.com/docs)** - Interactive API explorer
- **[Postman Collection](https://www.postman.com/auditoria360)** - Ready-to-use API calls
- **[OpenAPI Spec](https://api.auditoria360.com/openapi.json)** - Machine-readable spec

### **💬 Support**
- **[API Support](mailto:api-support@auditoria360.com.br)** - Technical assistance
- **[Status Page](https://status.auditoria360.com)** - API status and incidents
- **[Discord Community](https://discord.gg/auditoria360)** - Developer community

---

> **💡 Pro Tip**: Use the interactive Swagger documentation to explore endpoints and test API calls directly in your browser!