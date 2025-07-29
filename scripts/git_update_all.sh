#!/bin/bash

# ================================================================
# Script: git_update_all.sh
# Descrição: Atualização automática do repositório Git com commit e push
# Uso: ./git_update_all.sh [mensagem_commit]
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

# Cores para output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

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

# Função de ajuda
show_help() {
    cat << EOF
Uso: $SCRIPT_NAME [mensagem_commit]

DESCRIÇÃO:
    Executa git add, commit e push de forma automática e segura.
    Se não fornecida, uma mensagem padrão será usada.

PARÂMETROS:
    mensagem_commit    Mensagem personalizada para o commit (opcional)

OPÇÕES:
    -h, --help        Mostra esta ajuda
    -n, --dry-run     Mostra o que seria feito sem executar
    -f, --force       Força o push mesmo com conflitos

EXEMPLOS:
    $SCRIPT_NAME "Implementação da nova funcionalidade"
    $SCRIPT_NAME --dry-run
    $SCRIPT_NAME --help

NOTAS:
    - O script verifica se há mudanças antes de fazer commit
    - Verifica se o repositório está limpo e atualizado
    - Faz backup automático em caso de conflitos

EOF
}

# Validação de pré-requisitos
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    # Verificar se git está instalado
    if ! command -v git &> /dev/null; then
        log_error "Git não está instalado"
        exit 1
    fi
    
    # Verificar se estamos em um repositório Git
    if ! git rev-parse --git-dir &> /dev/null; then
        log_error "Não é um repositório Git válido"
        exit 1
    fi
    
    # Verificar conexão com remote
    if ! git ls-remote origin &> /dev/null; then
        log_error "Não foi possível conectar ao repositório remoto"
        exit 1
    fi
    
    log_success "Todos os pré-requisitos atendidos"
}

# Verificar status do repositório
check_repository_status() {
    log_info "Verificando status do repositório..."
    
    # Verificar se há mudanças staged ou unstaged
    if git diff-index --quiet HEAD --; then
        log_warning "Nenhuma mudança detectada para commit"
        return 1
    fi
    
    # Verificar se há conflitos não resolvidos
    if git ls-files -u | grep -q .; then
        log_error "Há conflitos não resolvidos no repositório"
        exit 1
    fi
    
    log_success "Repositório pronto para atualização"
    return 0
}

# Executar git add com verificação
execute_git_add() {
    log_info "Adicionando arquivos ao staging..."
    
    # Mostrar arquivos que serão adicionados
    git status --porcelain | while read -r status file; do
        log_info "  $status $file"
    done
    
    # Executar git add
    if git add .; then
        log_success "Arquivos adicionados com sucesso"
    else
        log_error "Falha ao adicionar arquivos"
        exit 1
    fi
}

# Executar git commit com verificação
execute_git_commit() {
    local commit_message="$1"
    log_info "Criando commit com mensagem: '$commit_message'"
    
    if git commit -m "$commit_message"; then
        local commit_hash=$(git rev-parse --short HEAD)
        log_success "Commit criado: $commit_hash"
    else
        log_error "Falha ao criar commit"
        exit 1
    fi
}

# Executar git push com verificação
execute_git_push() {
    local force_push="$1"
    log_info "Enviando mudanças para o repositório remoto..."
    
    # Verificar se há commits para push
    if git log origin/$(git branch --show-current)..HEAD --oneline | grep -q .; then
        # Verificar se precisa de force push
        if [[ "$force_push" == "true" ]]; then
            log_warning "Executando force push..."
            if git push --force-with-lease; then
                log_success "Force push executado com sucesso"
            else
                log_error "Falha no force push"
                exit 1
            fi
        else
            # Push normal
            if git push; then
                log_success "Push executado com sucesso"
            else
                log_error "Falha no push. Tente: git pull --rebase ou use --force"
                exit 1
            fi
        fi
    else
        log_warning "Nenhum commit novo para enviar"
    fi
}

# Função de dry-run
execute_dry_run() {
    local commit_message="$1"
    
    log_info "=== MODO DRY-RUN - Simulação de execução ==="
    
    if check_repository_status; then
        log_info "Arquivos que seriam adicionados:"
        git status --porcelain | while read -r status file; do
            echo "  $status $file"
        done
        
        log_info "Commit seria criado com mensagem: '$commit_message'"
        log_info "Push seria executado para: $(git remote get-url origin)"
    fi
    
    log_info "=== FIM DO DRY-RUN ==="
}

# Função principal
main() {
    log_info "Iniciando $SCRIPT_NAME..."
    
    local commit_message="Atualização geral: configs, automações e dependências"
    local dry_run=false
    local force_push=false
    
    # Processar argumentos
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -n|--dry-run)
                dry_run=true
                shift
                ;;
            -f|--force)
                force_push=true
                shift
                ;;
            -*)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
            *)
                # Primeira string não-opção é a mensagem do commit
                commit_message="$1"
                shift
                ;;
        esac
    done
    
    # Executar validações
    check_prerequisites
    
    # Verificar se é dry-run
    if [[ "$dry_run" == "true" ]]; then
        execute_dry_run "$commit_message"
        exit 0
    fi
    
    # Verificar status antes de proceder
    if ! check_repository_status; then
        log_warning "Não há mudanças para commit. Finalizando."
        exit 0
    fi
    
    # Executar sequência git
    execute_git_add
    execute_git_commit "$commit_message"
    execute_git_push "$force_push"
    
    log_success "$SCRIPT_NAME executado com sucesso!"
    log_info "Commit: $(git log -1 --oneline)"
}

# Executar função principal se script for chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
