# 🛠️ AUDITORIA360 - Developer Environment Setup

This directory contains automated scripts for setting up the AUDITORIA360 development environment on different operating systems.

## 📋 Quick Start

### Linux/macOS
```bash
chmod +x installers/setup_dev_env.sh
./installers/setup_dev_env.sh
```

### Windows (PowerShell as Administrator)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\installers\setup_dev_env.ps1
```

### Manual Setup
If you prefer manual setup or encounter issues with the automated scripts:

1. **Copy environment template:**
   ```bash
   cp installers/.env.example .env.local
   ```

2. **Edit configuration:**
   Edit `.env.local` with your actual database and API credentials

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```bash
   python installers/init_db.py
   ```

## 📁 Files Overview

| File | Description | OS Support |
|------|-------------|------------|
| `setup_dev_env.sh` | Main setup script for Unix systems | Linux, macOS |
| `setup_dev_env.ps1` | Main setup script for Windows | Windows |
| `.env.example` | Environment configuration template | All |
| `init_db.py` | Database initialization script | All |
| `compilar_instalador_windows.bat` | Legacy Windows installer | Windows |

## 🔧 What the Setup Scripts Do

### Automated Installation
- ✅ **Python 3.8+** verification and installation
- ✅ **Virtual environment** creation and activation
- ✅ **Dependencies** installation from requirements.txt
- ✅ **Development tools** (pytest, flake8, black, isort)
- ✅ **Pre-commit hooks** setup
- ✅ **Environment files** creation from template
- ✅ **Database initialization** (if configured)
- ✅ **Installation verification** tests

### Environment Configuration
The scripts create a comprehensive `.env.local` file with all necessary configuration options:

- **Database**: Neon PostgreSQL connection
- **Storage**: Cloudflare R2 configuration  
- **AI Services**: OpenAI API, PaddleOCR settings
- **Authentication**: JWT configuration
- **Development**: Debug settings, logging levels
- **Features**: Feature flags for optional components

## 🏗️ Architecture Components

### Core Stack
- **API**: FastAPI with async support
- **Database**: Neon PostgreSQL (serverless)
- **Storage**: Cloudflare R2 (S3-compatible)
- **Analytics**: DuckDB (embedded)
- **OCR**: PaddleOCR (local processing)
- **ML Orchestration**: Prefect

### Development Tools
- **Testing**: pytest with coverage
- **Linting**: flake8, black, isort
- **Pre-commit**: Automated code quality checks
- **Environment**: Python virtual environments

## 📚 Configuration Details

### Database Setup (Neon PostgreSQL)
```bash
# Required environment variables
DATABASE_URL=postgresql://username:password@host:5432/database
NEON_DATABASE_URL=postgresql://username:password@host:5432/database
```

### Storage Setup (Cloudflare R2)
```bash
# Required for file storage
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_ENDPOINT_URL=https://account.r2.cloudflarestorage.com
R2_BUCKET_NAME=auditoria360-storage
```

### AI Services Setup
```bash
# OpenAI for chatbot and AI features
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4

# PaddleOCR for document processing
PADDLE_OCR_USE_GPU=false
PADDLE_OCR_LANG=pt
```

## 🚀 Post-Installation Steps

1. **Edit Configuration**
   ```bash
   nano .env.local  # Edit with your actual credentials
   ```

2. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\Activate.ps1  # Windows
   ```

3. **Start Development Server**
   ```bash
   uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

5. **Access API Documentation**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔍 Troubleshooting

### Common Issues

**Python Version Error**
```bash
# Install Python 3.8+ manually
# Linux: apt install python3.9
# macOS: brew install python@3.9
# Windows: Download from python.org
```

**Permission Denied (Linux/macOS)**
```bash
chmod +x installers/setup_dev_env.sh
```

**PowerShell Execution Policy (Windows)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Database Connection Error**
- Verify DATABASE_URL in .env.local
- Check Neon database credentials
- Ensure database exists and is accessible

**Missing Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Manual Database Setup
If automated database setup fails:

```python
# Run Python script manually
python installers/init_db.py

# Or create tables manually
from src.models.database import Base, engine
Base.metadata.create_all(bind=engine)
```

## 📞 Support

### Getting Help
- 📖 **Documentation**: See `docs/` directory
- 🐛 **Issues**: Create GitHub issue
- 💬 **Questions**: Use GitHub discussions

### Development Workflow
1. **Feature development**: Create feature branch
2. **Code quality**: Pre-commit hooks run automatically
3. **Testing**: `pytest tests/` before committing
4. **Linting**: `flake8 .` and `black .`
5. **Pull request**: Submit for review

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Updating Pre-commit Hooks
```bash
pre-commit autoupdate
pre-commit install
```

### Database Migrations
```bash
# After model changes
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

---

## 📝 Notes

- **Security**: Never commit `.env.local` or credentials to version control
- **Performance**: Virtual environment improves dependency isolation
- **Compatibility**: Scripts tested on Ubuntu 20.04+, macOS 11+, Windows 10+
- **Updates**: Run setup scripts again to update environment

For more detailed documentation, see the `docs/` directory.