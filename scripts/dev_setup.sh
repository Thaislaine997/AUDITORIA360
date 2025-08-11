#!/bin/bash

# AUDITORIA360 - Development Environment Setup Script
# Configura ambiente de desenvolvimento local

set -e  # Exit on any error

echo "🔧 AUDITORIA360 - Setup Ambiente de Desenvolvimento"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
    OS="windows"
else
    print_warning "Sistema operacional não reconhecido: $OSTYPE"
    OS="unknown"
fi

print_status "Detectado sistema operacional: $OS"

# Check Python version
print_status "Verificando versão do Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -eq "3" ] && [ "$PYTHON_MINOR" -ge "10" ]; then
        print_success "Python $PYTHON_VERSION detectado ✓"
        PYTHON_CMD="python3"
    else
        print_error "Python 3.10+ é necessário. Versão encontrada: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 não encontrado. Por favor, instale Python 3.10+"
    exit 1
fi

# Check Node.js version
print_status "Verificando versão do Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
    
    if [ "$NODE_MAJOR" -ge "18" ]; then
        print_success "Node.js $NODE_VERSION detectado ✓"
    else
        print_warning "Node.js 18+ recomendado. Versão encontrada: $NODE_VERSION"
    fi
else
    print_warning "Node.js não encontrado. Recomendado para desenvolvimento frontend"
fi

# Create .env file if it doesn't exist
print_status "Configurando variáveis de ambiente..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Arquivo .env criado a partir de .env.example"
        print_warning "Por favor, configure as variáveis de ambiente em .env"
    else
        print_warning "Arquivo .env.example não encontrado"
        # Create basic .env file
        cat > .env << EOF
# AUDITORIA360 Development Environment
ENVIRONMENT=development
DEBUG=true

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/auditoria360_dev
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# AI/ML Configuration
OPENAI_API_KEY=your_openai_key

# Storage Configuration
CLOUDFLARE_R2_ACCESS_KEY=your_r2_access_key
CLOUDFLARE_R2_SECRET_KEY=your_r2_secret_key
CLOUDFLARE_R2_BUCKET=your_r2_bucket

# Application Configuration
SECRET_KEY=dev_secret_key_change_in_production
API_BASE_URL=http://localhost:8001
FRONTEND_URL=http://localhost:5173

# Monitoring Configuration
HEALTH_CHECK_INTERVAL=300
METRICS_COLLECTION_ENABLED=true
EOF
        print_success "Arquivo .env básico criado"
        print_warning "Configure as variáveis de ambiente em .env antes de prosseguir"
    fi
else
    print_success "Arquivo .env já existe ✓"
fi

# Create virtual environment
print_status "Configurando ambiente virtual Python..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    print_success "Ambiente virtual criado ✓"
else
    print_success "Ambiente virtual já existe ✓"
fi

# Activate virtual environment
print_status "Ativando ambiente virtual..."
source venv/bin/activate

# Upgrade pip
print_status "Atualizando pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Instalando dependências Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependências Python instaladas ✓"
else
    print_error "Arquivo requirements.txt não encontrado"
    exit 1
fi

# Install development dependencies if available
if [ -f "requirements-dev.txt" ]; then
    print_status "Instalando dependências de desenvolvimento..."
    pip install -r requirements-dev.txt
    print_success "Dependências de desenvolvimento instaladas ✓"
fi

# Install Node.js dependencies for frontend
if [ -d "src/frontend" ] && command -v npm &> /dev/null; then
    print_status "Instalando dependências do frontend..."
    cd src/frontend
    npm install
    cd ../..
    print_success "Dependências do frontend instaladas ✓"
elif [ -f "package.json" ] && command -v npm &> /dev/null; then
    print_status "Instalando dependências Node.js..."
    npm install
    print_success "Dependências Node.js instaladas ✓"
fi

# Setup database (if script exists)
if [ -f "setup_database.py" ]; then
    print_status "Configurando banco de dados..."
    $PYTHON_CMD setup_database.py
    print_success "Banco de dados configurado ✓"
fi

# Setup pre-commit hooks if available
if [ -f ".pre-commit-config.yaml" ] && command -v pre-commit &> /dev/null; then
    print_status "Configurando hooks pre-commit..."
    pre-commit install
    print_success "Hooks pre-commit configurados ✓"
elif pip list | grep -q pre-commit; then
    print_status "Configurando hooks pre-commit..."
    pre-commit install
    print_success "Hooks pre-commit configurados ✓"
fi

# Create necessary directories
print_status "Criando diretórios necessários..."
mkdir -p logs
mkdir -p temp
mkdir -p uploads
mkdir -p reports
print_success "Diretórios criados ✓"

# Set permissions
print_status "Configurando permissões..."
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x automation/*.py 2>/dev/null || true
print_success "Permissões configuradas ✓"

# Run health check
print_status "Executando verificação de saúde..."
if [ -f "automation/update_status.py" ]; then
    $PYTHON_CMD automation/update_status.py
    print_success "Verificação de saúde concluída ✓"
fi

echo ""
echo "=========================================="
print_success "🎉 Setup de desenvolvimento concluído!"
echo "=========================================="
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Configure as variáveis de ambiente em .env"
echo "2. Ative o ambiente virtual: source venv/bin/activate"
echo "3. Execute o servidor de desenvolvimento:"
echo "   - Backend: python -m uvicorn src.main:app --reload --port 8001"
echo "   - Frontend: cd src/frontend && npm run dev"
echo ""
echo "🔗 URLs úteis:"
echo "   - API: http://localhost:8001"
echo "   - Frontend: http://localhost:5173" 
echo "   - API Docs: http://localhost:8001/docs"
echo "   - Health Status: http://localhost:8001/api/health/status"
echo ""
echo "📚 Comandos úteis:"
echo "   - make run          # Executar servidor"
echo "   - make test         # Executar testes"
echo "   - make lint         # Verificar código"
echo "   - make format       # Formatar código"
echo ""
print_success "Desenvolvimento configurado com sucesso! 🚀"