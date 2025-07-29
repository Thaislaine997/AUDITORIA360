#!/bin/bash

# ================================================================
# Script: auditoria_gcp.sh
# Descrição: Auditoria recorrente de recursos e permissões GCP para AUDITORIA360
# Uso: ./auditoria_gcp.sh [opcoes]
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

# Configurações do projeto
PROJECT_ID="${GCP_PROJECT_ID:-auditoria-folha}"
OUTPUT_FORMAT="table"
GENERATE_REPORT=true
SAVE_TO_FILE=true

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

# Função de seção (para separar visualmente as seções do relatório)
log_section() {
    echo "" | tee -a "$LOG_FILE"
    echo "$(printf '=%.0s' {1..80})" | tee -a "$LOG_FILE"
    echo -e "${BLUE}$1${NC}" | tee -a "$LOG_FILE"
    echo "$(printf '=%.0s' {1..80})" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
}

# Função de ajuda
show_help() {
    cat << EOF
Uso: $SCRIPT_NAME [OPÇÕES]

DESCRIÇÃO:
    Executa auditoria completa dos recursos GCP do projeto AUDITORIA360.
    Gera relatórios detalhados sobre infraestrutura, segurança e custos.

OPÇÕES:
    -h, --help           Mostra esta ajuda
    -p, --project ID     ID do projeto GCP (padrão: auditoria-folha)
    -o, --output FORMAT  Formato de saída: table|json|yaml (padrão: table)
    -f, --file PATH      Arquivo de saída (padrão: auto-gerado)
    -q, --quiet          Modo silencioso (apenas erros)
    -v, --verbose        Modo verboso
    --no-report          Não gera relatório, apenas executa comandos
    --json-only          Saída apenas em JSON

EXEMPLOS:
    $SCRIPT_NAME                                    # Auditoria padrão
    $SCRIPT_NAME --project meu-projeto             # Projeto específico
    $SCRIPT_NAME --output json --file audit.json   # Saída em JSON
    $SCRIPT_NAME --quiet                           # Modo silencioso

VARIÁVEIS DE AMBIENTE:
    GCP_PROJECT_ID       ID do projeto GCP (sobrescreve padrão)
    AUDIT_OUTPUT_DIR     Diretório de saída (padrão: ./audit_reports)

EOF
}

# Validação de pré-requisitos
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    # Verificar se gcloud está instalado
    if ! command -v gcloud &> /dev/null; then
        log_error "Google Cloud SDK não está instalado"
        log_info "Instale em: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Verificar se bq está instalado
    if ! command -v bq &> /dev/null; then
        log_warning "BigQuery CLI (bq) não encontrado, alguns checks serão pulados"
    fi
    
    # Verificar autenticação
    if ! gcloud auth list --filter="status:ACTIVE" --format="value(account)" &> /dev/null; then
        log_error "Não está autenticado no Google Cloud"
        log_info "Execute: gcloud auth login"
        exit 1
    fi
    
    # Verificar acesso ao projeto
    if ! gcloud projects describe "$PROJECT_ID" &> /dev/null; then
        log_error "Projeto '$PROJECT_ID' não existe ou não é acessível"
        exit 1
    fi
    
    log_success "Pré-requisitos atendidos"
}

# Configurar projeto
setup_project() {
    log_info "Configurando projeto: $PROJECT_ID"
    
    if gcloud config set project "$PROJECT_ID"; then
        log_success "Projeto configurado: $PROJECT_ID"
    else
        log_error "Falha ao configurar projeto"
        exit 1
    fi
}

# Criar cabeçalho do relatório
create_report_header() {
    local output_file="$1"
    
    cat > "$output_file" << EOF
# AUDITORIA GCP - PROJETO: $PROJECT_ID
# Data: $(date)
# Executado por: $(gcloud auth list --filter="status:ACTIVE" --format="value(account)")
# Script: $SCRIPT_NAME v2.0.0

EOF
}

# Executar comando com tratamento de erro
execute_gcp_command() {
    local description="$1"
    local command="$2"
    local output_file="$3"
    
    log_info "$description"
    
    {
        echo "## $description"
        echo "Comando: $command"
        echo "Data: $(date)"
        echo ""
        
        if eval "$command" 2>&1; then
            echo ""
            echo "Status: ✅ Sucesso"
        else
            echo ""
            echo "Status: ❌ Erro na execução"
            log_warning "Erro ao executar: $description"
        fi
        
        echo ""
        echo "$(printf '─%.0s' {1..80})"
        echo ""
    } | tee -a "$output_file"
}

# Auditoria de instâncias Cloud SQL
audit_cloud_sql() {
    local output_file="$1"
    
    log_section "1. INSTÂNCIAS CLOUD SQL"
    
    execute_gcp_command \
        "Listando instâncias Cloud SQL" \
        "gcloud sql instances list --project=$PROJECT_ID" \
        "$output_file"
    
    # Verificar bancos e usuários para cada instância
    local instances
    instances=$(gcloud sql instances list --project="$PROJECT_ID" --format="value(name)" 2>/dev/null || true)
    
    if [[ -n "$instances" ]]; then
        while IFS= read -r instance; do
            if [[ -n "$instance" ]]; then
                execute_gcp_command \
                    "Bancos de dados da instância: $instance" \
                    "gcloud sql databases list --instance=$instance --project=$PROJECT_ID" \
                    "$output_file"
                
                execute_gcp_command \
                    "Usuários da instância: $instance" \
                    "gcloud sql users list --instance=$instance --project=$PROJECT_ID" \
                    "$output_file"
                
                execute_gcp_command \
                    "Backups da instância: $instance" \
                    "gcloud sql backups list --instance=$instance --project=$PROJECT_ID" \
                    "$output_file"
            fi
        done <<< "$instances"
    else
        echo "Nenhuma instância Cloud SQL encontrada." | tee -a "$output_file"
    fi
}

# Auditoria de rede e segurança
audit_network_security() {
    local output_file="$1"
    
    log_section "2. REDE E SEGURANÇA"
    
    execute_gcp_command \
        "Regras de firewall" \
        "gcloud compute firewall-rules list --project=$PROJECT_ID" \
        "$output_file"
    
    execute_gcp_command \
        "Conectores VPC Serverless" \
        "gcloud compute networks vpc-access connectors list --project=$PROJECT_ID" \
        "$output_file"
    
    execute_gcp_command \
        "Redes VPC" \
        "gcloud compute networks list --project=$PROJECT_ID" \
        "$output_file"
    
    execute_gcp_command \
        "Sub-redes" \
        "gcloud compute networks subnets list --project=$PROJECT_ID" \
        "$output_file"
}

# Auditoria de IAM
audit_iam() {
    local output_file="$1"
    
    log_section "3. IDENTIDADE E ACESSO (IAM)"
    
    execute_gcp_command \
        "Service Accounts" \
        "gcloud iam service-accounts list --project=$PROJECT_ID" \
        "$output_file"
    
    execute_gcp_command \
        "Políticas IAM do projeto" \
        "gcloud projects get-iam-policy $PROJECT_ID --format='table(bindings.role,bindings.members)'" \
        "$output_file"
    
    # Auditoria de chaves de service accounts
    local service_accounts
    service_accounts=$(gcloud iam service-accounts list --project="$PROJECT_ID" --format="value(email)" 2>/dev/null || true)
    
    if [[ -n "$service_accounts" ]]; then
        while IFS= read -r sa; do
            if [[ -n "$sa" ]]; then
                execute_gcp_command \
                    "Chaves da Service Account: $sa" \
                    "gcloud iam service-accounts keys list --iam-account=$sa --project=$PROJECT_ID" \
                    "$output_file"
            fi
        done <<< "$service_accounts"
    fi
}

# Auditoria de BigQuery
audit_bigquery() {
    local output_file="$1"
    
    log_section "4. BIGQUERY"
    
    if command -v bq &> /dev/null; then
        execute_gcp_command \
            "Datasets BigQuery" \
            "bq ls --project_id=$PROJECT_ID" \
            "$output_file"
        
        # Listar tabelas dos datasets
        local datasets
        datasets=$(bq ls --project_id="$PROJECT_ID" --format=json 2>/dev/null | jq -r '.[].datasetReference.datasetId' 2>/dev/null || true)
        
        if [[ -n "$datasets" ]]; then
            while IFS= read -r dataset; do
                if [[ -n "$dataset" ]]; then
                    execute_gcp_command \
                        "Tabelas do dataset: $dataset" \
                        "bq ls --project_id=$PROJECT_ID $dataset" \
                        "$output_file"
                fi
            done <<< "$datasets"
        fi
    else
        echo "BigQuery CLI não disponível, pulando auditoria do BigQuery." | tee -a "$output_file"
    fi
}

# Auditoria de Cloud Storage
audit_cloud_storage() {
    local output_file="$1"
    
    log_section "5. CLOUD STORAGE"
    
    execute_gcp_command \
        "Buckets Cloud Storage" \
        "gsutil ls -p $PROJECT_ID" \
        "$output_file"
    
    # Verificar configurações de buckets específicos do projeto
    local buckets
    buckets=$(gsutil ls -p "$PROJECT_ID" 2>/dev/null || true)
    
    if [[ -n "$buckets" ]]; then
        while IFS= read -r bucket; do
            if [[ -n "$bucket" ]]; then
                execute_gcp_command \
                    "Configurações do bucket: $bucket" \
                    "gsutil lifecycle get $bucket || echo 'Sem política de lifecycle'" \
                    "$output_file"
                
                execute_gcp_command \
                    "Permissões do bucket: $bucket" \
                    "gsutil iam get $bucket" \
                    "$output_file"
            fi
        done <<< "$buckets"
    fi
}

# Auditoria de Secret Manager
audit_secret_manager() {
    local output_file="$1"
    
    log_section "6. SECRET MANAGER"
    
    execute_gcp_command \
        "Secrets do Secret Manager" \
        "gcloud secrets list --project=$PROJECT_ID" \
        "$output_file"
}

# Auditoria de logs e monitoramento
audit_logging_monitoring() {
    local output_file="$1"
    
    log_section "7. LOGS E MONITORAMENTO"
    
    execute_gcp_command \
        "Sinks de logging" \
        "gcloud logging sinks list --project=$PROJECT_ID" \
        "$output_file"
    
    execute_gcp_command \
        "Métricas personalizadas" \
        "gcloud logging metrics list --project=$PROJECT_ID" \
        "$output_file"
}

# Auditoria de Cloud Run
audit_cloud_run() {
    local output_file="$1"
    
    log_section "8. CLOUD RUN"
    
    execute_gcp_command \
        "Serviços Cloud Run" \
        "gcloud run services list --project=$PROJECT_ID" \
        "$output_file"
}

# Auditoria de APIs habilitadas
audit_apis() {
    local output_file="$1"
    
    log_section "9. APIs HABILITADAS"
    
    execute_gcp_command \
        "APIs habilitadas no projeto" \
        "gcloud services list --enabled --project=$PROJECT_ID" \
        "$output_file"
}

# Resumo executivo
generate_executive_summary() {
    local output_file="$1"
    
    log_section "RESUMO EXECUTIVO"
    
    {
        echo "## Status Geral da Infraestrutura"
        echo ""
        
        # Contar recursos
        local sql_instances=$(gcloud sql instances list --project="$PROJECT_ID" --format="value(name)" 2>/dev/null | wc -l)
        local firewall_rules=$(gcloud compute firewall-rules list --project="$PROJECT_ID" --format="value(name)" 2>/dev/null | wc -l)
        local service_accounts=$(gcloud iam service-accounts list --project="$PROJECT_ID" --format="value(email)" 2>/dev/null | wc -l)
        local cloud_run_services=$(gcloud run services list --project="$PROJECT_ID" --format="value(metadata.name)" 2>/dev/null | wc -l)
        
        echo "- **Cloud SQL**: $sql_instances instância(s)"
        echo "- **Firewall**: $firewall_rules regra(s)"
        echo "- **Service Accounts**: $service_accounts conta(s)"
        echo "- **Cloud Run**: $cloud_run_services serviço(s)"
        echo ""
        
        echo "## Recomendações de Segurança"
        echo ""
        echo "1. ✅ Revisar regras de firewall regularmente"
        echo "2. ✅ Verificar permissões de Service Accounts"
        echo "3. ✅ Monitorar logs de acesso"
        echo "4. ✅ Validar configurações de backup"
        echo ""
        
        echo "## Próximos Passos"
        echo ""
        echo "1. Revisar este relatório com a equipe de segurança"
        echo "2. Implementar melhorias identificadas"
        echo "3. Agendar próxima auditoria para $(date -d '+1 month' '+%Y-%m-%d')"
        echo ""
        
    } | tee -a "$output_file"
}

# Função principal de auditoria
execute_audit() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output_dir="${AUDIT_OUTPUT_DIR:-./audit_reports}"
    local output_file="$output_dir/auditoria_gcp_${timestamp}.txt"
    
    # Criar diretório de saída
    mkdir -p "$output_dir"
    
    log_info "Iniciando auditoria GCP completa..."
    log_info "Relatório será salvo em: $output_file"
    
    # Criar cabeçalho
    create_report_header "$output_file"
    
    # Executar auditorias por seção
    audit_cloud_sql "$output_file"
    audit_network_security "$output_file"
    audit_iam "$output_file"
    audit_bigquery "$output_file"
    audit_cloud_storage "$output_file"
    audit_secret_manager "$output_file"
    audit_logging_monitoring "$output_file"
    audit_cloud_run "$output_file"
    audit_apis "$output_file"
    
    # Gerar resumo
    generate_executive_summary "$output_file"
    
    log_success "Auditoria concluída!"
    log_info "Relatório salvo em: $output_file"
    log_info "Log detalhado em: $LOG_FILE"
    
    # Mostrar estatísticas do relatório
    local lines=$(wc -l < "$output_file")
    local size=$(du -h "$output_file" | cut -f1)
    log_info "Estatísticas: $lines linhas, $size"
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
            -p|--project)
                PROJECT_ID="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            -f|--file)
                OUTPUT_FILE="$2"
                SAVE_TO_FILE=true
                shift 2
                ;;
            -q|--quiet)
                exec 1>/dev/null
                shift
                ;;
            -v|--verbose)
                set -x
                shift
                ;;
            --no-report)
                GENERATE_REPORT=false
                shift
                ;;
            --json-only)
                OUTPUT_FORMAT="json"
                shift
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Executar auditoria
    check_prerequisites
    setup_project
    execute_audit
    
    log_success "$SCRIPT_NAME executado com sucesso!"
}

# Executar função principal se script for chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi