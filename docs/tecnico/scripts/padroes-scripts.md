# Padrões de Scripts - AUDITORIA360

## Objetivo

Estabelecer padrões consistentes para todos os scripts do projeto AUDITORIA360, garantindo legibilidade, segurança e manutenibilidade.

## Padrões Gerais

### Nomenclatura
- Usar nomes descritivos e em minúsculas
- Separar palavras com underscore (_)
- Incluir extensão apropriada (.sh, .ps1, .bat)

### Documentação
- Header obrigatório em todos os scripts
- Comentários explicativos em funções complexas
- Documentação de parâmetros e variáveis importantes

### Segurança
- Validação de entrada
- Tratamento de erros
- Não expor credenciais no código
- Logs apropriados sem informações sensíveis

## Shell Scripts (.sh)

### Template Padrão

```bash
#!/bin/bash

# ================================================================
# Script: nome_do_script.sh
# Descrição: Breve descrição da funcionalidade
# Uso: ./nome_do_script.sh [parâmetros]
# Autor: AUDITORIA360 Team
# Data: YYYY-MM-DD
# Versão: 1.0.0
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

# Função de limpeza (chamada ao sair)
cleanup() {
    log_info "Limpando recursos temporários..."
    # Adicionar comandos de limpeza aqui
}

# Função de ajuda
show_help() {
    cat << EOF
Uso: $SCRIPT_NAME [OPÇÕES]

DESCRIÇÃO:
    Breve descrição do que o script faz

OPÇÕES:
    -h, --help     Mostra esta ajuda
    -v, --verbose  Modo verboso

EXEMPLOS:
    $SCRIPT_NAME --help
    $SCRIPT_NAME --verbose

EOF
}

# Validação de pré-requisitos
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    # Verificar comandos necessários
    local required_commands=("comando1" "comando2")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Comando requerido não encontrado: $cmd"
            exit 1
        fi
    done
    
    log_success "Todos os pré-requisitos atendidos"
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
            -v|--verbose)
                set -x
                shift
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Configurar trap para cleanup
    trap cleanup EXIT
    
    # Executar validações
    check_prerequisites
    
    # Lógica principal do script aqui
    log_info "Executando lógica principal..."
    
    log_success "$SCRIPT_NAME executado com sucesso!"
}

# Executar função principal se script for chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### Regras Específicas

1. **Shebang**: Sempre usar `#!/bin/bash`
2. **Configurações**: Definir `set -e`, `set -u`, `set -o pipefail`
3. **Variáveis**: Usar `readonly` para constantes, declarar no topo
4. **Funções**: Nomes em snake_case, uma responsabilidade por função
5. **Logs**: Usar funções padronizadas com cores
6. **Cleanup**: Implementar função de limpeza com trap
7. **Validação**: Verificar pré-requisitos antes da execução

## PowerShell Scripts (.ps1)

### Template Padrão

```powershell
<#
.SYNOPSIS
    Breve descrição do script

.DESCRIPTION
    Descrição detalhada da funcionalidade do script

.PARAMETER ParameterName
    Descrição do parâmetro

.EXAMPLE
    PS> .\script.ps1 -Parameter "value"
    Exemplo de uso do script

.NOTES
    Nome: script.ps1
    Autor: AUDITORIA360 Team
    Data: YYYY-MM-DD
    Versão: 1.0.0
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false, HelpMessage="Parâmetro de exemplo")]
    [string]$ParameterName,
    
    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

# Configurações globais
$ErrorActionPreference = "Stop"
$InformationPreference = "Continue"

# Variáveis globais
$ScriptPath = $PSScriptRoot
$ScriptName = $MyInvocation.MyCommand.Name
$LogFile = Join-Path $env:TEMP "$($ScriptName).log"

# Funções de logging
function Write-InfoLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [INFO] $Message"
    Write-Host $logMessage -ForegroundColor Blue
    $logMessage | Out-File -FilePath $LogFile -Append
}

function Write-SuccessLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [SUCCESS] $Message"
    Write-Host $logMessage -ForegroundColor Green
    $logMessage | Out-File -FilePath $LogFile -Append
}

function Write-WarningLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [WARNING] $Message"
    Write-Host $logMessage -ForegroundColor Yellow
    $logMessage | Out-File -FilePath $LogFile -Append
}

function Write-ErrorLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [ERROR] $Message"
    Write-Host $logMessage -ForegroundColor Red
    $logMessage | Out-File -FilePath $LogFile -Append
}

# Função para verificar pré-requisitos
function Test-Prerequisites {
    Write-InfoLog "Verificando pré-requisitos..."
    
    # Verificar comandos/módulos necessários
    $requiredCommands = @("comando1", "comando2")
    foreach ($cmd in $requiredCommands) {
        if (!(Get-Command $cmd -ErrorAction SilentlyContinue)) {
            Write-ErrorLog "Comando requerido não encontrado: $cmd"
            throw "Pré-requisito não atendido: $cmd"
        }
    }
    
    Write-SuccessLog "Todos os pré-requisitos atendidos"
}

# Função de limpeza
function Invoke-Cleanup {
    Write-InfoLog "Executando limpeza..."
    # Adicionar comandos de limpeza aqui
}

# Função principal
function Invoke-Main {
    try {
        Write-InfoLog "Iniciando $ScriptName..."
        
        # Verificar pré-requisitos
        Test-Prerequisites
        
        # Lógica principal do script aqui
        Write-InfoLog "Executando lógica principal..."
        
        Write-SuccessLog "$ScriptName executado com sucesso!"
    }
    catch {
        Write-ErrorLog "Erro durante execução: $($_.Exception.Message)"
        throw
    }
    finally {
        Invoke-Cleanup
    }
}

# Executar função principal
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-Main
}
```

### Regras Específicas

1. **Header**: Usar comentários .SYNOPSIS, .DESCRIPTION, etc.
2. **Parâmetros**: Declarar com [CmdletBinding()] e validação
3. **Configurações**: Definir `$ErrorActionPreference = "Stop"`
4. **Funções**: Usar verbo-substantivo (Write-Log, Test-Prerequisites)
5. **Try-Catch**: Implementar tratamento de erros robusto
6. **Logs**: Função padronizada com timestamp e cores

## Batch Scripts (.bat)

### Template Padrão

```batch
@echo off
setlocal EnableDelayedExpansion

REM ================================================================
REM Script: script_name.bat
REM Descrição: Breve descrição da funcionalidade
REM Uso: script_name.bat [parâmetros]
REM Autor: AUDITORIA360 Team
REM Data: YYYY-MM-DD
REM Versão: 1.0.0
REM ================================================================

REM Configurações
set SCRIPT_NAME=%~n0
set SCRIPT_DIR=%~dp0
set LOG_FILE=%TEMP%\%SCRIPT_NAME%.log

REM Função de logging (usando goto)
goto :main

:log_info
echo [INFO] %~1
echo [%date% %time%] [INFO] %~1 >> "%LOG_FILE%"
goto :eof

:log_success
echo [SUCCESS] %~1
echo [%date% %time%] [SUCCESS] %~1 >> "%LOG_FILE%"
goto :eof

:log_warning
echo [WARNING] %~1
echo [%date% %time%] [WARNING] %~1 >> "%LOG_FILE%"
goto :eof

:log_error
echo [ERROR] %~1
echo [%date% %time%] [ERROR] %~1 >> "%LOG_FILE%"
goto :eof

:check_prerequisites
call :log_info "Verificando pré-requisitos..."

REM Verificar comandos necessários
where comando1 >nul 2>&1
if errorlevel 1 (
    call :log_error "Comando requerido não encontrado: comando1"
    exit /b 1
)

call :log_success "Todos os pré-requisitos atendidos"
goto :eof

:cleanup
call :log_info "Executando limpeza..."
REM Adicionar comandos de limpeza aqui
goto :eof

:show_help
echo Uso: %SCRIPT_NAME% [OPCOES]
echo.
echo DESCRICAO:
echo     Breve descrição do que o script faz
echo.
echo OPCOES:
echo     /h, /help     Mostra esta ajuda
echo.
goto :eof

:main
call :log_info "Iniciando %SCRIPT_NAME%..."

REM Processar argumentos
:parse_args
if "%~1"=="" goto :start_execution
if /i "%~1"=="/h" goto :show_help
if /i "%~1"=="/help" goto :show_help

call :log_error "Opção desconhecida: %~1"
goto :show_help

:start_execution
REM Verificar pré-requisitos
call :check_prerequisites
if errorlevel 1 exit /b 1

REM Lógica principal do script aqui
call :log_info "Executando lógica principal..."

REM Limpeza
call :cleanup

call :log_success "%SCRIPT_NAME% executado com sucesso!"
exit /b 0
```

### Regras Específicas

1. **Header**: Iniciar com `@echo off` e `setlocal`
2. **Comentários**: Usar `REM` para comentários
3. **Funções**: Implementar com `:label` e `goto :eof`
4. **Logs**: Incluir timestamp nos logs
5. **Validação**: Verificar erros com `errorlevel`
6. **Limpeza**: Implementar rotina de cleanup

## Validação e Testes

### Checklist de Qualidade

- [ ] Header completo e atualizado
- [ ] Tratamento de erros implementado
- [ ] Logging apropriado
- [ ] Validação de pré-requisitos
- [ ] Função de limpeza
- [ ] Documentação de parâmetros
- [ ] Testes básicos executados
- [ ] Código revisado

### Ferramentas de Validação

- **Shell**: `shellcheck script.sh`
- **PowerShell**: `Invoke-ScriptAnalyzer script.ps1`
- **Batch**: Revisão manual seguindo checklist

## Manutenção

1. Revisar scripts semestralmente
2. Atualizar documentação conforme mudanças
3. Aplicar padrões a novos scripts
4. Refatorar scripts antigos quando possível