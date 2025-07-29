#!/bin/bash
#
# cloudrun_deploy.sh - Deploy automatizado para Google Cloud Run
# 
# Uso: ./cloudrun_deploy.sh [opções]
# Exemplo: ./cloudrun_deploy.sh --project-id my-project --region us-central1
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
DEFAULT_REGION="us-central1"
DEFAULT_SERVICE_NAME="auditoria360"
DEFAULT_CLOUDSQL_INSTANCE="auditoria-folha:us-central1:auditoria360portal"

# Variáveis globais
PROJECT_ID=""
REGION=""
SERVICE_NAME=""
CLOUDSQL_INSTANCE=""
DRY_RUN=false
VERBOSE=false
FORCE=false

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
${SCRIPT_NAME} - Deploy automatizado para Google Cloud Run

USO:
    ${SCRIPT_NAME} [OPÇÕES]

OPÇÕES:
    -h, --help                    Mostra esta ajuda
    -v, --verbose                 Modo verboso
    -p, --project-id PROJECT_ID   ID do projeto GCP (padrão: $DEFAULT_PROJECT_ID)
    -r, --region REGION           Região do deploy (padrão: $DEFAULT_REGION)
    -s, --service-name NAME       Nome do serviço (padrão: $DEFAULT_SERVICE_NAME)
    --cloudsql-instance INSTANCE  Instância CloudSQL (padrão: $DEFAULT_CLOUDSQL_INSTANCE)
    --dry-run                     Simula execução sem fazer deploy
    --force                       Força deploy mesmo com warnings
    --no-traffic                  Deploy sem direcionar tráfego

EXEMPLOS:
    ${SCRIPT_NAME} --project-id my-project
    ${SCRIPT_NAME} --region us-east1 --verbose
    ${SCRIPT_NAME} --dry-run

VARIÁVEIS DE AMBIENTE:
    GOOGLE_CLOUD_PROJECT         ID do projeto (sobrescreve --project-id)
    CLOUDSQL_DB_NAME            Nome do banco de dados
    CLOUDSQL_DB_USER            Usuário do banco de dados
    CLOUDSQL_DB_PASSWORD        Senha do banco de dados

EOF
}

# Função de limpeza (executada ao sair)
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Deploy finalizado com erro (código: $exit_code)"
    fi
    exit $exit_code
}

# Trap para executar cleanup ao sair
trap cleanup EXIT

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se estamos no diretório correto do projeto
    if [ ! -f "${PROJECT_ROOT}/Dockerfile" ] && [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
        log_error "Execute o script a partir da raiz do projeto AUDITORIA360"
        log_info "Arquivos esperados: Dockerfile ou requirements.txt"
        exit 1
    fi
    
    # Verificar se gcloud está instalado
    if ! command -v gcloud &> /dev/null; then
        log_error "Google Cloud CLI (gcloud) não encontrado"
        log_info "Instale em: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Verificar autenticação
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1 &> /dev/null; then
        log_error "Usuário não está autenticado no Google Cloud"
        log_info "Execute: gcloud auth login"
        exit 1
    fi
    
    local active_account=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1)
    log_success "Autenticado como: $active_account"
    
    log_success "Pré-requisitos validados"
}

# Configurar projeto GCP
setup_gcp_project() {
    log_info "Configurando projeto GCP..."
    
    # Usar PROJECT_ID da linha de comando ou variável de ambiente
    if [ -n "${GOOGLE_CLOUD_PROJECT:-}" ]; then
        PROJECT_ID="$GOOGLE_CLOUD_PROJECT"
        log_info "Usando PROJECT_ID da variável de ambiente: $PROJECT_ID"
    elif [ -z "$PROJECT_ID" ]; then
        # Tentar obter do gcloud config
        PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "$DEFAULT_PROJECT_ID")
        log_info "Usando PROJECT_ID do gcloud config: $PROJECT_ID"
    fi
    
    # Validar se o projeto existe
    if ! gcloud projects describe "$PROJECT_ID" &> /dev/null; then
        log_error "Projeto '$PROJECT_ID' não encontrado ou sem acesso"
        exit 1
    fi
    
    # Configurar projeto ativo
    gcloud config set project "$PROJECT_ID"
    log_success "Projeto configurado: $PROJECT_ID"
    
    # Verificar APIs necessárias
    local required_apis=("cloudbuild.googleapis.com" "run.googleapis.com" "sql.googleapis.com")
    for api in "${required_apis[@]}"; do
        if ! gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
            log_warning "API não habilitada: $api"
            
            if [ "$FORCE" = true ]; then
                log_info "Habilitando API: $api"
                gcloud services enable "$api"
            else
                log_error "APIs obrigatórias não habilitadas. Use --force para habilitar automaticamente"
                exit 1
            fi
        fi
    done
    
    log_success "Configuração do projeto GCP concluída"
}

# Preparar variáveis de ambiente
prepare_env_vars() {
    log_info "Preparando variáveis de ambiente..."
    
    # Variáveis obrigatórias com valores padrão
    local env_vars=""
    
    # CloudSQL
    if [ -n "${CLOUDSQL_DB_NAME:-}" ]; then
        env_vars="$env_vars,CLOUD_SQL_DB_NAME=${CLOUDSQL_DB_NAME}"
    else
        env_vars="$env_vars,CLOUD_SQL_DB_NAME=auditoria_db"
        log_warning "CLOUDSQL_DB_NAME não definida, usando: auditoria_db"
    fi
    
    if [ -n "${CLOUDSQL_DB_USER:-}" ]; then
        env_vars="$env_vars,CLOUD_SQL_DB_USER=${CLOUDSQL_DB_USER}"
    else
        env_vars="$env_vars,CLOUD_SQL_DB_USER=datastream_user"
        log_warning "CLOUDSQL_DB_USER não definida, usando: datastream_user"
    fi
    
    if [ -n "${CLOUDSQL_DB_PASSWORD:-}" ]; then
        env_vars="$env_vars,CLOUD_SQL_DB_PASSWORD=${CLOUDSQL_DB_PASSWORD}"
    else
        log_error "CLOUDSQL_DB_PASSWORD deve ser definida como variável de ambiente"
        exit 1
    fi
    
    # Remover vírgula inicial
    ENV_VARS="${env_vars#,}"
    
    log_success "Variáveis de ambiente preparadas"
}

# Executar build da imagem
execute_build() {
    log_info "Iniciando build da imagem Docker..."
    
    local image_tag="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
    
    cd "$PROJECT_ROOT"
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN: build seria executado"
        log_info "Comando: gcloud builds submit --tag $image_tag"
        return 0
    fi
    
    log_info "Executando: gcloud builds submit --tag $image_tag"
    
    if gcloud builds submit --tag "$image_tag"; then
        log_success "Build da imagem executado com sucesso"
    else
        log_error "Falha no build da imagem"
        exit 1
    fi
}

# Executar deploy no Cloud Run
execute_deploy() {
    log_info "Iniciando deploy no Cloud Run..."
    
    local image_tag="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
    
    # Preparar comando de deploy
    local deploy_cmd="gcloud run deploy ${SERVICE_NAME}"
    deploy_cmd="$deploy_cmd --image $image_tag"
    deploy_cmd="$deploy_cmd --platform managed"
    deploy_cmd="$deploy_cmd --region $REGION"
    deploy_cmd="$deploy_cmd --allow-unauthenticated"
    deploy_cmd="$deploy_cmd --add-cloudsql-instances $CLOUDSQL_INSTANCE"
    deploy_cmd="$deploy_cmd --set-env-vars \"$ENV_VARS\""
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Modo DRY-RUN: deploy seria executado"
        log_info "Comando: $deploy_cmd"
        return 0
    fi
    
    log_info "Executando deploy do serviço..."
    
    if gcloud run deploy "$SERVICE_NAME" \
        --image "$image_tag" \
        --platform managed \
        --region "$REGION" \
        --allow-unauthenticated \
        --add-cloudsql-instances "$CLOUDSQL_INSTANCE" \
        --set-env-vars "$ENV_VARS"; then
        
        log_success "Deploy executado com sucesso!"
        
        # Obter URL do serviço
        local service_url=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --format="value(status.url)")
        if [ -n "$service_url" ]; then
            log_success "URL do serviço: $service_url"
        fi
        
    else
        log_error "Falha no deploy do Cloud Run"
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
            -p|--project-id)
                PROJECT_ID="$2"
                shift 2
                ;;
            -r|--region)
                REGION="$2"
                shift 2
                ;;
            -s|--service-name)
                SERVICE_NAME="$2"
                shift 2
                ;;
            --cloudsql-instance)
                CLOUDSQL_INSTANCE="$2"
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
            --no-traffic)
                # Para implementação futura
                shift
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Configurar valores padrão se não fornecidos
    PROJECT_ID="${PROJECT_ID:-$DEFAULT_PROJECT_ID}"
    REGION="${REGION:-$DEFAULT_REGION}"
    SERVICE_NAME="${SERVICE_NAME:-$DEFAULT_SERVICE_NAME}"
    CLOUDSQL_INSTANCE="${CLOUDSQL_INSTANCE:-$DEFAULT_CLOUDSQL_INSTANCE}"
}

# Função principal
main() {
    log_info "Iniciando ${SCRIPT_NAME}..."
    
    parse_arguments "$@"
    
    log_info "Configurações de deploy:"
    log_info "  Projeto: $PROJECT_ID"
    log_info "  Região: $REGION"
    log_info "  Serviço: $SERVICE_NAME"
    log_info "  CloudSQL: $CLOUDSQL_INSTANCE"
    
    validate_prerequisites
    setup_gcp_project
    prepare_env_vars
    execute_build
    execute_deploy
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
    log_info "Deploy do AUDITORIA360 no Cloud Run concluído"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
