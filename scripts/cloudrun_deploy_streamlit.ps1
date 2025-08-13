<#
.SYNOPSIS
    Script PowerShell para build e deploy do Streamlit no Cloud Run

.DESCRIPTION
    Automatiza o processo de build da imagem Docker e deploy da aplicação 
    Streamlit da AUDITORIA360 no Google Cloud Run.

.PARAMETER ProjectId
    ID do projeto Google Cloud Platform

.PARAMETER Region
    Região para deploy do Cloud Run (padrão: us-central1)

.PARAMETER ServiceName
    Nome do serviço no Cloud Run (padrão: auditoria360-streamlit)

.PARAMETER ApiBaseUrl
    URL base da API backend (obrigatório)

.PARAMETER ImageTag
    Tag personalizada para a imagem (opcional)

.PARAMETER DockerFile
    Arquivo Dockerfile customizado (padrão: deploy/Dockerfile.streamlit)

.PARAMETER DryRun
    Simula execução sem fazer deploy real

.PARAMETER NoTraffic
    Deploy sem direcionar tráfego para nova versão

.EXAMPLE
    .\cloudrun_deploy_streamlit.ps1 -ProjectId "meu-projeto" -ApiBaseUrl "https://api.exemplo.com"

.EXAMPLE
    .\cloudrun_deploy_streamlit.ps1 -ProjectId "auditoria-folha" -ApiBaseUrl "https://backend-url" -Region "us-east1"

.EXAMPLE
    .\cloudrun_deploy_streamlit.ps1 -DryRun

.NOTES
    Autor: Equipe AUDITORIA360
    Data: Janeiro 2025
    Versão: 2.0
    
.LINK
    https://github.com/Thaislaine997/AUDITORIA360
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, HelpMessage = "ID do projeto GCP")]
    [ValidateNotNullOrEmpty()]
    [string]$ProjectId = "",
    
    [Parameter(Mandatory = $false)]
    [ValidateSet("us-central1", "us-east1", "us-west1", "europe-west1", "asia-east1")]
    [string]$Region = "us-central1",
    
    [Parameter(Mandatory = $false)]
    [ValidateNotNullOrEmpty()]
    [string]$ServiceName = "auditoria360-streamlit",
    
    [Parameter(Mandatory = $false, HelpMessage = "URL base da API backend")]
    [ValidateNotNullOrEmpty()]
    [string]$ApiBaseUrl = "",
    
    [Parameter(Mandatory = $false)]
    [string]$ImageTag = "",
    
    [Parameter(Mandatory = $false)]
    [string]$DockerFile = "deploy/Dockerfile.streamlit",
    
    [Parameter(Mandatory = $false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory = $false)]
    [switch]$NoTraffic
)

# Configurações de erro
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Informações do script
$ScriptName = $MyInvocation.MyCommand.Name
$ScriptPath = $PSScriptRoot
$ProjectRoot = Split-Path -Parent $ScriptPath

# Configurações padrão
$DefaultProjectId = "auditoria-folha"
$DefaultApiUrl = "https://auditoria360-backend-url"

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
    if (!(Test-Path (Join-Path $ProjectRoot "dashboards")) -and !(Test-Path (Join-Path $ProjectRoot "requirements.txt"))) {
        Write-LogError "Execute o script a partir da raiz do projeto AUDITORIA360"
        Write-LogInfo "Diretórios esperados: dashboards/ ou requirements.txt"
        exit 1
    }
    
    # Verificar se o Dockerfile existe
    $dockerfilePath = Join-Path $ProjectRoot $DockerFile
    if (!(Test-Path $dockerfilePath)) {
        Write-LogWarning "Dockerfile não encontrado: $DockerFile"
        Write-LogInfo "Usando Dockerfile padrão"
        $script:DockerFile = "Dockerfile"
    }
    
    # Verificar se gcloud está disponível
    if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
        Write-LogError "Google Cloud CLI (gcloud) não encontrado"
        Write-LogInfo "Instale em: https://cloud.google.com/sdk/docs/install"
        exit 1
    }
    
    # Verificar autenticação
    try {
        $activeAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" | Select-Object -First 1
        if (!$activeAccount) {
            Write-LogError "Usuário não está autenticado no Google Cloud"
            Write-LogInfo "Execute: gcloud auth login"
            exit 1
        }
        Write-LogSuccess "Autenticado como: $activeAccount"
    }
    catch {
        Write-LogError "Erro ao verificar autenticação: $($_.Exception.Message)"
        exit 1
    }
    
    Write-LogSuccess "Pré-requisitos validados"
}

# Configurar projeto GCP
function Set-GcpProject {
    Write-LogInfo "Configurando projeto GCP..."
    
    # Usar ProjectId fornecido ou padrão
    if ([string]::IsNullOrEmpty($ProjectId)) {
        # Tentar obter do gcloud config
        try {
            $ProjectId = gcloud config get-value project 2>$null
            if ([string]::IsNullOrEmpty($ProjectId)) {
                $ProjectId = $DefaultProjectId
            }
            Write-LogInfo "Usando PROJECT_ID: $ProjectId"
        }
        catch {
            $ProjectId = $DefaultProjectId
            Write-LogWarning "Usando PROJECT_ID padrão: $ProjectId"
        }
    }
    
    # Validar se o projeto existe
    try {
        gcloud projects describe $ProjectId | Out-Null
        Write-LogSuccess "Projeto encontrado: $ProjectId"
    }
    catch {
        Write-LogError "Projeto '$ProjectId' não encontrado ou sem acesso"
        exit 1
    }
    
    # Configurar projeto ativo
    gcloud config set project $ProjectId
    Write-LogSuccess "Projeto configurado: $ProjectId"
    
    return $ProjectId
}

# Validar configuração da API
function Test-ApiConfiguration {
    Write-LogInfo "Validando configuração da API..."
    
    # Verificar se URL da API foi fornecida
    if ([string]::IsNullOrEmpty($ApiBaseUrl)) {
        # Tentar obter de variável de ambiente
        $ApiBaseUrl = $env:API_BASE_URL
        if ([string]::IsNullOrEmpty($ApiBaseUrl)) {
            Write-LogWarning "URL da API não fornecida"
            Write-LogInfo "Usando URL padrão (configure com -ApiBaseUrl)"
            $script:ApiBaseUrl = $DefaultApiUrl
        }
        else {
            Write-LogInfo "Usando API_BASE_URL da variável de ambiente"
        }
    }
    
    # Validar formato da URL
    try {
        $uri = [System.Uri]$ApiBaseUrl
        if ($uri.Scheme -notin @("http", "https")) {
            Write-LogError "URL da API deve começar com http:// ou https://"
            exit 1
        }
        Write-LogSuccess "URL da API configurada: $ApiBaseUrl"
    }
    catch {
        Write-LogError "URL da API inválida: $ApiBaseUrl"
        exit 1
    }
    
    return $ApiBaseUrl
}

# Executar build da imagem
function Invoke-ImageBuild {
    param(
        [string]$ProjectId,
        [string]$ServiceName,
        [string]$ImageTag,
        [string]$DockerFile
    )
    
    Write-LogInfo "Iniciando build da imagem Docker..."
    
    if ([string]::IsNullOrEmpty($ImageTag)) {
        $ImageTag = "gcr.io/$ProjectId/$ServiceName"
    }
    
    if ($DryRun) {
        Write-LogWarning "Modo DRY-RUN: build seria executado"
        Write-LogInfo "Comando: gcloud builds submit --tag $ImageTag --file $DockerFile"
        return $ImageTag
    }
    
    try {
        if (Test-Path (Join-Path $ProjectRoot $DockerFile)) {
            Write-LogInfo "Executando: gcloud builds submit --tag $ImageTag --file $DockerFile"
            gcloud builds submit --tag $ImageTag --file $DockerFile
        }
        else {
            Write-LogInfo "Executando: gcloud builds submit --tag $ImageTag"
            gcloud builds submit --tag $ImageTag
        }
        
        Write-LogSuccess "Build da imagem executado com sucesso"
        return $ImageTag
    }
    catch {
        Write-LogError "Falha no build da imagem: $($_.Exception.Message)"
        exit 1
    }
}

# Executar deploy no Cloud Run
function Invoke-CloudRunDeploy {
    param(
        [string]$ServiceName,
        [string]$ImageTag,
        [string]$Region,
        [string]$ApiBaseUrl
    )
    
    Write-LogInfo "Iniciando deploy no Cloud Run..."
    
    if ($DryRun) {
        Write-LogWarning "Modo DRY-RUN: deploy seria executado"
        Write-LogInfo "Serviço: $ServiceName"
        Write-LogInfo "Imagem: $ImageTag"
        Write-LogInfo "Região: $Region"
        Write-LogInfo "API URL: $ApiBaseUrl"
        return
    }
    
    try {
        $deployArgs = @(
            "run", "deploy", $ServiceName,
            "--image", $ImageTag,
            "--platform", "managed",
            "--region", $Region,
            "--allow-unauthenticated",
            "--set-env-vars", "API_BASE_URL=$ApiBaseUrl"
        )
        
        if ($NoTraffic) {
            $deployArgs += "--no-traffic"
            Write-LogInfo "Deploy sem direcionamento de tráfego"
        }
        
        Write-LogInfo "Executando deploy do serviço..."
        & gcloud $deployArgs
        
        Write-LogSuccess "Deploy executado com sucesso!"
        
        # Obter URL do serviço
        try {
            $serviceUrl = gcloud run services describe $ServiceName --region=$Region --format="value(status.url)"
            if (![string]::IsNullOrEmpty($serviceUrl)) {
                Write-LogSuccess "URL do Streamlit: $serviceUrl"
            }
        }
        catch {
            Write-LogWarning "Não foi possível obter URL do serviço"
        }
    }
    catch {
        Write-LogError "Falha no deploy do Cloud Run: $($_.Exception.Message)"
        exit 1
    }
}

# Função de limpeza
function Invoke-Cleanup {
    param([int]$ExitCode = 0)
    
    if ($ExitCode -ne 0) {
        Write-LogError "Script finalizado com erro (código: $ExitCode)"
    }
    
    # Limpeza de recursos temporários se necessário
    
    exit $ExitCode
}

# Função principal
function Invoke-Main {
    try {
        Write-LogInfo "Iniciando $ScriptName..."
        
        # Configurar modo verboso se solicitado
        if ($VerbosePreference -eq "Continue") {
            Write-LogInfo "Modo verboso ativado"
        }
        
        # Mudar para diretório do projeto
        Set-Location $ProjectRoot
        
        Test-Prerequisites
        $ProjectId = Set-GcpProject
        $ApiBaseUrl = Test-ApiConfiguration
        $imageTag = Invoke-ImageBuild -ProjectId $ProjectId -ServiceName $ServiceName -ImageTag $ImageTag -DockerFile $DockerFile
        Invoke-CloudRunDeploy -ServiceName $ServiceName -ImageTag $imageTag -Region $Region -ApiBaseUrl $ApiBaseUrl
        
        Write-LogSuccess "$ScriptName executado com sucesso!"
        Write-LogInfo "Deploy do Streamlit AUDITORIA360 no Cloud Run concluído"
        
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
