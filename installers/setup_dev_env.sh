#!/bin/bash

# AUDITORIA360 - Automated Developer Environment Setup Script
# This script sets up the development environment for AUDITORIA360 project
# Supports Linux and macOS

set -e

echo "🚀 AUDITORIA360 Developer Environment Setup"
echo "=========================================="

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported OS
check_os() {
    case "$(uname -s)" in
        Linux*)     OS=Linux;;
        Darwin*)    OS=Mac;;
        *)          OS="UNKNOWN"
    esac
    
    if [ "$OS" = "UNKNOWN" ]; then
        log_error "Unsupported operating system. Please use Linux or macOS."
        log_info "For Windows, use setup_dev_env.ps1"
        exit 1
    fi
    
    log_info "Detected OS: $OS"
}

# Check if Python 3.8+ is installed
check_python() {
    log_info "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            log_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            log_error "Python 3.8+ required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
}

# Install pip if not available
check_pip() {
    log_info "Checking pip installation..."
    
    if ! command -v pip3 &> /dev/null; then
        log_warning "pip3 not found. Installing..."
        
        if [ "$OS" = "Linux" ]; then
            # Try to install pip using package manager
            if command -v apt-get &> /dev/null; then
                sudo apt-get update && sudo apt-get install -y python3-pip
            elif command -v yum &> /dev/null; then
                sudo yum install -y python3-pip
            else
                log_error "Could not install pip. Please install manually."
                exit 1
            fi
        elif [ "$OS" = "Mac" ]; then
            # Use homebrew if available
            if command -v brew &> /dev/null; then
                brew install python3
            else
                log_error "Please install Homebrew first or install pip manually."
                exit 1
            fi
        fi
    fi
    
    log_success "pip3 is available"
}

# Create virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        log_success "Virtual environment created"
    else
        log_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    log_success "Virtual environment activated"
    
    # Upgrade pip in venv
    pip install --upgrade pip
}

# Install project dependencies
install_dependencies() {
    log_info "Installing project dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Dependencies installed from requirements.txt"
    else
        log_error "requirements.txt not found!"
        exit 1
    fi
    
    # Install development dependencies
    log_info "Installing development dependencies..."
    pip install pytest pytest-cov flake8 black isort pre-commit
    log_success "Development dependencies installed"
}

# Setup environment variables
setup_env_files() {
    log_info "Setting up environment configuration..."
    
    # Create .env.local if it doesn't exist
    if [ ! -f ".env.local" ]; then
        cp .env.example .env.local 2>/dev/null || cat > .env.local << EOF
# AUDITORIA360 Local Development Environment
# Copy this file and adjust the values for your environment

# Database Configuration (Neon PostgreSQL)
DATABASE_URL=postgresql://username:password@host:5432/database_name
NEON_DATABASE_URL=postgresql://username:password@host:5432/database_name

# Cloudflare R2 Configuration
R2_ACCESS_KEY_ID=your_access_key_id
R2_SECRET_ACCESS_KEY=your_secret_access_key
R2_ENDPOINT_URL=https://account_id.r2.cloudflarestorage.com
R2_BUCKET_NAME=auditoria360-bucket

# OpenAI API (for AI features)
OPENAI_API_KEY=your_openai_api_key

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true

# API Configuration
API_HOST=localhost
API_PORT=8000
EOF
        log_success "Created .env.local template"
        log_warning "Please edit .env.local with your actual configuration values"
    else
        log_warning ".env.local already exists"
    fi
}

# Setup pre-commit hooks
setup_pre_commit() {
    log_info "Setting up pre-commit hooks..."
    
    if [ -f ".pre-commit-config.yaml" ]; then
        pre-commit install
        log_success "Pre-commit hooks installed"
    else
        # Create basic pre-commit config
        cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
EOF
        pre-commit install
        log_success "Pre-commit configuration created and installed"
    fi
}

# Initialize database (if possible)
init_database() {
    log_info "Checking database initialization..."
    
    # Try to run database initialization if we have the script
    if [ -f "scripts/init_db.py" ]; then
        log_info "Running database initialization..."
        python scripts/init_db.py
        log_success "Database initialized"
    else
        log_warning "Database initialization script not found"
        log_info "You may need to run database setup manually"
    fi
}

# Test installation
test_installation() {
    log_info "Testing installation..."
    
    # Test imports
    python -c "
import fastapi
import sqlalchemy
import duckdb
import paddleocr
import prefect
print('✅ All major dependencies imported successfully')
" && log_success "Dependency test passed" || log_error "Dependency test failed"

    # Test API startup (dry run)
    if [ -f "api/index.py" ]; then
        python -c "
from api.index import app
print('✅ FastAPI app loads successfully')
" && log_success "API test passed" || log_warning "API test failed - check configuration"
    fi
}

# Print final instructions
print_final_instructions() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "Next steps:"
    echo "1. Edit .env.local with your actual configuration values"
    echo "2. Set up your Neon PostgreSQL database"
    echo "3. Configure Cloudflare R2 storage"
    echo "4. Activate the virtual environment: source venv/bin/activate"
    echo "5. Start the development server: make run"
    echo ""
    echo "Useful commands:"
    echo "• Run tests: make test"
    echo "• Run linting: make lint"
    echo "• Start API server: uvicorn api.index:app --reload"
    echo ""
    echo "📚 Documentation: docs/"
    echo "🐛 Issues: Check GitHub issues"
    echo ""
}

# Main installation flow
main() {
    echo "Starting automated setup..."
    
    check_os
    check_python
    check_pip
    setup_venv
    install_dependencies
    setup_env_files
    setup_pre_commit
    init_database
    test_installation
    print_final_instructions
    
    log_success "AUDITORIA360 development environment setup completed!"
}

# Run main function
main "$@"