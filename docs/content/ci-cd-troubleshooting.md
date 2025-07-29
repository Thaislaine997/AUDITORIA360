# CI/CD Troubleshooting Guide

## Common Issues and Solutions

### Test Failures

#### 1. Import Errors (ModuleNotFoundError)

**Problem:**

```
ImportError: No module named 'tensorflow'
ModuleNotFoundError: No module named 'shap'
```

**Solution:**

```bash
# Option 1: Install missing dependencies
pip install tensorflow shap

# Option 2: Skip tests that require optional dependencies
pytest tests/ --ignore=tests/unit/test_ml_components_autoencoder.py

# Option 3: Mark tests as optional (in test file)
import pytest

try:
    import tensorflow as tf
    HAS_TF = True
except ImportError:
    HAS_TF = False

@pytest.mark.skipif(not HAS_TF, reason="TensorFlow not available")
def test_ml_function():
    pass
```

#### 2. Database Connection Errors

**Problem:**

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection failed
```

**Solution:**

```python
# In conftest.py - mock database for tests
@pytest.fixture
def mock_db():
    from unittest.mock import MagicMock
    return MagicMock()

# In test file
def test_database_function(mock_db):
    # Use mock instead of real database
    pass
```

#### 3. Async Test Issues

**Problem:**

```
RuntimeError: There is no current event loop in thread
```

**Solution:**

```python
# Use pytest-asyncio
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Linting and Formatting Issues

#### 1. Black Formatting Conflicts

**Problem:**

```
would reformat file.py
```

**Solution:**

```bash
# Fix all formatting issues
black .

# Check specific file
black --check src/specific_file.py

# Fix specific file
black src/specific_file.py
```

#### 2. Import Sorting Issues (isort)

**Problem:**

```
Imports are incorrectly sorted and/or formatted
```

**Solution:**

```bash
# Fix all import sorting
isort .

# Check specific file
isort --check-only src/specific_file.py

# Fix specific file with black profile
isort --profile black src/specific_file.py
```

#### 3. Flake8 Violations

**Problem:**

```
E501 line too long (89 > 88 characters)
F401 'module' imported but unused
```

**Solution:**

```bash
# Check all violations
flake8 . --show-source

# Fix line length (use black)
black .

# Remove unused imports
autoflake --in-place --remove-all-unused-imports --recursive .

# Or manually remove unused imports
```

### GitHub Actions Failures

#### 1. Workflow Syntax Errors

**Problem:**

```
Invalid workflow file: .github/workflows/ci-cd.yml
```

**Solution:**

1. Validate YAML syntax online: https://yamlchecker.com/
2. Check GitHub Actions documentation for correct syntax
3. Use GitHub's workflow editor for validation

#### 2. Matrix Job Failures

**Problem:**

```
Strategy job failed: Python 3.11 tests failed
```

**Solution:**

```yaml
# Add continue-on-error for non-critical versions
strategy:
  matrix:
    python-version: [3.11, 3.12]
  fail-fast: false # Continue other jobs if one fails

steps:
  - name: Test with Python ${{ matrix.python-version }}
    continue-on-error: ${{ matrix.python-version == '3.11' }}
```

#### 3. Timeout Issues

**Problem:**

```
The job running on ubuntu-latest exceeded the maximum execution time
```

**Solution:**

```yaml
# Increase timeout
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30 # Increase from default 6 hours

    steps:
      - name: Run tests
        timeout-minutes: 15 # Set step-specific timeout
```

### Deployment Issues

#### 1. Vercel Deployment Failures

**Problem:**

```
Error: Build failed with exit code 1
```

**Solution:**

1. Check build logs in Vercel dashboard
2. Verify environment variables are set
3. Test build locally:

```bash
# Install Vercel CLI
npm i -g vercel

# Test deployment locally
vercel dev
```

#### 2. Environment Variable Issues

**Problem:**

```
KeyError: 'REQUIRED_ENV_VAR'
```

**Solution:**

1. Add missing environment variables in GitHub repository settings
2. Use default values for optional variables:

```python
import os
API_KEY = os.getenv('API_KEY', 'default_value')
```

#### 3. Secret Access Issues

**Problem:**

```
Error: Secret VERCEL_TOKEN not found
```

**Solution:**

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add required secrets
3. Verify secret names match workflow file exactly

### Coverage Issues

#### 1. Low Coverage Warnings

**Problem:**

```
TOTAL coverage: 65% (below 70% threshold)
```

**Solution:**

```bash
# Generate detailed coverage report
pytest tests/ --cov=src --cov-report=html

# Open htmlcov/index.html to see uncovered lines

# Add tests for uncovered code or exclude non-testable code
# In .coveragerc:
[run]
omit =
    */migrations/*
    */venv/*
    */env/*
    */tests/*
```

#### 2. Coverage Report Generation Failures

**Problem:**

```
Coverage.py warning: No data to report
```

**Solution:**

```bash
# Ensure tests are actually running
pytest tests/ -v

# Check coverage configuration
cat .coveragerc

# Run with specific source
pytest tests/ --cov=. --cov-report=term
```

### Pre-commit Hook Issues

#### 1. Pre-commit Installation Failures

**Problem:**

```
command not found: pre-commit
```

**Solution:**

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Update hooks to latest versions
pre-commit autoupdate
```

#### 2. Hook Execution Failures

**Problem:**

```
black....................................................................Failed
```

**Solution:**

```bash
# Run hooks manually to see detailed errors
pre-commit run --all-files

# Fix specific hook issues
black .
isort .
flake8 .

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

### Dependency Issues

#### 1. Version Conflicts

**Problem:**

```
ERROR: package-a 1.0.0 has requirement package-b<2.0.0, but you have package-b 2.1.0
```

**Solution:**

```bash
# Check dependency tree
pip check

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install specific versions
pip install "package-b>=1.5.0,<2.0.0"

# Update requirements.txt
pip freeze > requirements.txt
```

#### 2. Missing System Dependencies

**Problem:**

```
Error: Microsoft Visual C++ 14.0 is required
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution:**

```bash
# For Ubuntu/Linux
sudo apt-get update
sudo apt-get install build-essential

# For macOS
xcode-select --install

# For Windows
# Install Visual Studio Build Tools
```

### Performance Issues

#### 1. Slow Test Execution

**Problem:**
Tests taking too long to complete

**Solution:**

```bash
# Run tests in parallel
pip install pytest-xdist
pytest tests/ -n auto

# Identify slow tests
pytest tests/ --durations=10

# Mark slow tests
@pytest.mark.slow
def test_slow_function():
    pass

# Skip slow tests in development
pytest tests/ -m "not slow"
```

#### 2. High Memory Usage

**Problem:**

```
MemoryError: Unable to allocate array
```

**Solution:**

```python
# Use generators instead of lists for large datasets
def process_large_data():
    for item in large_dataset:
        yield process_item(item)

# Clean up resources explicitly
def test_with_cleanup():
    resource = create_resource()
    try:
        # test code
        pass
    finally:
        resource.cleanup()
```

## Emergency Procedures

### 1. Rollback Deployment

**If production deployment fails:**

```bash
# Using Vercel CLI
vercel rollback --token $VERCEL_TOKEN

# Or via GitHub
# Revert the merge commit
git revert HEAD
git push origin main
```

### 2. Bypass CI for Hotfix

**Only in emergencies:**

```bash
# Create hotfix branch
git checkout -b hotfix/critical-fix

# Make minimal changes
# Commit with [skip ci] to bypass CI
git commit -m "[skip ci] Critical hotfix for security issue"

# Deploy directly
# This should be followed by proper CI validation
```

### 3. Disable Failing Workflows

**If CI is blocking all deployments:**

1. Go to repository → Actions
2. Select failing workflow
3. Click "..." → Disable workflow
4. Fix issues and re-enable

## Getting Additional Help

### 1. GitHub Actions Logs

```bash
# Download logs using GitHub CLI
gh run download <run-id>

# View logs in browser
# Go to: https://github.com/USER/REPO/actions/runs/RUN_ID
```

### 2. Local Debugging

```bash
# Reproduce CI environment locally
docker run -it python:3.12 bash
pip install -r requirements.txt
python -m pytest tests/
```

### 3. Community Resources

- [GitHub Actions Community Forum](https://github.community/c/github-actions/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/github-actions)

### 4. Contact Information

- **DevOps Team**: Create issue with label `devops`
- **Emergency Contact**: Use #incidents Slack channel
- **Documentation Issues**: Create issue with label `documentation`
