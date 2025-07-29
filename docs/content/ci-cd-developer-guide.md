# Developer CI/CD Guide

## Quick Start

### Setting Up Your Development Environment

1. **Clone the repository:**

```bash
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
```

2. **Install dependencies:**

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt
```

3. **Setup pre-commit hooks:**

```bash
make setup-hooks
# or manually:
pre-commit install
```

### Running Tests Locally

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests only
pytest tests/frontend/          # Frontend tests only

# Run tests with verbose output
pytest tests/ -v

# Run tests excluding problematic modules
pytest tests/ --ignore=tests/e2e/test_e2e_playwright.py
```

### Code Quality Checks

```bash
# Run all quality checks
make quality

# Individual tools
make format     # Format code with black and isort
make lint       # Run flake8 linting
make check      # Check formatting without applying changes

# Pre-commit hooks (runs automatically on commit)
pre-commit run --all-files
```

## CI/CD Workflow Details

### Automatic Triggers

**On Push to `main` or `develop`:**

- Full CI/CD pipeline runs
- All tests and quality checks execute
- Automatic deployment on success

**On Pull Request to `main`:**

- Complete validation pipeline
- No deployment until merge

**Daily at 9 AM UTC:**

- Automation workflows execute
- Scheduled reports generated
- System backups performed

### Pipeline Stages

1. **Pre-commit** (< 2 minutes)
   - Code formatting validation
   - Import sorting check
   - Basic linting

2. **Testing** (5-8 minutes)
   - Matrix testing on Python 3.11 and 3.12
   - Unit and integration tests
   - Coverage reporting

3. **Frontend Testing** (3-5 minutes)
   - Node.js environment setup
   - Frontend linting and tests
   - Build validation

4. **Automation Testing** (2-3 minutes)
   - Serverless function validation
   - GitHub Actions compatibility

5. **API Health Check** (1-2 minutes)
   - API import validation
   - Health endpoint testing

6. **Deployment** (2-4 minutes)
   - Staging deployment (develop branch)
   - Production deployment (main branch)

## Writing Tests

### Test Structure Guidelines

```python
# Unit test example
def test_function_name():
    """Test description with expected behavior."""
    # Arrange
    input_data = {"key": "value"}

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_output
    assert "expected_key" in result
```

### Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient

def test_api_endpoint():
    """Test API endpoint functionality."""
    with TestClient(app) as client:
        response = client.post("/api/endpoint", json={"data": "test"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
```

### Test Configuration

**Pytest Configuration** (`tests/pytest.ini`)

- Test discovery patterns
- Coverage settings
- Plugin configuration

**Test Environment** (`tests/conftest.py`)

- Global fixtures
- Mock configurations
- Test database setup

## Managing Dependencies

### Adding New Dependencies

1. **Production dependency:**

```bash
# Add to requirements.txt
echo "new-package>=1.0.0" >> requirements.txt
```

2. **Development dependency:**

```bash
# Add to requirements-dev.txt
echo "dev-package>=1.0.0" >> requirements-dev.txt
```

3. **Update CI configuration if needed:**

- Optional dependencies should be handled gracefully
- Update test exclusions if tests require heavy dependencies

### Handling Optional Dependencies

For ML or heavy dependencies:

```python
try:
    import tensorflow as tf
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False

@pytest.mark.skipif(not HAS_TENSORFLOW, reason="TensorFlow not available")
def test_ml_functionality():
    # Test that requires TensorFlow
    pass
```

## Branch Management

### Development Workflow

1. **Feature Development:**

```bash
git checkout -b feature/your-feature-name
# Make changes
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

2. **Create Pull Request:**

- Target `main` branch
- Include description of changes
- Ensure CI passes before requesting review

3. **After Review:**

- Address feedback
- Ensure all checks pass
- Merge when approved

### Branch Protection Rules

**Main Branch:**

- Requires pull request reviews
- Requires status checks to pass
- No direct pushes allowed
- Automatic deployment on merge

**Develop Branch:**

- Staging deployment target
- Less strict requirements
- Used for integration testing

## Debugging CI/CD Issues

### Common Failures and Solutions

**Test Failures:**

1. Check the GitHub Actions logs
2. Run tests locally to reproduce
3. Check for environment differences
4. Validate test data and fixtures

**Linting Failures:**

```bash
# Fix formatting issues
black .
isort .

# Check specific linting errors
flake8 . --show-source
```

**Deployment Failures:**

1. Check Vercel deployment logs
2. Verify environment variables
3. Validate build configuration
4. Check for breaking changes

### Accessing Logs

**GitHub Actions:**

1. Go to repository → Actions tab
2. Click on failed workflow run
3. Expand failed job for detailed logs
4. Download logs for offline analysis

**Vercel Deployment:**

1. Check Vercel dashboard
2. Review deployment logs
3. Monitor function execution
4. Check runtime errors

## Performance Optimization

### Test Performance

**Speed Up Local Testing:**

```bash
# Run tests in parallel
pytest tests/ -n auto

# Run only modified tests
pytest tests/ --lf  # last failed
pytest tests/ --ff  # failed first

# Skip slow tests during development
pytest tests/ -m "not slow"
```

**CI Performance:**

- Tests run in parallel where possible
- Cached dependencies for faster builds
- Matrix jobs for parallel Python version testing

### Resource Usage

**Memory Management:**

- Large test datasets are mocked
- Database connections are pooled
- Temporary files are cleaned up

**Build Time Optimization:**

- Dependency caching enabled
- Incremental builds where possible
- Parallel job execution

## Security Considerations

### Secrets Management

**Never commit secrets:**

- Use environment variables
- Configure secrets in GitHub repository settings
- Use .env files for local development (excluded from git)

**Secret Rotation:**

- Regularly update API tokens
- Monitor secret usage
- Use least privilege access

### Code Security

**Automated Scanning:**

- Dependency vulnerability scanning
- Code quality analysis
- Security linting rules

## Getting Help

### Documentation Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)

### Team Support

- Create GitHub issue for CI/CD problems
- Tag @devops-team for urgent deployment issues
- Check existing issues for similar problems

### Useful Commands

```bash
# Reset local environment
make clean
pip install -r requirements.txt -r requirements-dev.txt

# Update all dependencies
pip-review --auto

# Generate new requirements.txt
pip freeze > requirements.txt

# Check outdated packages
pip list --outdated
```
