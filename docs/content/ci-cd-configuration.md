# CI/CD Configuration Documentation

## Overview

This document describes the complete CI/CD setup for the AUDITORIA360 project, including automated testing, code quality checks, and deployment pipelines.

## GitHub Actions Workflows

### 1. Main CI/CD Pipeline (`ci-cd.yml`)

**Triggers:**

- Push to `main` and `develop` branches
- Pull requests to `main` branch

**Jobs:**

#### Pre-commit

- Runs pre-commit hooks for code quality
- Validates code formatting, imports, and basic checks
- Uses tools: black, isort, flake8, autoflake

#### Test (Matrix: Python 3.11, 3.12)

- **Linting**: Critical error detection with flake8
- **Code Quality**: Black and isort validation
- **Unit Tests**: Comprehensive test suite with coverage
- **Integration Tests**: API and system integration tests
- **Coverage Report**: Uploaded to Codecov

#### Frontend Tests

- Node.js 20 environment
- Frontend linting and testing
- Build validation

#### Automation Tests

- Serverless automation testing
- GitHub Actions environment compatibility
- RPA migration validation

#### API Health Check

- API import and functionality validation
- Health endpoint testing

#### Deployment

- **Staging**: Deploys to Vercel staging on `develop` branch
- **Production**: Deploys to Vercel production on `main` branch

### 2. Automation Pipeline (`automation.yml`)

**Triggers:**

- Daily cron schedule (9 AM UTC)
- Manual workflow dispatch

**Jobs:**

- **Legislation Automation**: Daily scraping and data collection
- **Communications Automation**: Automated messaging workflows
- **Payroll RPA**: Automated payroll processing
- **Scheduled Reports**: Daily and weekly report generation
- **Backup Routine**: Automated system backups
- **Health Checks**: Automation system validation

### 3. Documentation (`jekyll-gh-pages.yml`)

- Builds and deploys documentation site
- Uses Jekyll for static site generation

## Code Quality Standards

### Linting Configuration

**Flake8** (`.flake8`)

```ini
max-line-length = 88
extend-ignore = E203, W503, E501
```

**Black** (`pyproject.toml`)

```toml
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
```

**Isort** (`pyproject.toml`)

```toml
profile = "black"
line_length = 88
```

### Pre-commit Hooks

Configured in `.pre-commit-config.yaml`:

- Trailing whitespace removal
- End-of-file fixing
- YAML validation
- Large file checks
- Merge conflict detection
- Black code formatting
- Isort import sorting
- Flake8 linting
- Autoflake unused import removal

## Testing Strategy

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for API and services
├── e2e/           # End-to-end tests with Playwright
├── performance/   # Performance and load tests
├── frontend/      # Frontend-specific tests
└── conftest.py    # Global test configuration
```

### Test Execution

**Local Testing:**

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

**CI Testing:**

- Excludes tests requiring optional ML dependencies
- Focuses on core functionality and API validation
- Provides detailed coverage reports

### Coverage Requirements

- Minimum coverage threshold: 70%
- Critical modules require 90%+ coverage
- Coverage reports generated in XML and HTML formats

## Deployment Process

### Staging Deployment

1. Code pushed to `develop` branch
2. All CI checks pass
3. Automatic deployment to Vercel staging environment
4. Staging tests execute

### Production Deployment

1. Pull request merged to `main` branch
2. Full CI/CD pipeline execution
3. All quality gates pass
4. Automatic deployment to Vercel production
5. Post-deployment health checks

## Environment Configuration

### Required Secrets

- `VERCEL_TOKEN`: Vercel deployment token
- `VERCEL_ORG_ID`: Vercel organization ID
- `VERCEL_PROJECT_ID`: Vercel project ID
- `API_BASE_URL`: Base URL for API services
- `API_AUTH_TOKEN`: Authentication token for API
- `BACKUP_STORAGE_URL`: Backup storage endpoint
- `STORAGE_TOKEN`: Storage access token

### Environment Variables

- `GITHUB_ACTIONS`: Indicates CI environment
- `TESTING`: Enables testing mode
- `ENVIRONMENT`: Deployment environment (staging/production)

## Dependencies Management

### Production Dependencies (`requirements.txt`)

Core application dependencies including:

- FastAPI, SQLAlchemy, Pydantic
- Data processing: pandas, duckdb
- ML libraries: scikit-learn
- Authentication: python-jose, passlib
- Frontend: streamlit, plotly

### Development Dependencies (`requirements-dev.txt`)

Testing and development tools:

- pytest and plugins
- Code quality tools: black, isort, flake8
- Coverage reporting
- Documentation tools: mkdocs

## Monitoring and Alerts

### CI/CD Monitoring

- GitHub Actions status monitoring
- Build failure notifications
- Deployment status tracking
- Coverage trend analysis

### Quality Metrics

- Code coverage percentage
- Test execution time
- Linting error counts
- Security vulnerability scans

## Troubleshooting

### Common Issues

**Test Failures:**

1. Check for missing dependencies
2. Validate environment configuration
3. Review test isolation issues
4. Check for database connection problems

**Deployment Failures:**

1. Verify secret configuration
2. Check build logs for errors
3. Validate environment variables
4. Confirm Vercel configuration

**Linting Failures:**

1. Run `black .` for formatting
2. Run `isort .` for import sorting
3. Address flake8 warnings
4. Update pre-commit hooks

### Getting Help

- Check GitHub Actions logs for detailed error information
- Review this documentation for configuration details
- Contact the development team for critical issues

## Maintenance

### Regular Tasks

- Update dependencies monthly
- Review and update test coverage requirements
- Monitor CI/CD performance metrics
- Update documentation as needed

### Periodic Reviews

- Quarterly review of CI/CD pipeline efficiency
- Annual security audit of workflows and secrets
- Regular performance optimization of test suites
