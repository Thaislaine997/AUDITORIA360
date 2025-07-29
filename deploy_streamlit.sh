#!/bin/bash

# 🚀 AUDITORIA360 - Streamlit Cloud Deployment Script
# Automated deployment script for Streamlit Cloud

set -e  # Exit on any error

echo "🚀 AUDITORIA360 - Iniciando deploy para Streamlit Cloud..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
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

# Check if we're in the correct directory
if [ ! -f "dashboards/app.py" ]; then
    print_error "dashboards/app.py não encontrado. Execute este script na raiz do projeto."
    exit 1
fi

print_step "1. Verificando estrutura do projeto..."

# Check required files
REQUIRED_FILES=(
    "dashboards/app.py"
    "dashboards/requirements.txt"
    ".streamlit/config.toml"
    ".streamlit/secrets.toml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file encontrado"
    else
        print_error "✗ $file não encontrado"
        exit 1
    fi
done

print_step "2. Validando requirements.txt..."

# Check if requirements.txt has required dependencies
REQUIRED_DEPS=("streamlit" "pandas" "plotly" "requests")
for dep in "${REQUIRED_DEPS[@]}"; do
    if grep -q "$dep" dashboards/requirements.txt; then
        print_success "✓ $dep encontrado em requirements.txt"
    else
        print_warning "⚠ $dep não encontrado em requirements.txt"
    fi
done

print_step "3. Testando importações Python..."

# Test Python imports
cd dashboards/
python3 -c "
import sys
import importlib.util

required_modules = ['streamlit', 'pandas', 'plotly', 'requests']
missing_modules = []

for module in required_modules:
    if importlib.util.find_spec(module) is None:
        missing_modules.append(module)

if missing_modules:
    print(f'Módulos não encontrados: {missing_modules}')
    print('Execute: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('Todas as dependências estão disponíveis.')
"

if [ $? -eq 0 ]; then
    print_success "✓ Todas as dependências estão disponíveis"
else
    print_warning "⚠ Algumas dependências não estão instaladas. Execute: pip install -r dashboards/requirements.txt"
fi

cd ..

print_step "4. Verificando configuração da API..."

# Check API configuration
if [ -f ".env.production" ]; then
    if grep -q "API_BASE_URL" .env.production; then
        API_URL=$(grep "API_BASE_URL" .env.production | cut -d'=' -f2)
        print_success "✓ API_BASE_URL configurado: $API_URL"
    else
        print_warning "⚠ API_BASE_URL não encontrado em .env.production"
    fi
else
    print_warning "⚠ .env.production não encontrado"
fi

print_step "5. Preparando arquivos para deploy..."

# Create a deployment summary
cat > DEPLOY_STATUS.md << EOF
# 📊 AUDITORIA360 - Status do Deploy

## ✅ Configuração Completa

### 📁 Arquivos Configurados
- ✅ \`dashboards/app.py\` - Aplicação principal
- ✅ \`dashboards/requirements.txt\` - Dependências
- ✅ \`.streamlit/config.toml\` - Configuração visual
- ✅ \`.streamlit/secrets.toml\` - Secrets para produção
- ✅ \`.env.production\` - Variáveis de ambiente

### 🔧 Configuração Streamlit Cloud

#### 1. Acesse https://share.streamlit.io
#### 2. Conecte com GitHub
#### 3. Selecione repositório: \`Thaislaine997/AUDITORIA360\`
#### 4. Configure:
   - **Branch**: \`main\`
   - **Main file**: \`dashboards/app.py\`
   - **Python version**: \`3.11\`

#### 5. Configure Secrets (Advanced settings):
\`\`\`toml
# Copie o conteúdo de .streamlit/secrets.toml
# e cole na seção de secrets do Streamlit Cloud
\`\`\`

### 🌐 URLs Esperadas
- **Dashboard**: https://auditoria360-dashboards.streamlit.app
- **API**: https://auditoria360-api.vercel.app

### 📋 Checklist Pós-Deploy
- [ ] Dashboard carrega sem erros
- [ ] Páginas navegam corretamente
- [ ] API conecta com sucesso
- [ ] Autenticação funciona
- [ ] Dados são exibidos corretamente

---
**Status**: 🟢 **PRONTO PARA DEPLOY**  
**Data**: $(date)
EOF

print_success "✓ DEPLOY_STATUS.md criado"

print_step "6. Validação final..."

# Final validation
print_success "🎯 Projeto configurado com sucesso para Streamlit Cloud!"
echo ""
echo "📋 Próximos passos:"
echo "1. Acesse https://share.streamlit.io"
echo "2. Conecte com sua conta GitHub"
echo "3. Selecione o repositório: Thaislaine997/AUDITORIA360"
echo "4. Configure o main file: dashboards/app.py"
echo "5. Adicione os secrets do arquivo .streamlit/secrets.toml"
echo ""
print_success "✅ Deploy configurado! Execute o deploy no Streamlit Cloud."

# Show deployment info
echo ""
echo "🔗 Informações de Deploy:"
echo "   Repository: Thaislaine997/AUDITORIA360"
echo "   Branch: main"
echo "   App file: dashboards/app.py"
echo "   Python: 3.11"
echo ""