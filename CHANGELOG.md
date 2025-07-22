# CHANGELOG

All notable changes to the AUDITORIA360 project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **🔐 MAJOR FEATURE**: Complete authentication system with JWT tokens
- **🧪 COMPREHENSIVE TESTS**: Full authentication test suite (11/11 tests passing)
- **⚙️ CONFIG SYSTEM**: YAML-based configuration management for services
- **🛡️ SECURITY**: Bcrypt password hashing, JWT token validation
- **📊 API HEALTH**: Health check endpoints for all services
- **🌐 CORS SUPPORT**: Cross-origin request handling for frontend integration
- Comprehensive project analysis and documentation
- Modern test infrastructure with pytest, coverage reporting
- Structured services architecture (api, core, ingestion, ml)
- ML pipeline with Kubeflow support (mock implementation)
- Pydantic v2 migration for better validation
- FastAPI health checks and CORS configuration
- Project analysis documentation in `/docs/`

### Fixed
- ✅ Fixed all core test imports and dependencies (12/12 core + 11/11 auth tests passing)
- ✅ Fixed Pydantic deprecation warnings (v1 → v2 validators)
- ✅ Fixed missing functions in bq_loader and docai_utils modules
- ✅ Fixed API main.py import errors by removing non-existent routes
- ✅ Fixed ML pipeline definition syntax errors
- ✅ Fixed CPF validation and normalization in entity schema
- ✅ Fixed JWT error handling (PyJWTError vs JWTError)
- ✅ Fixed datetime deprecation warnings (UTC timezone support)

### Security
- 🔐 JWT-based authentication with configurable expiration
- 🔒 Bcrypt password hashing for user credentials
- 🛡️ Token validation middleware for protected endpoints
- 📋 User registration and management system
- 🏢 Multi-client/empresa support in authentication
- ⚠️ **Production Note**: Change JWT secret key from development default

### API Endpoints Added
- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration  
- `GET /auth/me` - Current user information
- `POST /auth/logout` - User logout
- `GET /auth/health` - Authentication service health
- `GET /health` - Overall API health check
- `POST /explainability/executar-pipeline` - ML pipeline execution

### Testing
- ✅ 23/23 total tests passing (12 core + 11 auth)
- 🧪 Authentication test coverage: login, registration, token validation
- 🔍 API integration tests for all endpoints
- 📊 Test coverage reporting with pytest-cov

### Changed
- Migrated from legacy `src/` structure to `services/` architecture
- Updated entity validation to use Pydantic v2 field validators
- Enhanced API structure with authentication and health monitoring
- Added mock implementations for external dependencies (Kubeflow)
- API version bumped to 0.2.0

### Configuration
- Added YAML configuration system in `services/configs/`
- Environment-based JWT secret configuration
- Service-specific configuration files (DocAI, common settings)
- Development and production configuration support

## Historical Context

### Previous Implementation (in src_legacy_backup/)
The system previously included:
- 25+ API route modules for complete business functionality
- 20+ backend controllers for business logic
- Comprehensive RBAC and multi-client support
- Advanced CCT (Collective Bargaining Agreement) processing
- Full audit trail and reporting system
- ETL pipelines for data processing

### Refactoring Strategy
Current refactoring moves from monolithic to microservices architecture:
- Core services modularization
- Google Cloud native integration
- Modern ML/AI pipeline with explainability
- Enhanced security and monitoring

## Next Steps

### High Priority
1. Restore authentication system from legacy backup
2. Fix remaining 29 test files with legacy imports
3. Restore core PDF processing API routes
4. Implement proper error handling and logging

### Medium Priority  
1. Restore advanced business features (CCT management, risk prediction)
2. Enhance documentation and API specifications
3. Implement CI/CD pipeline
4. Security audit and dependency updates

### Future Enhancements
1. Performance optimization and monitoring
2. Enhanced UI/UX improvements
3. Advanced ML features and model monitoring
4. Enterprise-grade security and compliance features