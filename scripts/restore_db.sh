#!/bin/bash

# ================================================================
# Script: restore_db.sh
# Descrição: Script seguro para restaurar banco de dados Neon a partir de backup
# Uso: ./restore_db.sh [opcoes] [arquivo_backup]
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
readonly BACKUP_DIR="${SCRIPT_DIR}/../backups"

# Cores para output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Variáveis de configuração
BACKUP_FILE=""
FORCE_RESTORE=false
CREATE_BACKUP_BEFORE_RESTORE=true
VERBOSE=false

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

# Função de limpeza
cleanup() {
    log_info "Executando limpeza de recursos temporários..."
    # Remove arquivos temporários se necessário
}

# Função de ajuda
show_help() {
    cat << EOF
Uso: $SCRIPT_NAME [OPÇÕES] [arquivo_backup]

DESCRIÇÃO:
    Restaura banco de dados Neon PostgreSQL a partir de arquivo de backup.
    Inclui validações de segurança e backup automático antes da restauração.

OPÇÕES:
    -h, --help              Mostra esta ajuda
    -f, --force             Força restauração sem confirmação
    -n, --no-backup         Não cria backup antes da restauração
    -v, --verbose           Modo verboso
    -b, --backup-dir DIR    Diretório de backups (padrão: ../backups)

PARÂMETROS:
    arquivo_backup          Caminho para o arquivo .sql de backup
                           Se não especificado, usa o backup mais recente

VARIÁVEIS DE AMBIENTE:
    DATABASE_URL            URL de conexão do banco Neon (obrigatória)
    BACKUP_RETENTION_DAYS   Dias para manter backups (padrão: 30)

EXEMPLOS:
    $SCRIPT_NAME                           # Restaura backup mais recente
    $SCRIPT_NAME backup_20240729.sql       # Restaura arquivo específico
    $SCRIPT_NAME --force --no-backup       # Restauração forçada sem backup
    $SCRIPT_NAME --verbose                 # Modo verboso

NOTAS:
    - Sempre faça backup antes de restaurar em produção
    - Verifique se a DATABASE_URL está correta
    - O script valida o arquivo SQL antes da restauração

EOF
}

# Validação de pré-requisitos
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    # Verificar se psql está instalado
    if ! command -v psql &> /dev/null; then
        log_error "PostgreSQL client (psql) não está instalado"
        log_info "Ubuntu/Debian: sudo apt-get install postgresql-client"
        log_info "CentOS/RHEL: sudo yum install postgresql"
        log_info "macOS: brew install postgresql"
        exit 1
    fi
    
    # Verificar variável DATABASE_URL
    if [[ -z "${DATABASE_URL:-}" ]]; then
        log_error "Variável de ambiente DATABASE_URL não está definida"
        log_info "Defina com: export DATABASE_URL='postgresql://user:pass@host:port/db'"
        exit 1
    fi
    
    # Validar formato da DATABASE_URL
    if [[ ! "$DATABASE_URL" =~ ^postgresql:// ]]; then
        log_error "DATABASE_URL deve começar com 'postgresql://'"
        exit 1
    fi
    
    # Criar diretório de backup se não existir
    if [[ ! -d "$BACKUP_DIR" ]]; then
        mkdir -p "$BACKUP_DIR"
        log_info "Diretório de backup criado: $BACKUP_DIR"
    fi
    
    log_success "Pré-requisitos atendidos"
}

# Testar conexão com banco
test_database_connection() {
    log_info "Testando conexão com banco de dados..."
    
    # Extrair informações da URL para mascarar senha no log
    local host=$(echo "$DATABASE_URL" | sed -E 's/.*@([^:]+):.*/\1/')
    local port=$(echo "$DATABASE_URL" | sed -E 's/.*:([0-9]+)\/.*/\1/')
    local db=$(echo "$DATABASE_URL" | sed -E 's/.*\/([^?]+).*/\1/')
    
    log_info "Conectando em: $host:$port/$db"
    
    if psql "$DATABASE_URL" -c "SELECT version();" &> /dev/null; then
        log_success "Conexão estabelecida com sucesso"
    else
        log_error "Falha na conexão com banco de dados"
        log_info "Verifique se a DATABASE_URL está correta e o banco está acessível"
        exit 1
    fi
}

# Encontrar arquivo de backup mais recente
find_latest_backup() {
    log_info "Procurando backup mais recente em: $BACKUP_DIR"
    
    local latest_backup
    latest_backup=$(find "$BACKUP_DIR" -name "*.sql" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
    
    if [[ -z "$latest_backup" ]]; then
        log_error "Nenhum arquivo de backup encontrado em: $BACKUP_DIR"
        log_info "Crie um backup primeiro ou especifique o arquivo manualmente"
        exit 1
    fi
    
    BACKUP_FILE="$latest_backup"
    log_success "Backup mais recente: $(basename "$BACKUP_FILE")"
}

# Validar arquivo de backup
validate_backup_file() {
    local file="$1"
    log_info "Validando arquivo de backup: $(basename "$file")"
    
    # Verificar se arquivo existe
    if [[ ! -f "$file" ]]; then
        log_error "Arquivo de backup não encontrado: $file"
        exit 1
    fi
    
    # Verificar se arquivo não está vazio
    if [[ ! -s "$file" ]]; then
        log_error "Arquivo de backup está vazio: $file"
        exit 1
    fi
    
    # Verificar se é um arquivo SQL válido
    if ! grep -q "CREATE\|INSERT\|COPY" "$file"; then
        log_warning "Arquivo não parece conter comandos SQL válidos"
        if [[ "$FORCE_RESTORE" == "false" ]]; then
            log_error "Use --force para continuar mesmo assim"
            exit 1
        fi
    fi
    
    # Mostrar informações do arquivo
    local file_size=$(du -h "$file" | cut -f1)
    local file_date=$(stat -c %y "$file" 2>/dev/null || stat -f %Sm "$file" 2>/dev/null)
    log_info "Tamanho: $file_size"
    log_info "Data: $file_date"
    
    log_success "Arquivo de backup validado"
}

# Criar backup antes da restauração
create_backup_before_restore() {
    if [[ "$CREATE_BACKUP_BEFORE_RESTORE" == "false" ]]; then
        log_warning "Pulando backup automático (--no-backup)"
        return 0
    fi
    
    log_info "Criando backup automático antes da restauração..."
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local auto_backup_file="$BACKUP_DIR/auto_backup_before_restore_${backup_timestamp}.sql"
    
    log_info "Exportando banco atual para: $(basename "$auto_backup_file")"
    
    if pg_dump "$DATABASE_URL" > "$auto_backup_file"; then
        log_success "Backup automático criado com sucesso"
        log_info "Arquivo: $auto_backup_file"
    else
        log_error "Falha ao criar backup automático"
        if [[ "$FORCE_RESTORE" == "false" ]]; then
            exit 1
        else
            log_warning "Continuando sem backup devido ao --force"
        fi
    fi
}

# Confirmar restauração
confirm_restore() {
    if [[ "$FORCE_RESTORE" == "true" ]]; then
        log_warning "Restauração forçada (--force)"
        return 0
    fi
    
    echo
    log_warning "ATENÇÃO: Esta operação irá SUBSTITUIR todos os dados do banco atual!"
    log_info "Arquivo de backup: $(basename "$BACKUP_FILE")"
    log_info "Banco de destino: $(echo "$DATABASE_URL" | sed -E 's/(.*:\/\/[^:]+:)[^@]+(@.*)/\1***\2/')"
    echo
    
    read -p "Tem certeza que deseja continuar? (digite 'CONFIRMO' para prosseguir): " confirmation
    
    if [[ "$confirmation" != "CONFIRMO" ]]; then
        log_info "Restauração cancelada pelo usuário"
        exit 0
    fi
    
    log_info "Restauração confirmada pelo usuário"
}

# Executar restauração
execute_restore() {
    log_info "Iniciando restauração do banco de dados..."
    
    local start_time=$(date +%s)
    
    # Executar restauração com log detalhado se verbose
    if [[ "$VERBOSE" == "true" ]]; then
        log_info "Executando restauração em modo verboso..."
        if psql "$DATABASE_URL" < "$BACKUP_FILE"; then
            log_success "Restauração executada com sucesso"
        else
            log_error "Falha durante a restauração"
            exit 1
        fi
    else
        log_info "Executando restauração..."
        if psql "$DATABASE_URL" < "$BACKUP_FILE" 2>&1 | tee -a "$LOG_FILE" | grep -E "(ERROR|FATAL)" && false; then
            log_error "Erros detectados durante a restauração"
            exit 1
        else
            log_success "Restauração executada com sucesso"
        fi
    fi
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    log_info "Tempo de restauração: ${duration} segundos"
}

# Verificar integridade pós-restauração
verify_restore() {
    log_info "Verificando integridade da restauração..."
    
    # Contar tabelas
    local table_count
    table_count=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | xargs)
    log_info "Tabelas encontradas: $table_count"
    
    # Verificar se há dados nas principais tabelas (ajustar conforme necessário)
    if psql "$DATABASE_URL" -c "\dt" &> /dev/null; then
        log_success "Esquema do banco restaurado com sucesso"
    else
        log_warning "Possível problema com o esquema do banco"
    fi
    
    log_success "Verificação de integridade concluída"
}

# Limpeza de backups antigos
cleanup_old_backups() {
    local retention_days="${BACKUP_RETENTION_DAYS:-30}"
    log_info "Limpando backups com mais de $retention_days dias..."
    
    local deleted_count=0
    while IFS= read -r -d '' old_backup; do
        rm "$old_backup"
        deleted_count=$((deleted_count + 1))
        log_info "Removido: $(basename "$old_backup")"
    done < <(find "$BACKUP_DIR" -name "*.sql" -type f -mtime +$retention_days -print0 2>/dev/null)
    
    if [[ $deleted_count -gt 0 ]]; then
        log_success "Removidos $deleted_count backups antigos"
    else
        log_info "Nenhum backup antigo para remover"
    fi
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
            -f|--force)
                FORCE_RESTORE=true
                shift
                ;;
            -n|--no-backup)
                CREATE_BACKUP_BEFORE_RESTORE=false
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                set -x
                shift
                ;;
            -b|--backup-dir)
                BACKUP_DIR="$2"
                shift 2
                ;;
            -*)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
            *)
                # Primeiro argumento não-opção é o arquivo de backup
                BACKUP_FILE="$1"
                shift
                ;;
        esac
    done
    
    # Configurar trap para cleanup
    trap cleanup EXIT
    
    # Validações iniciais
    check_prerequisites
    test_database_connection
    
    # Determinar arquivo de backup
    if [[ -z "$BACKUP_FILE" ]]; then
        find_latest_backup
    fi
    
    # Validar arquivo de backup
    validate_backup_file "$BACKUP_FILE"
    
    # Confirmar restauração
    confirm_restore
    
    # Criar backup antes da restauração
    create_backup_before_restore
    
    # Executar restauração
    execute_restore
    
    # Verificar integridade
    verify_restore
    
    # Limpeza de backups antigos
    cleanup_old_backups
    
    log_success "$SCRIPT_NAME executado com sucesso!"
    log_info "Log completo: $LOG_FILE"
    echo
    log_warning "IMPORTANTE: Teste a aplicação para verificar se tudo está funcionando corretamente"
}

# Executar função principal se script for chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
