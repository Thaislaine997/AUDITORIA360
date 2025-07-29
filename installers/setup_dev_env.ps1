# AUDITORIA360 - Automated Developer Environment Setup Script (PowerShell)
# This script sets up the development environment for AUDITORIA360 project on Windows

param(
    [switch]$SkipPython,
    [switch]$SkipGit,
    [switch]$VerboseOutput
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Color functions for output
function Write-Info {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Install-Chocolatey {
    Write-Info "Installing Chocolatey package manager..."
    
    if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Success "Chocolatey installed successfully"
    } else {
        Write-Warning "Chocolatey already installed"
    }
}

function Install-Python {
    if ($SkipPython) {
        Write-Info "Skipping Python installation (--SkipPython flag)"
        return
    }
    
    Write-Info "Checking Python installation..."
    
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion -match "Python 3\.([8-9]|\d{2})") {
            Write-Success "Python $pythonVersion found"
            return
        }
    } catch {
        # Python not found or wrong version
    }
    
    Write-Info "Installing Python 3.11..."
    choco install python311 -y
    
    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Success "Python 3.11 installed"
}

function Install-Git {
    if ($SkipGit) {
        Write-Info "Skipping Git installation (--SkipGit flag)"
        return
    }
    
    Write-Info "Checking Git installation..."
    
    if (!(Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Info "Installing Git..."
        choco install git -y
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Success "Git installed"
    } else {
        Write-Success "Git already installed"
    }
}

function Setup-VirtualEnvironment {
    Write-Info "Setting up Python virtual environment..."
    
    if (!(Test-Path "venv")) {
        python -m venv venv
        Write-Success "Virtual environment created"
    } else {
        Write-Warning "Virtual environment already exists"
    }
    
    # Activate virtual environment
    & ".\venv\Scripts\Activate.ps1"
    Write-Success "Virtual environment activated"
    
    # Upgrade pip
    python -m pip install --upgrade pip
}

function Install-Dependencies {
    Write-Info "Installing project dependencies..."
    
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
        Write-Success "Dependencies installed from requirements.txt"
    } else {
        Write-Error "requirements.txt not found!"
        exit 1
    }
    
    # Install development dependencies
    Write-Info "Installing development dependencies..."
    pip install pytest pytest-cov flake8 black isort pre-commit
    Write-Success "Development dependencies installed"
}

function Setup-EnvironmentFiles {
    Write-Info "Setting up environment configuration..."
    
    if (!(Test-Path ".env.local")) {
        $envContent = @"
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
"@
        $envContent | Out-File -FilePath ".env.local" -Encoding UTF8
        Write-Success "Created .env.local template"
        Write-Warning "Please edit .env.local with your actual configuration values"
    } else {
        Write-Warning ".env.local already exists"
    }
}

function Setup-PreCommitHooks {
    Write-Info "Setting up pre-commit hooks..."
    
    if (!(Test-Path ".pre-commit-config.yaml")) {
        $preCommitConfig = @"
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
"@
        $preCommitConfig | Out-File -FilePath ".pre-commit-config.yaml" -Encoding UTF8
        Write-Success "Pre-commit configuration created"
    }
    
    pre-commit install
    Write-Success "Pre-commit hooks installed"
}

function Initialize-Database {
    Write-Info "Checking database initialization..."
    
    if (Test-Path "scripts\init_db.py") {
        Write-Info "Running database initialization..."
        python scripts\init_db.py
        Write-Success "Database initialized"
    } else {
        Write-Warning "Database initialization script not found"
        Write-Info "You may need to run database setup manually"
    }
}

function Test-Installation {
    Write-Info "Testing installation..."
    
    try {
        python -c @"
import fastapi
import sqlalchemy
import duckdb
import paddleocr
import prefect
print('✅ All major dependencies imported successfully')
"@
        Write-Success "Dependency test passed"
    } catch {
        Write-Error "Dependency test failed"
    }
    
    if (Test-Path "api\index.py") {
        try {
            python -c @"
from api.index import app
print('✅ FastAPI app loads successfully')
"@
            Write-Success "API test passed"
        } catch {
            Write-Warning "API test failed - check configuration"
        }
    }
}

function Show-FinalInstructions {
    Write-Host ""
    Write-Host "🎉 Setup Complete!" -ForegroundColor Green
    Write-Host "=================="
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. Edit .env.local with your actual configuration values"
    Write-Host "2. Set up your Neon PostgreSQL database"
    Write-Host "3. Configure Cloudflare R2 storage"
    Write-Host "4. Activate the virtual environment: .\venv\Scripts\Activate.ps1"
    Write-Host "5. Start the development server: make run"
    Write-Host ""
    Write-Host "Useful commands:"
    Write-Host "• Run tests: make test"
    Write-Host "• Run linting: make lint"
    Write-Host "• Start API server: uvicorn api.index:app --reload"
    Write-Host ""
    Write-Host "📚 Documentation: docs\"
    Write-Host "🐛 Issues: Check GitHub issues"
    Write-Host ""
}

# Main execution
function Main {
    Write-Host "🚀 AUDITORIA360 Developer Environment Setup" -ForegroundColor Cyan
    Write-Host "==========================================="
    
    # Check if running as administrator
    if (!(Test-Administrator)) {
        Write-Warning "Running without administrator privileges. Some installations may fail."
        Write-Info "Consider running PowerShell as Administrator for best results."
    }
    
    try {
        Install-Chocolatey
        Install-Python
        Install-Git
        Setup-VirtualEnvironment
        Install-Dependencies
        Setup-EnvironmentFiles
        Setup-PreCommitHooks
        Initialize-Database
        Test-Installation
        Show-FinalInstructions
        
        Write-Success "AUDITORIA360 development environment setup completed!"
    } catch {
        Write-Error "Setup failed: $($_.Exception.Message)"
        exit 1
    }
}

# Run main function
Main