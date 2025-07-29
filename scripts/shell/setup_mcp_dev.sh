#!/bin/bash
#
# setup_mcp_dev.sh - Script para configurar ambiente de desenvolvimento MCP
# 
# Uso: ./setup_mcp_dev.sh [opções]
# Exemplo: ./setup_mcp_dev.sh --skip-install --verbose
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
SKIP_INSTALL=false
VERBOSE=false
DRY_RUN=false

# Funções de logging padronizadas
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
${SCRIPT_NAME} - Configurar ambiente de desenvolvimento MCP

USO:
    ${SCRIPT_NAME} [OPÇÕES]

OPÇÕES:
    -h, --help          Mostra esta ajuda
    -v, --verbose       Modo verboso
    --skip-install      Pula instalação de dependências
    --dry-run           Simula execução sem fazer alterações

EXEMPLOS:
    ${SCRIPT_NAME} --skip-install
    ${SCRIPT_NAME} --verbose
    ${SCRIPT_NAME} --dry-run

DESCRIÇÃO:
    Este script configura o ambiente completo de desenvolvimento MCP
    para integração com GitHub Copilot no projeto AUDITORIA360.

EOF
}

# Função de limpeza (executada ao sair)
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Setup finalizado com erro (código: $exit_code)"
    fi
    exit $exit_code
}

# Trap para executar cleanup ao sair
trap cleanup EXIT

# Validação de pré-requisitos
validate_prerequisites() {
    log_info "Validando pré-requisitos..."
    
    # Verificar se estamos no diretório correto do projeto
    if [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
        log_error "Execute o script a partir da raiz do projeto AUDITORIA360"
        log_info "Arquivo esperado: requirements.txt"
        exit 1
    fi
    
    # Verificar se Python está disponível
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        log_error "Python não encontrado no sistema"
        exit 1
    fi
    
    log_success "Pré-requisitos validados"
}

# Criar estrutura de diretórios
create_directory_structure() {
    log_info "Criando estrutura de diretórios..."
    
    local directories=(
        "logs"
        "configs/mcp/servers"
        "configs/mcp/clients" 
        "configs/copilot"
        ".vscode"
    )
    
    for dir in "${directories[@]}"; do
        if [ "$DRY_RUN" = true ]; then
            log_info "Seria criado diretório: $dir"
        else
            mkdir -p "${PROJECT_ROOT}/$dir"
            log_success "✓ Criado diretório: $dir"
        fi
    done
}

# Instalar dependências MCP
install_mcp_dependencies() {
    if [ "$SKIP_INSTALL" = true ]; then
        log_info "Pulando instalação de dependências (--skip-install)"
        return 0
    fi
    
    log_info "Instalando dependências MCP..."
    
    local dependencies=("pydantic" "pyyaml" "asyncio")
    
    if [ "$DRY_RUN" = true ]; then
        log_info "Seria executado: pip install ${dependencies[*]}"
        return 0
    fi
    
    # Verificar se pip está disponível
    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        log_error "pip não encontrado. Instale pip primeiro"
        exit 1
    fi
    
    local pip_cmd="pip"
    if command -v pip3 &> /dev/null; then
        pip_cmd="pip3"
    fi
    
    $pip_cmd install "${dependencies[@]}"
    log_success "Dependências MCP instaladas"
}

# Gerar configuração MCP
generate_mcp_configuration() {
    log_info "Gerando configuração MCP..."
    
    local config_file="${PROJECT_ROOT}/configs/mcp/mcp_config.yaml"
    
    if [ -f "$config_file" ]; then
        log_warning "Arquivo de configuração MCP já existe: $config_file"
        return 0
    fi
    
    if [ "$DRY_RUN" = true ]; then
        log_info "Seria gerada configuração MCP em: $config_file"
        return 0
    fi
    
    # Verificar se o módulo Python existe
    if ! python3 -c "from src.mcp.config import get_config_manager" 2>/dev/null; then
        log_warning "Módulo src.mcp.config não encontrado - pulando geração automática"
        log_info "Configure manualmente ou execute após setup completo do projeto"
        return 0
    fi
    
    python3 -c "
from src.mcp.config import get_config_manager
config_manager = get_config_manager('configs/mcp')
config = config_manager.load_config()
config_manager.save_config(config)
print('MCP configuration generated successfully')
" && log_success "Configuração MCP gerada com sucesso"
}

# Gerar configuração do GitHub Copilot
generate_copilot_configuration() {
    log_info "Gerando configuração do GitHub Copilot..."
    
    local copilot_config_file="${PROJECT_ROOT}/configs/copilot/copilot_mcp.json"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "Seria gerada configuração Copilot em: $copilot_config_file"
        return 0
    fi
    
    # Verificar se o módulo Python existe
    if ! python3 -c "from src.mcp.config import get_config_manager" 2>/dev/null; then
        log_warning "Módulo src.mcp.config não encontrado - pulando geração automática"
        log_info "Configure manualmente ou execute após setup completo do projeto"
        return 0
    fi
    
    python3 -c "
import json
from src.mcp.config import get_config_manager

config_manager = get_config_manager('configs/mcp')
config = config_manager.load_config()
copilot_config = config_manager.generate_copilot_config()

with open('configs/copilot/copilot_mcp.json', 'w') as f:
    json.dump(copilot_config, f, indent=2)

print('Copilot configuration generated successfully')
" && log_success "Configuração Copilot gerada com sucesso"
}

# Criar scripts de inicialização MCP
create_mcp_startup_scripts() {
    log_info "Criando scripts de inicialização MCP..."
    
    local mcp_server_script="${PROJECT_ROOT}/scripts/start_mcp_server.sh"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "Seria criado script: $mcp_server_script"
    else
        # Criar script do servidor MCP
        cat > "$mcp_server_script" << 'EOF'
#!/bin/bash
#
# start_mcp_server.sh - Iniciar servidor MCP do AUDITORIA360
#
# Configurações de segurança
set -e
set -u
set -o pipefail

echo "🚀 Iniciando servidor MCP do AUDITORIA360..."

# Definir variáveis de ambiente
export AUDITORIA360_MCP_MODE=server
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Iniciar o servidor
python -m src.mcp.copilot_server
EOF
        
        chmod +x "$mcp_server_script"
        log_success "✓ Script do servidor MCP criado"
    fi
}

# Criar script de ambiente de desenvolvimento
create_dev_environment_script() {
    log_info "Criando script de ambiente de desenvolvimento..."
    
    local dev_script="${PROJECT_ROOT}/scripts/start_dev_environment.sh"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "Seria criado script: $dev_script"
    else
        cat > "$dev_script" << 'EOF'
#!/bin/bash
#
# start_dev_environment.sh - Iniciar ambiente completo de desenvolvimento
#
# Configurações de segurança
set -e
set -u
set -o pipefail

echo "🚀 Iniciando ambiente de desenvolvimento AUDITORIA360 com MCP..."

# Função de limpeza
cleanup() {
    echo "🛑 Encerrando ambiente de desenvolvimento..."
    kill $API_PID 2>/dev/null || true
    kill $MCP_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar servidor API principal em background
echo "📡 Iniciando servidor API principal..."
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!

# Aguardar inicialização da API
sleep 3

# Iniciar servidor MCP em background
echo "🔧 Iniciando servidor MCP..."
export AUDITORIA360_MCP_MODE=server
python -m src.mcp.copilot_server &
MCP_PID=$!

echo "✅ Ambiente de desenvolvimento iniciado!"
echo "📊 Servidor API: http://localhost:8000"
echo "🔧 Servidor MCP: Executando em stdio"
echo "📖 Documentação API: http://localhost:8000/docs"
echo ""
echo "Pressione Ctrl+C para encerrar..."

# Aguardar processos
wait $API_PID $MCP_PID
EOF
        
        chmod +x "$dev_script"
        log_success "✓ Script de ambiente de desenvolvimento criado"
    fi
}

# Mostrar instruções finais
show_final_instructions() {
    log_info "Setup do ambiente MCP concluído!"
    
    echo ""
    log_success "✅ Ambiente de desenvolvimento MCP do AUDITORIA360 configurado com sucesso!"
    echo ""
    echo "📚 Próximos passos:"
    echo "1. Revisar os arquivos de configuração gerados"
    echo "2. Executar 'python scripts/test_mcp.py' para testar a integração"
    echo "3. Iniciar desenvolvimento com './scripts/start_dev_environment.sh'"
    echo "4. Abrir VS Code e usar GitHub Copilot com ferramentas MCP"
    echo ""
    echo "📖 Documentação: docs/MCP_INTEGRATION.md"
    echo "⚙️  Configuração: configs/mcp/mcp_config.yaml"
    echo "🔧 Configurações VS Code: .vscode/settings.json"
    echo ""
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
            --skip-install)
                SKIP_INSTALL=true
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

# Função principal
main() {
    log_info "Iniciando ${SCRIPT_NAME}..."
    
    parse_arguments "$@"
    
    cd "$PROJECT_ROOT"
    
    validate_prerequisites
    create_directory_structure
    install_mcp_dependencies
    generate_mcp_configuration
    generate_copilot_configuration
    create_mcp_startup_scripts
    create_dev_environment_script
    show_final_instructions
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
    log_info "Setup do ambiente MCP para AUDITORIA360 concluído"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_agent import EnhancedAIAgent

async def test_mcp_integration():
    """Test MCP integration functionality"""
    print("🧪 Testing AUDITORIA360 MCP Integration...")
    
    # Initialize enhanced AI agent
    agent = EnhancedAIAgent()
    
    # Wait for initialization
    max_wait = 30
    waited = 0
    while agent.status == "initializing" and waited < max_wait:
        await asyncio.sleep(1)
        waited += 1
    
    if agent.status != "ready":
        print(f"❌ Agent failed to initialize: {agent.status}")
        return False
    
    print(f"✅ Agent initialized successfully: {agent.status}")
    
    # Test MCP capabilities
    try:
        capabilities = await agent.get_mcp_capabilities()
        print(f"📋 MCP Capabilities: {len(capabilities.get('tools', []))} tools, {len(capabilities.get('resources', []))} resources")
        
        # Test payroll calculation
        print("\n🧮 Testing payroll calculation...")
        result = await agent.executar_acao(
            "calcular folha de pagamento",
            {
                "employee_id": "TEST001",
                "base_salary": 5000.00,
                "overtime_hours": 8
            }
        )
        
        if result.get("success"):
            print("✅ Payroll calculation successful")
            calculation_result = result.get("result", {})
# Mostrar instruções finais
show_final_instructions() {
    log_info "Setup do ambiente MCP concluído!"
    
    echo ""
    log_success "✅ Ambiente de desenvolvimento MCP do AUDITORIA360 configurado com sucesso!"
    echo ""
    echo "📚 Próximos passos:"
    echo "1. Revisar os arquivos de configuração gerados"
    echo "2. Executar 'python scripts/test_mcp.py' para testar a integração"
    echo "3. Iniciar desenvolvimento com './scripts/start_dev_environment.sh'"
    echo "4. Abrir VS Code e usar GitHub Copilot com ferramentas MCP"
    echo ""
    echo "📖 Documentação: docs/MCP_INTEGRATION.md"
    echo "⚙️  Configuração: configs/mcp/mcp_config.yaml"
    echo "🔧 Configurações VS Code: .vscode/settings.json"
    echo ""
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
            --skip-install)
                SKIP_INSTALL=true
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

# Função principal
main() {
    log_info "Iniciando ${SCRIPT_NAME}..."
    
    parse_arguments "$@"
    
    cd "$PROJECT_ROOT"
    
    validate_prerequisites
    create_directory_structure
    install_mcp_dependencies
    generate_mcp_configuration
    generate_copilot_configuration
    create_mcp_startup_scripts
    create_dev_environment_script
    show_final_instructions
    
    log_success "${SCRIPT_NAME} executado com sucesso!"
    log_info "Setup do ambiente MCP para AUDITORIA360 concluído"
}

# Executar função principal se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi