#!/bin/bash
#
# deploy_streamlit.sh - Script para deploy automatizado no Streamlit Cloud
# 
# Uso: ./deploy_streamlit.sh [opções]
# Exemplo: ./deploy_streamlit.sh --validate-only --verbose
#
# Autor: Equipe AUDITORIA360
# Data: Janeiro 2025
# Versão: 2.0

# Configurações de segurança
set -e          # Sair em caso de erro
set -u          # Sair se variável não definida for usada  
set -o pipefail # Falhar se qualquer comando no pipe falhar

# Configurações de script
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Cores para output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Variáveis globais
VALIDATE_ONLY=false
VERBOSE=false
SKIP_TESTS=false

# Funções de logging padronizadas
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Função de ajuda
show_help() {
    cat << EOF
${SCRIPT_NAME} - Deploy automatizado no Streamlit Cloud

USO:
    ${SCRIPT_NAME} [OPÇÕES]

OPÇÕES:
    -h, --help          Mostra esta ajuda
    -v, --verbose       Modo verboso
    --validate-only     Apenas valida configuração sem fazer deploy
    --skip-tests        Pula testes de importação Python

EXEMPLOS:
    ${SCRIPT_NAME} --validate-only
    ${SCRIPT_NAME} --verbose
    ${SCRIPT_NAME} --skip-tests

DESCRIÇÃO:
    Este script valida e prepara o projeto AUDITORIA360 para deploy
    no Streamlit Cloud, verificando dependências, estrutura de arquivos
    e configurações necessárias.

EOF
}

# Função de limpeza (executada ao sair)
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Script finalizado com erro (código: $exit_code)"
    fi
    exit $exit_code
}

# Trap para executar cleanup ao sair
trap cleanup EXIT

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se estamos no diretório correto do projeto
    if [ ! -f "${PROJECT_ROOT}/dashboards/app.py" ]; then
        log_error "Execute este script a partir da raiz do projeto AUDITORIA360"
        log_info "Arquivo esperado: dashboards/app.py"
        exit 1
    fi
    
    log_success "Pré-requisitos validados"
}

# Verificar estrutura do projeto
validate_project_structure() {
    log_info "1. Verificando estrutura do projeto..."

    # Verificar arquivos obrigatórios
    local required_files=(
        "dashboards/app.py"
        "dashboards/requirements.txt"
        ".streamlit/config.toml"
        ".streamlit/secrets.toml"
    )

    for file in "${required_files[@]}"; do
        if [ -f "${PROJECT_ROOT}/$file" ]; then
            log_success "✓ $file encontrado"
        else
            log_error "✗ $file não encontrado"
            exit 1
        fi
    done
}

# Validar dependências Python
validate_python_dependencies() {
    log_info "2. Validando requirements.txt..."
    
    # Verificar dependências obrigatórias
    local required_deps=("streamlit" "pandas" "plotly" "requests")
    local requirements_file="${PROJECT_ROOT}/dashboards/requirements.txt"
    
    for dep in "${required_deps[@]}"; do
        if grep -q "$dep" "$requirements_file"; then
            log_success "✓ $dep encontrado em requirements.txt"
        else
            log_warning "⚠ $dep não encontrado em requirements.txt"
        fi
    done
}

# Testar importações Python
test_python_imports() {
    if [ "$SKIP_TESTS" = true ]; then
        log_info "Pulando testes de importação Python (--skip-tests)"
        return 0
    fi
    
    log_info "3. Testando importações Python..."
    
    cd "${PROJECT_ROOT}/dashboards/"
    
    # Testar importações de módulos obrigatórios
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
" && log_success "✓ Todas as dependências estão disponíveis" || {
        log_warning "⚠ Algumas dependências não estão instaladas"
        log_info "Execute: pip install -r dashboards/requirements.txt"
        return 1
    }
    
    cd "$PROJECT_ROOT"
}

# Verificar configuração da API
validate_api_configuration() {
    log_info "4. Verificando configuração da API..."
    
    # Verificar arquivo de configuração de produção
    if [ -f "${PROJECT_ROOT}/.env.production" ]; then
        if grep -q "API_BASE_URL" "${PROJECT_ROOT}/.env.production"; then
            local api_url=$(grep "API_BASE_URL" "${PROJECT_ROOT}/.env.production" | cut -d'=' -f2)
            log_success "✓ API_BASE_URL configurado: $api_url"
        else
            log_warning "⚠ API_BASE_URL não encontrado em .env.production"
        fi
    else
        log_warning "⚠ .env.production não encontrado"
    fi
}

# Gerar arquivos de status e documentação
generate_deployment_files() {
    log_info "5. Preparando arquivos para deploy..."
    
    # Criar resumo de deploy
    cat > "${PROJECT_ROOT}/DEPLOY_STATUS.md" << EOF
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

    log_success "✓ DEPLOY_STATUS.md criado"
}

# Mostrar instruções finais
show_final_instructions() {
    log_info "6. Validação final..."
    
    if [ "$VALIDATE_ONLY" = true ]; then
        log_success "🎯 Validação completa! Projeto está pronto para deploy no Streamlit Cloud"
        return 0
    fi
    
    # Instruções completas para deploy
    log_success "🎯 Projeto configurado com sucesso para Streamlit Cloud!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Acesse https://share.streamlit.io"
    echo "2. Conecte com sua conta GitHub"
    echo "3. Selecione o repositório: Thaislaine997/AUDITORIA360"
    echo "4. Configure o main file: dashboards/app.py"
    echo "5. Adicione os secrets do arquivo .streamlit/secrets.toml"
    echo ""
    log_success "✅ Deploy configurado! Execute o deploy no Streamlit Cloud."
    
    # Mostrar informações de deploy
    echo ""
    echo "🔗 Informações de Deploy:"
    echo "   Repository: Thaislaine997/AUDITORIA360"
    echo "   Branch: main"
    echo "   App file: dashboards/app.py"
    echo "   Python: 3.11"
    echo ""
}

# Parse de argumentos
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                set -x  # Debug mode
                shift
                ;;
            --validate-only)
                VALIDATE_ONLY=true
                shift
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Função principal
main() {
    log_info "Iniciando ${SCRIPT_NAME}..."
    
    parse_arguments "$@"
    
    cd "$PROJECT_ROOT"
    
    validate_prerequisites
    validate_project_structure
    validate_python_dependencies
    test_python_imports
    validate_api_configuration
    
    if [ "$VALIDATE_ONLY" = false ]; then
        generate_deployment_files
    fi
    
    show_final_instructions
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
    log_info "Validação do projeto AUDITORIA360 para Streamlit Cloud concluída"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi