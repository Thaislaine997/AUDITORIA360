#!/bin/bash
#
# deploy_vercel.sh - Script para deploy automatizado na Vercel
# 
# Uso: ./deploy_vercel.sh [opções]
# Exemplo: ./deploy_vercel.sh --production --verbose
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
PRODUCTION=false
DRY_RUN=false
VERBOSE=false

# Funções de logging
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
${SCRIPT_NAME} - Deploy automatizado na Vercel

USO:
    ${SCRIPT_NAME} [OPÇÕES]

OPÇÕES:
    -h, --help        Mostra esta ajuda
    -v, --verbose     Modo verboso
    -p, --production  Deploy para produção (padrão: preview)
    --dry-run         Simula execução sem fazer deploy
    --force          Força deploy mesmo com warnings

EXEMPLOS:
    ${SCRIPT_NAME} --production
    ${SCRIPT_NAME} --dry-run
    ${SCRIPT_NAME} --verbose

AMBIENTES:
    preview      Deploy de preview (padrão)
    production   Deploy de produção (--production)

EOF
}

# Função de limpeza (executada ao sair)
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Deploy finalizado com erro (código: $exit_code)"
    fi
    # Limpeza de arquivos temporários se necessário
    exit $exit_code
}

# Trap para executar cleanup ao sair
trap cleanup EXIT

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se estamos no diretório correto do projeto
    if [ ! -f "${PROJECT_ROOT}/package.json" ] && [ ! -f "${PROJECT_ROOT}/vercel.json" ]; then
        log_error "Execute o script a partir da raiz do projeto AUDITORIA360"
        log_info "Arquivos esperados: package.json ou vercel.json"
        exit 1
    fi
    
    # Verificar se Vercel CLI está instalado
    if ! command -v vercel &> /dev/null; then
        log_warning "Vercel CLI não encontrado. Instalando..."
        
        # Verificar se npm está disponível
        if ! command -v npm &> /dev/null; then
            log_error "npm não encontrado. Instale Node.js primeiro"
            exit 1
        fi
        
        # Instalar Vercel CLI globalmente
        npm install -g vercel
        
        # Verificar instalação
        if ! command -v vercel &> /dev/null; then
            log_error "Falha na instalação do Vercel CLI"
            exit 1
        fi
        
        log_success "Vercel CLI instalado com sucesso"
    else
        log_success "Vercel CLI encontrado"
    fi
    
    # Verificar se usuário está logado na Vercel
    if ! vercel whoami &> /dev/null; then
        log_warning "Usuário não está logado na Vercel"
        log_info "Execute 'vercel login' para fazer login"
        
        if [ "$DRY_RUN" = false ]; then
            log_info "Iniciando processo de login..."
            vercel login
        fi
    else
        local vercel_user=$(vercel whoami)
        log_success "Logado na Vercel como: $vercel_user"
    fi
    
    log_success "Pré-requisitos validados"
}

# Verificar configuração do projeto
validate_project_config() {
    log_info "Validando configuração do projeto..."
    
    # Verificar se há configuração da Vercel
    if [ -f "${PROJECT_ROOT}/vercel.json" ]; then
        log_success "Arquivo vercel.json encontrado"
        
        # Verificar sintaxe JSON básica
        if ! python3 -m json.tool "${PROJECT_ROOT}/vercel.json" &> /dev/null; then
            log_error "Arquivo vercel.json contém JSON inválido"
            exit 1
        fi
    else
        log_warning "Arquivo vercel.json não encontrado - usando configuração padrão"
    fi
    
    # Verificar variáveis de ambiente necessárias
    if [ -f "${PROJECT_ROOT}/.env.production" ] && [ "$PRODUCTION" = true ]; then
        log_success "Arquivo .env.production encontrado"
    elif [ -f "${PROJECT_ROOT}/.env.local" ]; then
        log_success "Arquivo .env.local encontrado"
    else
        log_warning "Nenhum arquivo de ambiente encontrado"
    fi
    
    log_success "Configuração do projeto validada"
}

# Executar build local (se necessário)
run_build() {
    log_info "Verificando necessidade de build local..."
    
    if [ -f "${PROJECT_ROOT}/package.json" ]; then
        # Verificar se há script de build
        if grep -q '"build"' "${PROJECT_ROOT}/package.json"; then
            log_info "Script de build encontrado - executando build local..."
            
            cd "$PROJECT_ROOT"
            
            if [ "$DRY_RUN" = true ]; then
                log_warning "Modo DRY-RUN: build seria executado"
            else
                npm run build
                log_success "Build local executado com sucesso"
            fi
        else
            log_info "Nenhum script de build encontrado"
        fi
    fi
}

# Executar deploy na Vercel
execute_deploy() {
    log_info "Iniciando deploy na Vercel..."
    
    cd "$PROJECT_ROOT"
    
    # Preparar comando de deploy
    local deploy_cmd="vercel"
    
    if [ "$PRODUCTION" = true ]; then
        deploy_cmd="$deploy_cmd --prod"
        log_info "Fazendo deploy para PRODUÇÃO"
    else
        log_info "Fazendo deploy para PREVIEW"
    fi
    
    # Adicionar flag de confirmação automática
    deploy_cmd="$deploy_cmd --confirm"
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN ativo - comando que seria executado:"
        log_info "$deploy_cmd"
        return 0
    fi
    
    # Executar deploy
    log_info "Executando: $deploy_cmd"
    
    if $deploy_cmd; then
        log_success "Deploy executado com sucesso!"
        
        # Obter URL do deploy
        local deploy_url=$(vercel ls --limit 1 --format json | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data and len(data) > 0:
    print(f'https://{data[0][\"url\"]}')
" 2>/dev/null || echo "URL não disponível")
        
        if [ "$deploy_url" != "URL não disponível" ]; then
            log_success "URL do deploy: $deploy_url"
        fi
        
    else
        log_error "Falha no deploy da Vercel"
        exit 1
    fi
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
            -p|--production)
                PRODUCTION=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --force)
                # Para compatibilidade futura
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
    validate_project_config
    run_build
    execute_deploy
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
    
    if [ "$PRODUCTION" = true ]; then
        log_info "Deploy de PRODUÇÃO realizado"
    else
        log_info "Deploy de PREVIEW realizado"
    fi
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
