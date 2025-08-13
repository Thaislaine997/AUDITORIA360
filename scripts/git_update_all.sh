#!/bin/bash
#
# git_update_all.sh - Script para commit e push automático das alterações
# 
# Uso: ./git_update_all.sh [mensagem_do_commit]
# Exemplo: ./git_update_all.sh "Correções de bugs e melhorias"
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
${SCRIPT_NAME} - Commit e push automático das alterações

USO:
    ${SCRIPT_NAME} [OPÇÕES] [MENSAGEM_DO_COMMIT]

OPÇÕES:
    -h, --help        Mostra esta ajuda
    -v, --verbose     Modo verboso
    --dry-run         Simula execução sem fazer alterações
    --force          Força o push mesmo com arquivos sensíveis

EXEMPLOS:
    ${SCRIPT_NAME} "Correções de bugs"
    ${SCRIPT_NAME} --dry-run
    ${SCRIPT_NAME} --verbose "Nova funcionalidade de auditoria"

EOF
}

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se estamos em um repositório Git
    if [ ! -d "${PROJECT_ROOT}/.git" ]; then
        log_error "Não está em um repositório Git válido"
        exit 1
    fi
    
    # Verificar se git está disponível
    if ! command -v git &> /dev/null; then
        log_error "Git não encontrado no sistema"
        exit 1
    fi
    
    # Verificar se há configuração de usuário Git
    if ! git config user.name &> /dev/null || ! git config user.email &> /dev/null; then
        log_error "Configuração de usuário Git não encontrada"
        log_info "Configure com: git config --global user.name 'Seu Nome'"
        log_info "Configure com: git config --global user.email 'seu@email.com'"
        exit 1
    fi
    
    log_success "Pré-requisitos validados"
}

# Verificar arquivos sensíveis
check_sensitive_files() {
    log_info "Verificando arquivos sensíveis..."
    
    local sensitive_patterns=(
        "*.key"
        "*.pem"
        "*.p12"
        "*.env"
        "*.secret"
        "*password*"
        "*credential*"
        "config/production/*"
    )
    
    local found_sensitive=false
    
    for pattern in "${sensitive_patterns[@]}"; do
        if git diff --cached --name-only | grep -q "$pattern" 2>/dev/null; then
            log_warning "Arquivo potencialmente sensível encontrado: $pattern"
            found_sensitive=true
        fi
    done
    
    if [ "$found_sensitive" = true ] && [ "${FORCE:-false}" != true ]; then
        log_error "Arquivos sensíveis detectados. Use --force para ignorar ou remova-os do commit"
        log_info "Para remover: git reset HEAD <arquivo>"
        exit 1
    fi
}

# Verificar status do repositório
check_repository_status() {
    log_info "Verificando status do repositório..."
    
    # Verificar se há mudanças para commit
    if git diff --quiet && git diff --cached --quiet; then
        log_warning "Nenhuma alteração detectada para commit"
        return 1
    fi
    
    # Verificar se estamos na branch correta
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
        log_warning "Você está na branch principal ($current_branch)"
        log_info "Considerado usar uma branch de feature para desenvolvimento"
    fi
    
    # Verificar se há conflitos não resolvidos
    if git ls-files -u | grep -q .; then
        log_error "Há conflitos de merge não resolvidos"
        exit 1
    fi
    
    log_success "Status do repositório verificado"
}

# Executar commit e push
execute_git_operations() {
    local commit_message="$1"
    local dry_run="$2"
    
    if [ "$dry_run" = true ]; then
        log_warning "Modo DRY-RUN ativo - simulando operações Git"
        log_info "Seria executado: git add ."
        log_info "Seria executado: git commit -m \"$commit_message\""
        log_info "Seria executado: git push"
        return 0
    fi
    
    log_info "Adicionando arquivos ao stage..."
    git add .
    
    log_info "Criando commit..."
    git commit -m "$commit_message"
    
    log_info "Fazendo push para repositório remoto..."
    git push
    
    log_success "Operações Git executadas com sucesso"
}

# Função principal
main() {
    local commit_message="Atualização geral: configs, automações e dependências"
    local dry_run=false
    local verbose=false
    local force=false
    
    # Parse de argumentos
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                set -x  # Debug mode
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --force)
                force=true
                export FORCE=true
                shift
                ;;
            -*)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
            *)
                # Mensagem do commit como argumento posicional
                commit_message="$1"
                shift
                ;;
        esac
    done
    
    log_info "Iniciando ${SCRIPT_NAME}..."
    
    cd "$PROJECT_ROOT"
    
    validate_prerequisites
    
    if ! check_repository_status; then
        log_info "Nada para fazer. Saindo..."
        exit 0
    fi
    
    check_sensitive_files
    execute_git_operations "$commit_message" "$dry_run"
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
    log_info "Commit: $commit_message"
    log_info "Branch: $(git branch --show-current)"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
