# ================================================================
# Script: cloudrun_deploy_streamlit.ps1
# Descrição: Script para build e deploy do Streamlit AUDITORIA360 no Google Cloud Run
# Uso: .\cloudrun_deploy_streamlit.ps1 [parâmetros]
# Autor: AUDITORIA360 Team
# Data: 2024-07-29
# Versão: 2.0.0
# ================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false, HelpMessage="ID do projeto GCP")]
    [string]$ProjectId = "auditoria-folha",
    
    [Parameter(Mandatory=$false, HelpMessage="Região do Cloud Run")]
    [string]$Region = "us-central1",
    
    [Parameter(Mandatory=$false, HelpMessage="Nome do serviço")]
    [string]$ServiceName = "auditoria360-streamlit",
    
    [Parameter(Mandatory=$false, HelpMessage="URL do backend API")]
    [string]$ApiUrl = "https://auditoria360-backend-url.run.app",
    
    [Parameter(Mandatory=$false, HelpMessage="Tag da imagem Docker")]
    [string]$ImageTag = "latest",
    
    [Parameter(Mandatory=$false, HelpMessage="Pular build da imagem")]
    [switch]$SkipBuild,
    
    [Parameter(Mandatory=$false, HelpMessage="Modo verboso")]
    [switch]$Verbose
)

# Configurações globais
$ErrorActionPreference = "Stop"
$InformationPreference = "Continue"

# Variáveis globais
$ScriptName = $MyInvocation.MyCommand.Name
$LogFile = Join-Path $env:TEMP "$($ScriptName).log"
$ImageName = "gcr.io/$ProjectId/$ServiceName"

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
    
    # Verificar se gcloud está instalado
    try {
        $gcloudVersion = gcloud version --format="value(Google Cloud SDK)" 2>$null
        Write-SuccessLog "Google Cloud SDK encontrado: $gcloudVersion"
    }
    catch {
        Write-ErrorLog "Google Cloud SDK não está instalado"
        Write-InfoLog "Instale em: https://cloud.google.com/sdk/docs/install"
        throw "Pré-requisito não atendido: Google Cloud SDK"
    }
    
    # Verificar se Docker está instalado
    try {
        $dockerVersion = docker --version 2>$null
        Write-SuccessLog "Docker encontrado: $dockerVersion"
    }
    catch {
        Write-ErrorLog "Docker não está instalado"
        Write-InfoLog "Instale em: https://docs.docker.com/get-docker/"
        throw "Pré-requisito não atendido: Docker"
    }
    
    # Verificar autenticação do gcloud
    try {
        $currentAccount = gcloud auth list --filter="status:ACTIVE" --format="value(account)" 2>$null
        if ([string]::IsNullOrWhiteSpace($currentAccount)) {
            Write-ErrorLog "Não está autenticado no Google Cloud"
            Write-InfoLog "Execute: gcloud auth login"
            throw "Autenticação necessária"
        }
        Write-SuccessLog "Autenticado como: $currentAccount"
    }
    catch {
        Write-ErrorLog "Erro ao verificar autenticação do gcloud"
        throw
    }
    
    Write-SuccessLog "Todos os pré-requisitos atendidos"
}

# Função para configurar projeto
function Set-GCloudProject {
    Write-InfoLog "Configurando projeto GCP: $ProjectId"
    
    try {
        gcloud config set project $ProjectId
        Write-SuccessLog "Projeto configurado: $ProjectId"
    }
    catch {
        Write-ErrorLog "Falha ao configurar projeto: $ProjectId"
        throw
    }
    
    # Verificar se o projeto existe e é acessível
    try {
        $projectInfo = gcloud projects describe $ProjectId --format="value(projectId)" 2>$null
        if ($projectInfo -eq $ProjectId) {
            Write-SuccessLog "Projeto verificado e acessível"
        }
        else {
            throw "Projeto não encontrado ou inacessível"
        }
    }
    catch {
        Write-ErrorLog "Erro ao verificar projeto: $ProjectId"
        throw
    }
}

# Função para verificar estrutura do projeto Streamlit
function Test-StreamlitStructure {
    Write-InfoLog "Verificando estrutura do projeto Streamlit..."
    
    $requiredFiles = @(
        "dashboards/app.py",
        "dashboards/requirements.txt",
        "deploy/Dockerfile.streamlit"
    )
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-InfoLog "✓ $file encontrado"
        }
        else {
            Write-ErrorLog "✗ $file não encontrado"
            throw "Arquivo obrigatório ausente: $file"
        }
    }
    
    # Verificar configurações do Streamlit
    if (Test-Path ".streamlit/config.toml") {
        Write-InfoLog "✓ Configuração do Streamlit encontrada"
    }
    else {
        Write-WarningLog "Configuração do Streamlit não encontrada (.streamlit/config.toml)"
    }
    
    Write-SuccessLog "Estrutura do projeto Streamlit validada"
}

# Função para validar configuração da API
function Test-ApiConfiguration {
    Write-InfoLog "Validando configuração da API..."
    
    # Verificar se URL da API foi fornecida
    if ([string]::IsNullOrWhiteSpace($ApiUrl) -or $ApiUrl -eq "https://auditoria360-backend-url.run.app") {
        Write-WarningLog "URL da API não foi configurada ou está usando valor padrão"
        Write-InfoLog "Use o parâmetro -ApiUrl para especificar a URL correta do backend"
    }
    else {
        Write-SuccessLog "URL da API configurada: $ApiUrl"
        
        # Teste básico de conectividade com a API
        try {
            $response = Invoke-WebRequest -Uri "$ApiUrl/health" -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-SuccessLog "API backend está acessível"
            }
            else {
                Write-WarningLog "API backend retornou status: $($response.StatusCode)"
            }
        }
        catch {
            Write-WarningLog "Não foi possível verificar conectividade com a API: $($_.Exception.Message)"
        }
    }
}

# Função para build da imagem Docker
function Invoke-DockerBuild {
    if ($SkipBuild) {
        Write-WarningLog "Pulando build da imagem (SkipBuild especificado)"
        return
    }
    
    Write-InfoLog "Iniciando build da imagem Docker do Streamlit..."
    Write-InfoLog "Imagem: $ImageName:$ImageTag"
    
    try {
        # Executar build com Dockerfile específico para Streamlit
        $buildCommand = "gcloud builds submit --tag ${ImageName}:${ImageTag} --file deploy/Dockerfile.streamlit"
        Write-InfoLog "Executando: $buildCommand"
        
        Invoke-Expression $buildCommand
        
        Write-SuccessLog "Build da imagem concluído com sucesso"
    }
    catch {
        Write-ErrorLog "Falha no build da imagem Docker"
        Write-ErrorLog $_.Exception.Message
        throw
    }
}

# Função para configurar variáveis de ambiente
function Get-EnvironmentVariables {
    Write-InfoLog "Configurando variáveis de ambiente do Streamlit..."
    
    $envVars = @{
        "API_BASE_URL" = $ApiUrl
        "STREAMLIT_SERVER_PORT" = "8080"
        "STREAMLIT_SERVER_ADDRESS" = "0.0.0.0"
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS" = "false"
        "ENVIRONMENT" = "production"
    }
    
    # Converter para formato do gcloud
    $envVarString = ($envVars.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join ","
    
    Write-InfoLog "Variáveis configuradas:"
    foreach ($var in $envVars.GetEnumerator()) {
        Write-InfoLog "  $($var.Key) = $($var.Value)"
    }
    
    return $envVarString
}

# Função para executar deploy
function Invoke-CloudRunDeploy {
    Write-InfoLog "Iniciando deploy do Streamlit no Cloud Run..."
    
    $envVars = Get-EnvironmentVariables
    
    try {
        $deployCommand = @(
            "gcloud run deploy $ServiceName",
            "--image ${ImageName}:${ImageTag}",
            "--platform managed",
            "--region $Region",
            "--allow-unauthenticated",
            "--set-env-vars `"$envVars`"",
            "--memory 2Gi",
            "--cpu 2",
            "--max-instances 50",
            "--timeout 900s",
            "--port 8080"
        ) -join " "
        
        Write-InfoLog "Executando deploy..."
        Write-InfoLog "Comando: $deployCommand"
        
        Invoke-Expression $deployCommand
        
        Write-SuccessLog "Deploy executado com sucesso"
    }
    catch {
        Write-ErrorLog "Falha no deploy do Cloud Run"
        Write-ErrorLog $_.Exception.Message
        throw
    }
}

# Função para verificar status do serviço
function Test-ServiceHealth {
    Write-InfoLog "Verificando status do serviço Streamlit..."
    
    try {
        # Obter URL do serviço
        $serviceUrl = gcloud run services describe $ServiceName --platform=managed --region=$Region --format="value(status.url)" 2>$null
        
        if ([string]::IsNullOrWhiteSpace($serviceUrl)) {
            Write-WarningLog "Não foi possível obter URL do serviço"
            return
        }
        
        Write-SuccessLog "Aplicação Streamlit disponível em: $serviceUrl"
        
        # Teste básico de conectividade
        try {
            $healthCheck = Invoke-WebRequest -Uri $serviceUrl -TimeoutSec 30 -UseBasicParsing
            if ($healthCheck.StatusCode -eq 200) {
                Write-SuccessLog "Aplicação está respondendo: HTTP $($healthCheck.StatusCode)"
            }
            else {
                Write-WarningLog "Aplicação retornou status: HTTP $($healthCheck.StatusCode)"
            }
        }
        catch {
            Write-WarningLog "Aplicação pode ainda estar inicializando ou não está acessível"
        }
    }
    catch {
        Write-WarningLog "Erro ao verificar status do serviço: $($_.Exception.Message)"
    }
}

# Função para mostrar informações do deploy
function Show-DeploymentInfo {
    Write-InfoLog "=== INFORMAÇÕES DO DEPLOY STREAMLIT ==="
    Write-InfoLog "Projeto: $ProjectId"
    Write-InfoLog "Região: $Region"
    Write-InfoLog "Serviço: $ServiceName"
    Write-InfoLog "Imagem: $ImageName:$ImageTag"
    Write-InfoLog "API Backend: $ApiUrl"
    Write-InfoLog "Log completo: $LogFile"
    
    try {
        $serviceUrl = gcloud run services describe $ServiceName --platform=managed --region=$Region --format="value(status.url)" 2>$null
        if (-not [string]::IsNullOrWhiteSpace($serviceUrl)) {
            Write-InfoLog "URL da aplicação: $serviceUrl"
            Write-InfoLog ""
            Write-SuccessLog "✅ Acesse sua aplicação AUDITORIA360 em: $serviceUrl"
        }
    }
    catch {
        Write-WarningLog "Não foi possível obter URL do serviço"
    }
    
    Write-InfoLog "========================================="
}

# Função de limpeza
function Invoke-Cleanup {
    Write-InfoLog "Executando limpeza..."
    # Adicionar comandos de limpeza se necessário
}

# Função principal
function Invoke-Main {
    try {
        Write-InfoLog "=== AUDITORIA360 - DEPLOY DO STREAMLIT NO CLOUD RUN ==="
        Write-InfoLog "Iniciando deploy da aplicação Streamlit..."
        
        # Validações
        Test-Prerequisites
        Set-GCloudProject
        Test-StreamlitStructure
        Test-ApiConfiguration
        
        # Build e Deploy
        Invoke-DockerBuild
        Invoke-CloudRunDeploy
        
        # Verificações pós-deploy
        Test-ServiceHealth
        Show-DeploymentInfo
        
        Write-SuccessLog "Deploy do Streamlit concluído com sucesso!"
        Write-InfoLog "A aplicação pode levar alguns minutos para estar totalmente disponível."
    }
    catch {
        Write-ErrorLog "Erro durante o deploy: $($_.Exception.Message)"
        Write-ErrorLog "Verifique o log completo em: $LogFile"
        throw
    }
    finally {
        Invoke-Cleanup
    }
}

# Executar função principal se não for importado como módulo
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-Main
}
