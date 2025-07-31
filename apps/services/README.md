# AUDITORIA360 - Services Layer

## 🔧 Business Logic Services

This directory contains the business logic services for the AUDITORIA360 platform.

### 🏗️ Architecture

The actual implementation is located in `src/services/` directory. This directory provides legacy compatibility for the checklist validation system.

### 🛠️ Available Services

#### Core Services
- **auth_service.py**: Authentication and authorization logic
- **user_service.py**: User management operations  
- **cache_service.py**: Redis caching layer
- **duckdb_optimizer.py**: Query optimization service

#### Advanced Services  
- **openai_service.py**: AI/ML integration service
- **payroll_service.py**: Payroll processing logic
- **enhanced_notification_service.py**: Multi-channel notifications

#### Storage Services
- **storage/storage_service.py**: File storage abstraction
- **ocr/ocr_service.py**: OCR processing service

#### Communication
- **communication_gateway/**: Multi-provider communication hub
  - **gateway.py**: Main gateway service
  - **providers.py**: Provider implementations
  - **github_integration.py**: GitHub API integration

### 📋 Service Pattern

All services follow the Repository/Service pattern:

```python
class BaseService:
    def __init__(self, repository):
        self.repository = repository
    
    async def create(self, data): ...
    async def get(self, id): ...
    async def update(self, id, data): ...
    async def delete(self, id): ...
```

### 🔄 Migration Status

✅ All services migrated to `src/services/` directory  
✅ Dependency injection implemented  
✅ Async/await pattern adopted  
✅ Error handling standardized  
✅ Logging and monitoring integrated

### 📚 Documentation

For detailed service documentation, see:
- [API Reference](../docs-source/05_Referencia_da_API/README.md)
- [Service Architecture](../docs-source/02_Guias_de_Desenvolvedor/architecture-overview.md)

---

*Legacy reference maintained for checklist compatibility*