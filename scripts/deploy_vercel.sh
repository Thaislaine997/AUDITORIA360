#!/bin/bash

# ================================================================
# Script: deploy_vercel.sh
# Descrição: Script para deploy automatizado na plataforma Vercel
# Uso: ./deploy_vercel.sh [opcoes]
# Autor: AUDITORIA360 Team
# Data: 2024-07-29
# Versão: 2.0.0
# ================================================================

# Configurações globais
set -e                    # Exit on any error
set -u                    # Exit on undefined variable
set -o pipefail          # Exit on pipe failure

# Variáveis globais
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"
readonly LOG_FILE="/tmp/${SCRIPT_NAME}.log"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Cores para output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Variáveis de configuração
PRODUCTION_DEPLOY=false
SKIP_BUILD_CHECK=false
FORCE_DEPLOY=false

# Funções de logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# Função de limpeza (chamada ao sair)
cleanup() {
    log_info "Limpando recursos temporários..."
    # Remove arquivos temporários se necessário
}

# Função de ajuda
show_help() {
    cat << EOF
Uso: $SCRIPT_NAME [OPÇÕES]

DESCRIÇÃO:
    Deploy automatizado do AUDITORIA360 na plataforma Vercel.
    Inclui validações, instalação de dependências e configurações.

OPÇÕES:
    -h, --help           Mostra esta ajuda
    -p, --production     Deploy para produção (padrão: preview)
    -f, --force          Força o deploy mesmo com avisos
    -s, --skip-build     Pula verificação de build local
    -v, --verbose        Modo verboso

EXEMPLOS:
    $SCRIPT_NAME                    # Deploy preview
    $SCRIPT_NAME --production       # Deploy produção
    $SCRIPT_NAME --force            # Força deploy
    $SCRIPT_NAME --verbose          # Modo verboso

NOTAS:
    - Verifica se Vercel CLI está instalado
    - Valida configurações do projeto
    - Executa testes básicos antes do deploy
    - Suporta deploy para preview e produção

EOF
}

# Validação de pré-requisitos
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    # Verificar se Node.js está instalado
    if ! command -v node &> /dev/null; then
        log_error "Node.js não está instalado"
        exit 1
    fi
    
    # Verificar se npm está instalado
    if ! command -v npm &> /dev/null; then
        log_error "npm não está instalado"
        exit 1
    fi
    
    # Verificar se estamos no diretório correto
    if [[ ! -f "$PROJECT_ROOT/vercel.json" ]]; then
        log_error "Arquivo vercel.json não encontrado na raiz do projeto"
        log_info "Execute este script a partir do diretório scripts/"
        exit 1
    fi
    
    log_success "Pré-requisitos básicos atendidos"
}

# Instalar ou verificar Vercel CLI
install_vercel_cli() {
    log_info "Verificando instalação do Vercel CLI..."
    
    if ! command -v vercel &> /dev/null; then
        log_warning "Vercel CLI não encontrado. Instalando..."
        
        if npm install -g vercel; then
            log_success "Vercel CLI instalado com sucesso"
        else
            log_error "Falha ao instalar Vercel CLI"
            exit 1
        fi
    else
        local vercel_version=$(vercel --version)
        log_success "Vercel CLI encontrado: v$vercel_version"
    fi
    
    # Verificar se está logado
    if ! vercel whoami &> /dev/null; then
        log_warning "Não está logado no Vercel"
        log_info "Executando login..."
        vercel login
    else
        local user=$(vercel whoami)
        log_success "Logado como: $user"
    fi
}

# Validar configurações do projeto
validate_project_config() {
    log_info "Validando configurações do projeto..."
    
    cd "$PROJECT_ROOT"
    
    # Verificar arquivos essenciais
    local required_files=("vercel.json" "package.json" "api/index.py")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Arquivo obrigatório não encontrado: $file"
            exit 1
        fi
        log_info "✓ $file encontrado"
    done
    
    # Verificar configuração do vercel.json
    if ! python3 -c "import json; json.load(open('vercel.json'))" 2>/dev/null; then
        log_error "vercel.json contém JSON inválido"
        exit 1
    fi
    
    log_success "Configurações validadas"
}

# Verificar build do projeto
check_project_build() {
    if [[ "$SKIP_BUILD_CHECK" == "true" ]]; then
        log_warning "Pulando verificação de build (--skip-build)"
        return 0
    fi
    
    log_info "Verificando build do projeto..."
    cd "$PROJECT_ROOT"
    
    # Verificar se há package.json para projetos Node.js
    if [[ -f "package.json" ]]; then
        log_info "Verificando dependências Node.js..."
        if [[ ! -d "node_modules" ]]; then
            log_info "Instalando dependências..."
            npm install
        fi
        
        # Verificar se há script de build
        if npm run --silent build &> /dev/null; then
            log_info "Executando build local..."
            npm run build
        fi
    fi
    
    # Verificar dependências Python se houver
    if [[ -f "requirements.txt" ]]; then
        log_info "Verificando dependências Python..."
        if ! python3 -c "import requests" &> /dev/null; then
            log_warning "Algumas dependências Python podem estar ausentes"
        fi
    fi
    
    log_success "Build verificado"
}

# Executar testes básicos
run_basic_tests() {
    log_info "Executando testes básicos..."
    cd "$PROJECT_ROOT"
    
    # Teste de sintaxe Python se houver arquivos .py
    if find . -name "*.py" -not -path "./venv/*" | head -1 | read; then
        log_info "Verificando sintaxe Python..."
        if ! python3 -m py_compile api/index.py; then
            log_error "Erro de sintaxe em api/index.py"
            exit 1
        fi
        log_success "Sintaxe Python OK"
    fi
    
    # Verificar se API básica pode ser importada
    if [[ -f "api/index.py" ]]; then
        log_info "Testando importação da API..."
        if python3 -c "
import sys
sys.path.append('.')
try:
    from api.index import app
    print('API importada com sucesso')
except Exception as e:
    print(f'Erro na importação: {e}')
    sys.exit(1)
"; then
            log_success "API pode ser importada"
        else
            log_error "Falha ao importar API"
            if [[ "$FORCE_DEPLOY" == "false" ]]; then
                exit 1
            else
                log_warning "Continuando devido ao --force"
            fi
        fi
    fi
}

# Executar deploy no Vercel
execute_deploy() {
    log_info "Iniciando deploy no Vercel..."
    cd "$PROJECT_ROOT"
    
    local deploy_args=""
    
    if [[ "$PRODUCTION_DEPLOY" == "true" ]]; then
        deploy_args="--prod"
        log_info "Deploy para PRODUÇÃO"
    else
        log_info "Deploy para PREVIEW"
    fi
    
    # Adicionar flag de confirmação automática
    deploy_args="$deploy_args --yes"
    
    # Executar deploy
    log_info "Executando: vercel $deploy_args"
    
    if vercel $deploy_args; then
        log_success "Deploy executado com sucesso!"
        
        # Obter URL do deploy
        local deploy_url
        if [[ "$PRODUCTION_DEPLOY" == "true" ]]; then
            deploy_url=$(vercel ls --scope=$(vercel whoami) | grep "$(basename "$PROJECT_ROOT")" | head -1 | awk '{print $2}')
        else
            deploy_url="https://$(basename "$PROJECT_ROOT")-preview.vercel.app"
        fi
        
        if [[ -n "$deploy_url" ]]; then
            log_success "URL do deploy: $deploy_url"
        fi
    else
        log_error "Falha no deploy"
        exit 1
    fi
}

# Verificar status do deploy
check_deploy_status() {
    log_info "Verificando status do deploy..."
    
    # Aguardar um momento para o deploy ser processado
    sleep 5
    
    # Listar deployments recentes
    log_info "Deployments recentes:"
    vercel ls --scope=$(vercel whoami) | head -5
    
    log_success "Verificação de status concluída"
}

# Função principal
main() {
    log_info "Iniciando $SCRIPT_NAME..."
    
    # Processar argumentos
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -p|--production)
                PRODUCTION_DEPLOY=true
                shift
                ;;
            -f|--force)
                FORCE_DEPLOY=true
                shift
                ;;
            -s|--skip-build)
                SKIP_BUILD_CHECK=true
                shift
                ;;
            -v|--verbose)
                set -x
                shift
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Configurar trap para cleanup
    trap cleanup EXIT
    
    # Executar validações e deploy
    check_prerequisites
    install_vercel_cli
    validate_project_config
    check_project_build
    run_basic_tests
    execute_deploy
    check_deploy_status
    
    log_success "$SCRIPT_NAME executado com sucesso!"
    
    if [[ "$PRODUCTION_DEPLOY" == "true" ]]; then
        log_warning "Deploy em PRODUÇÃO realizado. Monitore a aplicação."
    else
        log_info "Deploy de preview realizado. Teste antes de promover para produção."
    fi
}

# Executar função principal se script for chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
