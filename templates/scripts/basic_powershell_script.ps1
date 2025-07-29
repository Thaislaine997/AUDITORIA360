<#
.SYNOPSIS
    Template Básico para Scripts PowerShell - AUDITORIA360

.DESCRIPTION
    Template padrão para criação de scripts PowerShell seguindo as
    diretrizes de padronização do projeto AUDITORIA360.

.PARAMETER Environment
    Ambiente de execução (development, staging, production)

.PARAMETER Verbose
    Ativa modo verboso com informações detalhadas

.PARAMETER DryRun
    Simula execução sem fazer alterações reais

.EXAMPLE
    .\basic_powershell_script.ps1 -Environment "production" -Verbose

.EXAMPLE
    .\basic_powershell_script.ps1 -DryRun

.NOTES
    Autor: Equipe AUDITORIA360
    Data: Janeiro 2025
    Versão: 1.0
    
.LINK
    https://github.com/Thaislaine997/AUDITORIA360
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("development", "staging", "production")]
    [string]$Environment = "development",
    
    [Parameter(Mandatory = $false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory = $false)]
    [switch]$Verbose
)

# Configurações de erro
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Informações do script
$ScriptName = $MyInvocation.MyCommand.Name
$ScriptPath = $PSScriptRoot
$ProjectRoot = Split-Path -Parent $ScriptPath

# Funções de logging (obrigatórias em todos os scripts)
function Write-LogInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-LogSuccess {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-LogWarning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Função de validação de pré-requisitos
function Test-Prerequisites {
    Write-LogInfo "Validando pré-requisitos..."
    
    # Verificar se estamos no diretório correto
    if (!(Test-Path (Join-Path $ProjectRoot "requirements.txt"))) {
        Write-LogError "Execute o script a partir da raiz do projeto AUDITORIA360"
        exit 1
    }
    
    # Verificar dependências
    $requiredCommands = @("git", "python")
    foreach ($cmd in $requiredCommands) {
        if (!(Get-Command $cmd -ErrorAction SilentlyContinue)) {
            Write-LogError "Comando obrigatório não encontrado: $cmd"
            exit 1
        }
    }
    
    Write-LogSuccess "Pré-requisitos validados"
}

# Função de validação de variáveis de ambiente
function Test-EnvironmentVariables {
    param([string[]]$RequiredVars)
    
    foreach ($var in $RequiredVars) {
        if (!(Get-ChildItem Env: | Where-Object Name -eq $var)) {
            Write-LogError "Variável de ambiente obrigatória não definida: $var"
            exit 1
        }
    }
}

# Função principal do script
function Invoke-MainLogic {
    Write-LogInfo "Executando lógica principal..."
    
    if ($DryRun) {
        Write-LogWarning "Modo DRY-RUN ativo - simulando execução"
    }
    
    # TODO: Implementar lógica específica do script aqui
    
    Write-LogSuccess "Lógica principal executada com sucesso"
}

# Função de limpeza
function Invoke-Cleanup {
    param([int]$ExitCode = 0)
    
    if ($ExitCode -ne 0) {
        Write-LogError "Script finalizado com erro (código: $ExitCode)"
    }
    
    # Limpeza de recursos temporários
    
    exit $ExitCode
}

# Função principal
function Invoke-Main {
    try {
        Write-LogInfo "Iniciando $ScriptName..."
        
        # Configurar modo verboso se solicitado
        if ($Verbose) {
            $VerbosePreference = "Continue"
        }
        
        Test-Prerequisites
        Invoke-MainLogic
        
        Write-LogSuccess "$ScriptName executado com sucesso!"
        
    }
    catch {
        Write-LogError "Erro durante execução: $($_.Exception.Message)"
        Write-LogError "Linha: $($_.InvocationInfo.ScriptLineNumber)"
        Invoke-Cleanup -ExitCode 1
    }
}

# Executar se script foi chamado diretamente
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-Main
}