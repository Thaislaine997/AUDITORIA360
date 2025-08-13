# AUDITORIA360 - Security & RLS Implementation

This document outlines the Row Level Security (RLS) and security infrastructure implemented for AUDITORIA360.

## 🔒 Row Level Security (RLS) Implementation

### Overview
Multi-tenant data isolation ensuring each contabilidade can only access their own data, complying with LGPD requirements.

### Test Suite
**Location**: `tests/integration/test_rls.py`

**Coverage**:
- ✅ Tenant isolation validation
- ✅ JWT token claims verification  
- ✅ Cross-tenant data leakage prevention
- ✅ LGPD compliance checks
- ✅ Performance impact assessment
- ✅ Security headers validation

**Run Tests**:
```bash
# Run all RLS tests
python -m pytest tests/integration/test_rls.py -v

# Run specific test categories
python -m pytest tests/integration/test_rls.py::TestRLSIsolation -v
python -m pytest tests/integration/test_rls.py::TestRLSCompliance -v
```

### Database Policies
**Location**: `supabase/policies/tenants_rls.sql`

**Features**:
- Automatic tenant isolation using `jwt.claims.contabilidade_id`
- Policies for all major tables (clientes, auditorias, folhas_pagamento, etc.)
- Audit logging isolation for compliance
- Helper functions for tenant context management

## 🛡️ Security Infrastructure

### Secret Scanning
**Configuration**: `.gitleaks.toml`

**Detects**:
- AWS credentials (access keys, secret keys)
- OpenAI API keys
- GitHub tokens
- Supabase keys
- Database URLs with credentials
- JWT secrets
- Generic API keys

**Run Scan**:
```bash
# Install gitleaks first
# https://github.com/gitleaks/gitleaks

gitleaks detect --config .gitleaks.toml
```

### CI/CD Security Pipeline
**Location**: `.github/workflows/rls-tests.yml`

**Features**:
- Automated RLS testing on every PR
- PostgreSQL + Redis test environment
- Secret scanning integration
- Policy validation
- Daily scheduled security checks

**Trigger Paths**:
- `api/**` - Backend changes
- `src/**` - Source code changes
- `tests/integration/test_rls.py` - RLS test changes
- `supabase/**` - Database policy changes

## 📊 Observability

### Structured Logging
**Location**: `src/utils/structured_logging.py`

**Features**:
- JSON-formatted logs for production
- Tenant context in every log entry
- Security event logging
- Data access logging (LGPD compliance)
- Performance metrics logging

**Usage**:
```python
from src.utils.structured_logging import (
    setup_structured_logging,
    log_security_event,
    log_data_access,
    audit_context
)

# Setup logging
logger = setup_structured_logging("auditoria360")

# Log with tenant context
with audit_context(tenant_id="contab_123", user_id="user_456"):
    logger.info("Processing payroll data")

# Log security events
log_security_event(
    "unauthorized_access_attempt",
    "User attempted to access different tenant data",
    tenant_id="contab_123",
    severity="WARNING"
)

# Log data access for LGPD
log_data_access(
    table_name="clientes",
    operation="SELECT",
    tenant_id="contab_123",
    user_id="user_456",
    record_count=10
)
```

## 🐳 Development Environment

### Docker Compose Setup
**Location**: `docker-compose.dev.yml`

**Services**:
- PostgreSQL 15 with RLS policies pre-loaded
- Redis 7 for caching/sessions
- API service with hot reload
- Frontend service (when dependencies installed)

**Start Development Environment**:
```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Start specific services
docker-compose -f docker-compose.dev.yml up postgres redis api
```

**Environment Variables**:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/auditoria_dev
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
LOG_JSON=true
ENVIRONMENT=development
```

## 🧪 Testing Strategy

### Test Categories
1. **Unit Tests**: Individual function testing
2. **Integration Tests**: RLS and API testing  
3. **E2E Tests**: Full user workflow testing (Playwright)
4. **Security Tests**: Secret scanning, RLS validation
5. **Performance Tests**: RLS impact assessment

### Running Tests
```bash
# All RLS tests
python -m pytest tests/integration/test_rls.py -v

# Specific test class
python -m pytest tests/integration/test_rls.py::TestRLSIsolation -v

# Performance tests (marked as slow)
python -m pytest tests/integration/test_rls.py::TestRLSPerformance -v

# With coverage
python -m pytest tests/integration/test_rls.py --cov=api --cov=src
```

## 📋 Compliance & Audit

### LGPD Compliance Features
- ✅ Tenant data isolation at database level
- ✅ Audit trail logging with tenant context
- ✅ Data access logging for all operations
- ✅ Security event logging for compliance
- ✅ User consent and access tracking (structured logs)

### Audit Trail
All security-relevant events are logged with:
- Timestamp
- Tenant ID
- User ID  
- Operation type
- Data accessed
- Request ID for tracing

### Security Headers
API validates and logs:
- `x-contabilidade-id` - Tenant identification
- `x-client-id` - Client identification  
- `Authorization` - JWT tokens with tenant claims

## 🚀 Deployment Notes

### Production Checklist
- [ ] Enable RLS policies on all tenant tables
- [ ] Configure JWT claims with tenant identification
- [ ] Set up structured logging aggregation (ELK/Grafana)
- [ ] Enable secret scanning in CI/CD
- [ ] Configure database backups with tenant isolation
- [ ] Set up monitoring alerts for security events

### Environment Configuration
```bash
# Production
LOG_JSON=true
LOG_LEVEL=INFO
ENVIRONMENT=production

# Enable RLS testing
RLS_TESTS_ENABLED=true
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## 📞 Support

For security issues or RLS policy questions, refer to:
- `tests/integration/test_rls.py` - Test examples
- `supabase/policies/tenants_rls.sql` - Policy templates
- `.github/workflows/rls-tests.yml` - CI configuration