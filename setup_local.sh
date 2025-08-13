#!/bin/bash
# setup_local.sh - AUDITORIA360 Local Development Setup

set -e  # Exit on error

echo "🚀 AUDITORIA360 - Configuração do Ambiente de Desenvolvimento"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running in correct directory
if [ ! -f "README.md" ] || [ ! -d ".git" ]; then
    print_error "Execute este script a partir do diretório raiz do projeto AUDITORIA360"
    exit 1
fi

print_info "Verificando pré-requisitos do sistema..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION encontrado"
else
    print_error "Python 3 não encontrado. Instale Python 3.11 ou superior."
    exit 1
fi

# Check Node.js version
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js $NODE_VERSION encontrado"
else
    print_warning "Node.js não encontrado. Algumas funcionalidades frontend podem não funcionar."
fi

# Check Git
if command -v git &> /dev/null; then
    print_status "Git encontrado"
else
    print_error "Git não encontrado. Instale o Git para continuar."
    exit 1
fi

print_info "Configurando ambiente Python..."

# Create virtual environment
if [ ! -d ".venv" ]; then
    print_info "Criando ambiente virtual Python..."
    python3 -m venv .venv
    print_status "Ambiente virtual criado"
else
    print_status "Ambiente virtual já existe"
fi

# Activate virtual environment
print_info "Ativando ambiente virtual..."
source .venv/bin/activate

# Upgrade pip
print_info "Atualizando pip..."
python -m pip install --upgrade pip

# Install Python dependencies
print_info "Instalando dependências Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependências principais instaladas"
fi

if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    print_status "Dependências de desenvolvimento instaladas"
fi

# Install Node.js dependencies if package.json exists
if [ -f "package.json" ] && command -v npm &> /dev/null; then
    print_info "Instalando dependências Node.js..."
    npm install
    print_status "Dependências Node.js instaladas"
fi

# Setup pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    print_info "Configurando pre-commit hooks..."
    pip install pre-commit
    pre-commit install
    print_status "Pre-commit hooks configurados"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.template" ]; then
        print_info "Criando arquivo .env a partir do template..."
        cp .env.template .env
        print_status "Arquivo .env criado - configure as variáveis necessárias"
    elif [ -f ".env.example" ]; then
        print_info "Criando arquivo .env a partir do exemplo..."
        cp .env.example .env
        print_status "Arquivo .env criado - configure as variáveis necessárias"
    else
        print_info "Criando arquivo .env básico..."
        cat > .env << 'EOF'
# AUDITORIA360 Environment Variables
# Configure these variables for your local environment

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/auditoria360

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Development
DEBUG=true
ENVIRONMENT=development

# Security
SECRET_KEY=your_secret_key_here
EOF
        print_status "Arquivo .env básico criado - configure as variáveis necessárias"
    fi
fi

# Create necessary directories
print_info "Criando estrutura de diretórios..."
mkdir -p logs temp exports data/uploads data/cache

# Set up database (if setup script exists)
if [ -f "setup_database.py" ]; then
    print_info "Executando configuração inicial do banco de dados..."
    python setup_database.py --local
    print_status "Banco de dados configurado"
fi

# Run initial tests
print_info "Executando testes básicos..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short || print_warning "Alguns testes falharam - verifique a configuração"
else
    python -m pytest tests/ -v --tb=short 2>/dev/null || print_warning "Pytest não disponível ou testes falharam"
fi

# Generate development documentation
print_info "Gerando documentação de desenvolvimento..."
cat > DEVELOPMENT.md << 'EOF'
# AUDITORIA360 - Guia de Desenvolvimento Local

Este arquivo foi gerado automaticamente pelo script setup_local.sh

## Ambiente Configurado

- ✅ Python virtual environment (`.venv`)
- ✅ Dependências Python instaladas
- ✅ Arquivo `.env` criado
- ✅ Pre-commit hooks configurados
- ✅ Estrutura de diretórios criada

## Como usar

### 1. Ativar ambiente virtual
```bash
source .venv/bin/activate
```

### 2. Executar a aplicação
```bash
# API Backend
python api/main.py

# Ou usando uvicorn diretamente
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Executar testes
```bash
pytest tests/
```

### 4. Executar linting
```bash
pre-commit run --all-files
```

### 5. Atualizar dependências
```bash
pip install -r requirements.txt
```

## URLs Importantes

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estrutura do Projeto

```
AUDITORIA360/
├── api/              # Backend FastAPI
├── src/              # Código fonte principal
├── frontend/         # Interface React
├── tests/            # Testes automatizados
├── scripts/          # Scripts de automação
├── docs/             # Documentação
├── data/             # Dados e uploads
├── .venv/            # Ambiente virtual Python
└── .env              # Variáveis de ambiente
```

## Próximos Passos

1. Configure as variáveis no arquivo `.env`
2. Execute `source .venv/bin/activate` sempre que trabalhar no projeto
3. Consulte o MANUAL_SUPREMO.md para documentação completa
4. Execute os testes antes de fazer commit
EOF

print_status "Documentação de desenvolvimento criada (DEVELOPMENT.md)"

# Final instructions
echo
echo "🎉 Configuração concluída com sucesso!"
echo "============================================"
print_info "Para começar a trabalhar no projeto:"
echo "  1. source .venv/bin/activate"
echo "  2. Configure as variáveis em .env"
echo "  3. python api/main.py (ou uvicorn api.main:app --reload)"
echo
print_info "Documentação importante:"
echo "  - DEVELOPMENT.md - Guia de desenvolvimento local"
echo "  - MANUAL_SUPREMO.md - Documentação completa do projeto"
echo "  - README.md - Visão geral do projeto"
echo
print_info "URLs de desenvolvimento:"
echo "  - API: http://localhost:8000"
echo "  - Documentação: http://localhost:8000/docs"
echo
print_warning "Lembre-se de configurar as variáveis de ambiente em .env antes de executar!"
echo