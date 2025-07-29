#!/bin/bash
#
# auditoria_gcp.sh - Auditoria recorrente de recursos e permissões GCP para AUDITORIA360
# 
# Uso: ./auditoria_gcp.sh [opções] > relatorio_auditoria_$(date +%Y%m%d).txt
# Exemplo: ./auditoria_gcp.sh --project-id auditoria-folha --verbose
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

# Configurações padrão
DEFAULT_PROJECT_ID="auditoria-folha"

# Variáveis globais
PROJECT_ID=""
LOGFILE=""
VERBOSE=false
OUTPUT_FORMAT="table"
SAVE_TO_FILE=true

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

# Função de output que vai tanto para stdout quanto para arquivo de log
output() {
    local message="$1"
    echo "$message"
    
    if [ "$SAVE_TO_FILE" = true ] && [ -n "$LOGFILE" ]; then
        echo "$message" >> "$LOGFILE"
    fi
}

# Função de ajuda
show_help() {
    cat << EOF
${SCRIPT_NAME} - Auditoria recorrente de recursos e permissões GCP

USO:
    ${SCRIPT_NAME} [OPÇÕES]

OPÇÕES:
    -h, --help                    Mostra esta ajuda
    -v, --verbose                 Modo verboso
    -p, --project-id PROJECT_ID   ID do projeto GCP (padrão: $DEFAULT_PROJECT_ID)
    -o, --output-format FORMAT    Formato de saída (table, json, csv) (padrão: table)
    -f, --log-file FILE          Arquivo de log personalizado
    --no-log-file                Não salvar em arquivo de log
    --stdout-only                Saída apenas no stdout

EXEMPLOS:
    ${SCRIPT_NAME} --project-id my-project
    ${SCRIPT_NAME} --output-format json > auditoria.json
    ${SCRIPT_NAME} --verbose --log-file custom_audit.log

SEÇÕES DE AUDITORIA:
    1. Instâncias Cloud SQL
    2. Bancos e usuários Cloud SQL  
    3. Firewalls e regras de rede
    4. Conectores VPC Serverless
    5. Service Accounts
    6. Permissões IAM
    7. Backups automáticos
    8. Datasets BigQuery
    9. Perfis Datastream
    10. Secret Manager
    11. Logs de auditoria

EOF
}

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se gcloud está instalado
    if ! command -v gcloud &> /dev/null; then
        log_error "Google Cloud CLI (gcloud) não encontrado"
        log_info "Instale em: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Verificar se bq está disponível
    if ! command -v bq &> /dev/null; then
        log_warning "BigQuery CLI (bq) não encontrado - seção BigQuery será ignorada"
    fi
    
    # Verificar autenticação
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1 &> /dev/null; then
        log_error "Usuário não está autenticado no Google Cloud"
        log_info "Execute: gcloud auth login"
        exit 1
    fi
    
    local active_account=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1)
    log_success "Autenticado como: $active_account"
    
    # Verificar se o projeto existe
    if ! gcloud projects describe "$PROJECT_ID" &> /dev/null; then
        log_error "Projeto '$PROJECT_ID' não encontrado ou sem acesso"
        exit 1
    fi
    
    log_success "Pré-requisitos validados"
}

# Configurar ambiente
setup_environment() {
    log_info "Configurando ambiente de auditoria..."
    
    # Configurar projeto ativo
    gcloud config set project "$PROJECT_ID"
    
    # Configurar arquivo de log se necessário
    if [ "$SAVE_TO_FILE" = true ] && [ -z "$LOGFILE" ]; then
        LOGFILE="${PROJECT_ROOT}/auditoria_gcp_$(date +%Y%m%d_%H%M%S).log"
        log_info "Arquivo de log: $LOGFILE"
    fi
    
    log_success "Ambiente configurado"
}

# Imprimir cabeçalho do relatório
print_header() {
    local header="==== Auditoria GCP - Projeto: $PROJECT_ID ===="
    local date_info="Data: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    local user_info="Usuário: $(gcloud auth list --filter=status:ACTIVE --format='value(account)' | head -n1)"
    
    output ""
    output "$header"
    output "$date_info"
    output "$user_info"
    output ""
}

# Executar comando gcloud com tratamento de erro
execute_gcloud_command() {
    local section_name="$1"
    local command="$2"
    
    output "=== $section_name ==="
    
    if eval "$command" 2>/dev/null; then
        log_success "Seção '$section_name' executada com sucesso"
    else
        log_warning "Falha na execução da seção '$section_name'"
        output "Erro: Não foi possível executar o comando ou sem dados disponíveis"
    fi
    
    output ""
}

# Auditoria de Cloud SQL
audit_cloud_sql() {
    execute_gcloud_command "1. Instâncias Cloud SQL" \
        "gcloud sql instances list --project=$PROJECT_ID --format='$OUTPUT_FORMAT'"
    
    # Auditoria detalhada de usuários por instância
    output "=== 2. Verificar bancos e usuários Cloud SQL ==="
    
    local instances=$(gcloud sql instances list --project="$PROJECT_ID" --format="value(name)" 2>/dev/null || echo "")
    
    if [ -n "$instances" ]; then
        while IFS= read -r instance; do
            if [ -n "$instance" ]; then
                output "  > Instância: $instance"
                gcloud sql users list --instance="$instance" --project="$PROJECT_ID" --format="$OUTPUT_FORMAT" 2>/dev/null || output "    Erro ao listar usuários"
                
                # Listar databases da instância
                output "  > Databases na instância $instance:"
                gcloud sql databases list --instance="$instance" --project="$PROJECT_ID" --format="$OUTPUT_FORMAT" 2>/dev/null || output "    Erro ao listar databases"
                
                output ""
            fi
        done <<< "$instances"
    else
        output "Nenhuma instância Cloud SQL encontrada"
        output ""
    fi
}

# Auditoria de rede
audit_network() {
    execute_gcloud_command "3. Firewalls e regras de rede" \
        "gcloud compute firewall-rules list --project=$PROJECT_ID --format='$OUTPUT_FORMAT'"
    
    execute_gcloud_command "4. Conectores VPC Serverless" \
        "gcloud compute networks vpc-access connectors list --project=$PROJECT_ID --format='$OUTPUT_FORMAT'"
}

# Auditoria de IAM
audit_iam() {
    execute_gcloud_command "5. Service Accounts vinculadas" \
        "gcloud iam service-accounts list --project=$PROJECT_ID --format='$OUTPUT_FORMAT'"
    
    output "=== 6. Permissões e papéis (IAM) ==="
    gcloud projects get-iam-policy "$PROJECT_ID" --format="table(bindings.role,bindings.members)" 2>/dev/null || output "Erro ao obter políticas IAM"
    output ""
}

# Auditoria de backups
audit_backups() {
    output "=== 7. Backups automáticos Cloud SQL ==="
    
    local instances=$(gcloud sql instances list --project="$PROJECT_ID" --format="value(name)" 2>/dev/null || echo "")
    
    if [ -n "$instances" ]; then
        while IFS= read -r instance; do
            if [ -n "$instance" ]; then
                output "  > Backups da instância: $instance"
                gcloud sql backups list --instance="$instance" --project="$PROJECT_ID" --format="$OUTPUT_FORMAT" 2>/dev/null || output "    Erro ao listar backups"
                output ""
            fi
        done <<< "$instances"
    else
        output "Nenhuma instância Cloud SQL para verificar backups"
        output ""
    fi
}

# Auditoria de BigQuery
audit_bigquery() {
    if command -v bq &> /dev/null; then
        execute_gcloud_command "8. Datasets BigQuery" \
            "bq ls --project_id=$PROJECT_ID --format='$OUTPUT_FORMAT'"
    else
        output "=== 8. Datasets BigQuery ==="
        output "BigQuery CLI não disponível - seção ignorada"
        output ""
    fi
}

# Auditoria de Datastream
audit_datastream() {
    execute_gcloud_command "9. Perfis Datastream" \
        "gcloud datastream connection-profiles list --project=$PROJECT_ID --format='$OUTPUT_FORMAT'"
}

# Auditoria de Secret Manager
audit_secrets() {
    execute_gcloud_command "10. Secret Manager" \
        "gcloud secrets list --project=$PROJECT_ID --format='$OUTPUT_FORMAT'"
}

# Auditoria de logs
audit_logging() {
    execute_gcloud_command "11. Verificação de auditoria de logs" \
        "gcloud logging sinks list --project=$PROJECT_ID --format='$OUTPUT_FORMAT'"
}

# Imprimir rodapé do relatório
print_footer() {
    output ""
    output "==== Auditoria Finalizada ===="
    output "Data de conclusão: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    
    if [ "$SAVE_TO_FILE" = true ] && [ -n "$LOGFILE" ]; then
        output "Relatório salvo em: $LOGFILE"
        log_success "Relatório completo salvo em: $LOGFILE"
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
            -p|--project-id)
                PROJECT_ID="$2"
                shift 2
                ;;
            -o|--output-format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            -f|--log-file)
                LOGFILE="$2"
                shift 2
                ;;
            --no-log-file)
                SAVE_TO_FILE=false
                shift
                ;;
            --stdout-only)
                SAVE_TO_FILE=false
                shift
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Configurar valor padrão se não fornecido
    PROJECT_ID="${PROJECT_ID:-$DEFAULT_PROJECT_ID}"
}

# Função principal
main() {
    parse_arguments "$@"
    
    log_info "Iniciando ${SCRIPT_NAME}..."
    log_info "Projeto: $PROJECT_ID"
    log_info "Formato de saída: $OUTPUT_FORMAT"
    
    validate_prerequisites
    setup_environment
    
    # Executar auditoria completa
    print_header
    audit_cloud_sql
    audit_network
    audit_iam
    audit_backups
    audit_bigquery
    audit_datastream
    audit_secrets
    audit_logging
    print_footer
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi