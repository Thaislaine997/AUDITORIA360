# AUDITORIA360 - Models README

## 📋 Data Models Overview

This directory contains the data models for the AUDITORIA360 platform.

### 🏗️ Architecture

The actual implementation is located in `src/models/` directory. This directory provides legacy compatibility for the checklist validation system.

### 📊 Available Models

- **auth_models.py**: User authentication and authorization models
- **audit_models.py**: Audit trail and compliance models  
- **payroll_models.py**: Payroll processing models
- **cct_models.py**: CCT (Collective Bargaining Agreement) models
- **document_models.py**: Document processing models
- **client_models.py**: Client management models
- **notification_models.py**: Notification system models
- **report_models.py**: Report generation models
- **ai_models.py**: AI/ML model configurations

### 🔄 Migration Status

✅ All models have been migrated to `src/models/` directory  
✅ SQLAlchemy ORM implemented  
✅ Pydantic schemas for API validation  
✅ Database migrations available in `migrations/`

### 📚 Documentation

For detailed model documentation, see:
- [API Reference](../docs-source/05_Referencia_da_API/README.md)
- [Database Schema](../data_base/schemas/)
- [Development Guide](../docs-source/02_Guias_de_Desenvolvedor/architecture-overview.md)

---

*Legacy reference maintained for checklist compatibility*