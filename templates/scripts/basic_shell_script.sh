#!/bin/bash
#
# Template Básico para Scripts Shell - AUDITORIA360
# 
# Uso: ./template_basic.sh [opções] [parâmetros]
# Exemplo: ./template_basic.sh --verbose --dry-run
#
# Autor: Equipe AUDITORIA360
# Data: Janeiro 2025
# Versão: 1.0

# Configurações de segurança
set -e          # Sair em caso de erro
set -u          # Sair se variável não definida for usada  
set -o pipefail # Falhar se qualquer comando no pipe falhar

# Configurações de script
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Cores para output (padrão obrigatório)
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Variáveis globais
DRY_RUN=false
VERBOSE=false

# Funções de logging (obrigatórias em todos os scripts)
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

# Função de ajuda (obrigatória)
show_help() {
    cat << EOF
${SCRIPT_NAME} - Template básico para scripts Shell

USO:
    ${SCRIPT_NAME} [OPÇÕES] [ARGUMENTOS]

OPÇÕES:
    -h, --help        Mostra esta ajuda
    -v, --verbose     Modo verboso
    --dry-run         Simula execução sem fazer alterações

EXEMPLOS:
    ${SCRIPT_NAME} --verbose
    ${SCRIPT_NAME} --dry-run

EOF
}

# Função de limpeza (executada ao sair)
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Script finalizado com erro (código: $exit_code)"
    fi
    # Limpeza de arquivos temporários, processos, etc.
    exit $exit_code
}

# Trap para executar cleanup ao sair
trap cleanup EXIT

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se estamos no diretório correto
    if [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
        log_error "Execute o script a partir da raiz do projeto AUDITORIA360"
        exit 1
    fi
    
    # Verificar dependências obrigatórias
    local required_commands=("git" "python3")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Comando obrigatório não encontrado: $cmd"
            exit 1
        fi
    done
    
    log_success "Pré-requisitos validados"
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
            --dry-run)
                DRY_RUN=true
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

# Função principal do script
execute_main_logic() {
    log_info "Executando lógica principal..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN ativo - simulando execução"
    fi
    
    # TODO: Implementar lógica específica do script aqui
    
    log_success "Lógica principal executada com sucesso"
}

# Função principal
main() {
    log_info "Iniciando ${SCRIPT_NAME}..."
    
    parse_arguments "$@"
    validate_prerequisites
    execute_main_logic
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi