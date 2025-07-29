#!/bin/bash
#
# restore_db.sh - Script para restaurar banco Neon a partir de backup.sql
# 
# Uso: ./restore_db.sh [opções] [arquivo_backup]
# Exemplo: ./restore_db.sh --database-url postgresql://... backup.sql
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
DATABASE_URL=""
BACKUP_FILE=""
DRY_RUN=false
VERBOSE=false
FORCE=false
CREATE_BACKUP_BEFORE=true

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
${SCRIPT_NAME} - Restaurar banco Neon a partir de backup

USO:
    ${SCRIPT_NAME} [OPÇÕES] [ARQUIVO_BACKUP]

OPÇÕES:
    -h, --help                    Mostra esta ajuda
    -v, --verbose                 Modo verboso
    -d, --database-url URL        URL de conexão do banco (ou use variável DATABASE_URL)
    -f, --backup-file FILE        Arquivo de backup SQL (padrão: backup.sql)
    --dry-run                     Simula execução sem fazer alterações
    --force                       Força restauração mesmo com avisos
    --no-backup                   Não cria backup antes da restauração
    --create-db                   Cria database se não existir

EXEMPLOS:
    ${SCRIPT_NAME} backup.sql
    ${SCRIPT_NAME} --database-url postgresql://user:pass@host:5432/db backup.sql
    ${SCRIPT_NAME} --dry-run --verbose
    ${SCRIPT_NAME} --force --no-backup restore_file.sql

VARIÁVEIS DE AMBIENTE:
    DATABASE_URL                  URL de conexão do banco
    NEON_DATABASE_URL            URL alternativa (Neon specific)
    PGPASSWORD                   Senha do PostgreSQL (opcional)

FORMATOS SUPORTADOS:
    - SQL dump (.sql)
    - SQL comprimido (.sql.gz)
    - Backup customizado (.dump)

EOF
}

# Função de limpeza (executada ao sair)
cleanup() {
    local exit_code=$?
    
    # Limpar arquivos temporários
    if [ -n "${TEMP_BACKUP_FILE:-}" ] && [ -f "$TEMP_BACKUP_FILE" ]; then
        rm -f "$TEMP_BACKUP_FILE"
    fi
    
    if [ $exit_code -ne 0 ]; then
        log_error "Restauração finalizada com erro (código: $exit_code)"
    fi
    
    exit $exit_code
}

# Trap para executar cleanup ao sair
trap cleanup EXIT

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se psql está disponível
    if ! command -v psql &> /dev/null; then
        log_error "PostgreSQL client (psql) não encontrado"
        log_info "Instale com: apt-get install postgresql-client (Ubuntu/Debian)"
        log_info "Instale com: brew install postgresql (macOS)"
        exit 1
    fi
    
    # Verificar se pg_dump está disponível (para backup)
    if [ "$CREATE_BACKUP_BEFORE" = true ] && ! command -v pg_dump &> /dev/null; then
        log_warning "pg_dump não encontrado - backup antes da restauração será ignorado"
        CREATE_BACKUP_BEFORE=false
    fi
    
    log_success "Pré-requisitos validados"
}

# Validar configuração de banco
validate_database_config() {
    log_info "Validando configuração do banco..."
    
    # Verificar URL do banco
    if [ -z "$DATABASE_URL" ]; then
        # Tentar variáveis de ambiente alternativas
        if [ -n "${NEON_DATABASE_URL:-}" ]; then
            DATABASE_URL="$NEON_DATABASE_URL"
            log_info "Usando NEON_DATABASE_URL"
        else
            log_error "URL do banco não fornecida"
            log_info "Configure com --database-url ou variável DATABASE_URL"
            exit 1
        fi
    fi
    
    # Validar formato da URL
    if [[ ! "$DATABASE_URL" =~ ^postgresql:// ]]; then
        log_error "URL do banco deve começar com 'postgresql://'"
        exit 1
    fi
    
    # Extrair informações da URL para logs (sem mostrar senha)
    local url_info=$(echo "$DATABASE_URL" | sed -E 's/:([^:@]+)@/:***@/')
    log_success "URL do banco configurada: $url_info"
    
    log_success "Configuração do banco validada"
}

# Validar arquivo de backup
validate_backup_file() {
    log_info "Validando arquivo de backup..."
    
    # Verificar se arquivo existe
    if [ ! -f "$BACKUP_FILE" ]; then
        log_error "Arquivo de backup não encontrado: $BACKUP_FILE"
        exit 1
    fi
    
    # Verificar se arquivo não está vazio
    if [ ! -s "$BACKUP_FILE" ]; then
        log_error "Arquivo de backup está vazio: $BACKUP_FILE"
        exit 1
    fi
    
    # Detectar tipo de arquivo
    local file_size=$(du -h "$BACKUP_FILE" | cut -f1)
    log_success "Arquivo de backup encontrado: $BACKUP_FILE ($file_size)"
    
    # Verificar se é arquivo comprimido
    if [[ "$BACKUP_FILE" =~ \.gz$ ]]; then
        log_info "Arquivo comprimido detectado (.gz)"
        
        # Verificar se gzip está disponível
        if ! command -v gunzip &> /dev/null; then
            log_error "gunzip não encontrado para descomprimir arquivo"
            exit 1
        fi
    fi
    
    log_success "Arquivo de backup validado"
}

# Testar conexão com banco
test_database_connection() {
    log_info "Testando conexão com banco..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN: teste de conexão seria executado"
        return 0
    fi
    
    # Extrair senha da URL se presente
    local password=$(echo "$DATABASE_URL" | sed -n 's/.*:\([^@]*\)@.*/\1/p')
    if [ -n "$password" ]; then
        export PGPASSWORD="$password"
    fi
    
    # Testar conexão simples
    if psql "$DATABASE_URL" -c "SELECT version();" &> /dev/null; then
        log_success "Conexão com banco estabelecida"
    else
        log_error "Falha na conexão com banco"
        log_info "Verifique a URL de conexão e credenciais"
        exit 1
    fi
}

# Criar backup antes da restauração
create_backup_before_restore() {
    if [ "$CREATE_BACKUP_BEFORE" = false ]; then
        log_info "Backup antes da restauração desabilitado"
        return 0
    fi
    
    log_info "Criando backup antes da restauração..."
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local pre_restore_backup="pre_restore_backup_${backup_timestamp}.sql"
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN: backup seria criado em $pre_restore_backup"
        return 0
    fi
    
    # Extrair senha da URL se presente
    local password=$(echo "$DATABASE_URL" | sed -n 's/.*:\([^@]*\)@.*/\1/p')
    if [ -n "$password" ]; then
        export PGPASSWORD="$password"
    fi
    
    if pg_dump "$DATABASE_URL" > "$pre_restore_backup"; then
        log_success "Backup criado: $pre_restore_backup"
    else
        if [ "$FORCE" = true ]; then
            log_warning "Falha na criação do backup - continuando devido ao --force"
        else
            log_error "Falha na criação do backup - use --force para ignorar"
            exit 1
        fi
    fi
}

# Preparar arquivo para restauração
prepare_backup_file() {
    log_info "Preparando arquivo para restauração..."
    
    # Se arquivo está comprimido, descomprimir
    if [[ "$BACKUP_FILE" =~ \.gz$ ]]; then
        log_info "Descomprimindo arquivo..."
        
        TEMP_BACKUP_FILE="${BACKUP_FILE%.gz}"
        
        if [ "$DRY_RUN" = true ]; then
            log_warning "Modo DRY-RUN: arquivo seria descomprimido"
            BACKUP_FILE="$TEMP_BACKUP_FILE"
            return 0
        fi
        
        if gunzip -c "$BACKUP_FILE" > "$TEMP_BACKUP_FILE"; then
            BACKUP_FILE="$TEMP_BACKUP_FILE"
            log_success "Arquivo descomprimido"
        else
            log_error "Falha na descompressão do arquivo"
            exit 1
        fi
    fi
    
    log_success "Arquivo preparado para restauração"
}

# Executar restauração
execute_restore() {
    log_info "Iniciando restauração do banco..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN: restauração seria executada"
        log_info "Comando: psql \"$DATABASE_URL\" < \"$BACKUP_FILE\""
        return 0
    fi
    
    # Extrair senha da URL se presente
    local password=$(echo "$DATABASE_URL" | sed -n 's/.*:\([^@]*\)@.*/\1/p')
    if [ -n "$password" ]; then
        export PGPASSWORD="$password"
    fi
    
    log_info "Executando restauração..."
    
    if psql "$DATABASE_URL" < "$BACKUP_FILE"; then
        log_success "Restauração executada com sucesso"
    else
        log_error "Falha na restauração do banco"
        exit 1
    fi
}

# Verificar restauração
verify_restore() {
    log_info "Verificando restauração..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN: verificação seria executada"
        return 0
    fi
    
    # Extrair senha da URL se presente
    local password=$(echo "$DATABASE_URL" | sed -n 's/.*:\([^@]*\)@.*/\1/p')
    if [ -n "$password" ]; then
        export PGPASSWORD="$password"
    fi
    
    # Verificar se banco responde
    if psql "$DATABASE_URL" -c "SELECT 'Restauração verificada' as status;" &> /dev/null; then
        log_success "Verificação da restauração bem-sucedida"
    else
        log_error "Falha na verificação da restauração"
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
            -d|--database-url)
                DATABASE_URL="$2"
                shift 2
                ;;
            -f|--backup-file)
                BACKUP_FILE="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --no-backup)
                CREATE_BACKUP_BEFORE=false
                shift
                ;;
            --create-db)
                # Para implementação futura
                shift
                ;;
            -*)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
            *)
                # Arquivo de backup como argumento posicional
                BACKUP_FILE="$1"
                shift
                ;;
        esac
    done
    
    # Configurar valores padrão
    DATABASE_URL="${DATABASE_URL:-${DATABASE_URL:-}}"
    BACKUP_FILE="${BACKUP_FILE:-backup.sql}"
}

# Função principal
main() {
    log_info "Iniciando ${SCRIPT_NAME}..."
    
    parse_arguments "$@"
    
    # Usar diretório do projeto como base
    cd "$PROJECT_ROOT"
    
    log_info "Configurações:"
    log_info "  Arquivo de backup: $BACKUP_FILE"
    log_info "  Criar backup antes: $CREATE_BACKUP_BEFORE"
    
    validate_prerequisites
    validate_database_config
    validate_backup_file
    test_database_connection
    create_backup_before_restore
    prepare_backup_file
    execute_restore
    verify_restore
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
    log_info "Banco restaurado a partir de: $BACKUP_FILE"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
