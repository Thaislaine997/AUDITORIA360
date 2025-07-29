# AUDITORIA360 - PowerShell Scripts Help
# This script displays information about available PowerShell scripts

param(
    [string]$ScriptName = ""
)

# Color functions for consistent output
function Write-Info {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Title {
    param($Message)
    Write-Host $Message -ForegroundColor Cyan
}

function Show-ScriptHelp {
    param($ScriptName)
    
    switch ($ScriptName.ToLower()) {
        "setup" {
            Write-Title "🔧 Setup Development Environment"
            Write-Host "Script: installers/setup_dev_env.ps1" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Purpose: Automatically sets up the development environment for Windows"
            Write-Host ""
            Write-Host "Usage:"
            Write-Host "  .\installers\setup_dev_env.ps1 [-SkipPython] [-SkipGit] [-VerboseOutput]"
            Write-Host ""
            Write-Host "Parameters:"
            Write-Host "  -SkipPython    Skip Python installation"
            Write-Host "  -SkipGit       Skip Git installation"
            Write-Host "  -VerboseOutput Show detailed output"
            Write-Host ""
            Write-Host "Examples:"
            Write-Host "  .\installers\setup_dev_env.ps1 -VerboseOutput"
            Write-Host "  .\installers\setup_dev_env.ps1 -SkipPython -SkipGit"
        }
        
        "backend" {
            Write-Title "☁️ Backend Deployment"
            Write-Host "Script: deploy/cloudrun_deploy_backend.ps1" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Purpose: Build and deploy the FastAPI backend to Google Cloud Run"
            Write-Host ""
            Write-Host "Usage:"
            Write-Host "  .\deploy\cloudrun_deploy_backend.ps1 -ProjectId <project> [options]"
            Write-Host ""
            Write-Host "Required Parameters:"
            Write-Host "  -ProjectId     Google Cloud Project ID"
            Write-Host ""
            Write-Host "Optional Parameters:"
            Write-Host "  -Region        Cloud Run region (default: us-central1)"
            Write-Host "  -ServiceName   Service name (default: auditoria360-backend)"
            Write-Host "  -ProcessorId   Document AI Processor ID"
            Write-Host "  -SkipBuild     Skip container build"
            Write-Host "  -AllowUnauthenticated  Allow unauthenticated access"
            Write-Host "  -VerboseOutput Show detailed output"
            Write-Host ""
            Write-Host "Examples:"
            Write-Host "  .\deploy\cloudrun_deploy_backend.ps1 -ProjectId 'my-project' -VerboseOutput"
            Write-Host "  .\deploy\cloudrun_deploy_backend.ps1 -ProjectId 'my-project' -ProcessorId 'abc123' -AllowUnauthenticated"
        }
        
        "frontend" {
            Write-Title "🎨 Frontend Deployment"
            Write-Host "Script: deploy/cloudrun_deploy_streamlit.ps1" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Purpose: Build and deploy the Streamlit frontend to Google Cloud Run"
            Write-Host ""
            Write-Host "Usage:"
            Write-Host "  .\deploy\cloudrun_deploy_streamlit.ps1 -ProjectId <project> -ApiBaseUrl <url> [options]"
            Write-Host ""
            Write-Host "Required Parameters:"
            Write-Host "  -ProjectId     Google Cloud Project ID"
            Write-Host "  -ApiBaseUrl    Backend API base URL"
            Write-Host ""
            Write-Host "Optional Parameters:"
            Write-Host "  -Region        Cloud Run region (default: us-central1)"
            Write-Host "  -ServiceName   Service name (default: auditoria360-streamlit)"
            Write-Host "  -SkipBuild     Skip container build"
            Write-Host "  -AllowUnauthenticated  Allow unauthenticated access"
            Write-Host "  -VerboseOutput Show detailed output"
            Write-Host ""
            Write-Host "Examples:"
            Write-Host "  .\deploy\cloudrun_deploy_streamlit.ps1 -ProjectId 'my-project' -ApiBaseUrl 'https://api.example.com' -VerboseOutput"
            Write-Host "  .\deploy\cloudrun_deploy_streamlit.ps1 -ProjectId 'my-project' -ApiBaseUrl 'https://api.example.com' -AllowUnauthenticated"
        }
        
        default {
            Write-Warning "Unknown script: $ScriptName"
            Write-Info "Available scripts: setup, backend, frontend"
        }
    }
}

function Show-AllScripts {
    Write-Title "🚀 AUDITORIA360 PowerShell Scripts"
    Write-Host "====================================="
    Write-Host ""
    
    Write-Info "Available scripts in this project:"
    Write-Host ""
    
    Write-Host "1. 🔧 Development Environment Setup" -ForegroundColor Green
    Write-Host "   Script: installers/setup_dev_env.ps1"
    Write-Host "   Purpose: Setup development environment (Python, Git, dependencies)"
    Write-Host "   Usage: .\installers\setup_dev_env.ps1 -VerboseOutput"
    Write-Host ""
    
    Write-Host "2. ☁️ Backend Deployment" -ForegroundColor Green
    Write-Host "   Script: deploy/cloudrun_deploy_backend.ps1"
    Write-Host "   Purpose: Deploy FastAPI backend to Google Cloud Run"
    Write-Host "   Usage: .\deploy\cloudrun_deploy_backend.ps1 -ProjectId 'project-id' -VerboseOutput"
    Write-Host ""
    
    Write-Host "3. 🎨 Frontend Deployment" -ForegroundColor Green
    Write-Host "   Script: deploy/cloudrun_deploy_streamlit.ps1"
    Write-Host "   Purpose: Deploy Streamlit frontend to Google Cloud Run"
    Write-Host "   Usage: .\deploy\cloudrun_deploy_streamlit.ps1 -ProjectId 'project-id' -ApiBaseUrl 'backend-url' -VerboseOutput"
    Write-Host ""
    
    Write-Info "For detailed help on a specific script:"
    Write-Host "  .\scripts\help.ps1 -ScriptName setup"
    Write-Host "  .\scripts\help.ps1 -ScriptName backend"
    Write-Host "  .\scripts\help.ps1 -ScriptName frontend"
    Write-Host ""
    
    Write-Info "Documentation:"
    Write-Host "  Complete guide: docs/tecnico/desenvolvimento/scripts-powershell.md"
    Write-Host "  Setup guide: docs/tecnico/desenvolvimento/setup-ambiente.md"
    Write-Host "  Deploy checklist: docs/tecnico/deploy/deploy-checklist.md"
    Write-Host ""
    
    Write-Success "All scripts follow the same pattern with standardized parameters and error handling."
}

# Main execution
if ([string]::IsNullOrEmpty($ScriptName)) {
    Show-AllScripts
} else {
    Show-ScriptHelp -ScriptName $ScriptName
}

Write-Host ""
Write-Info "Need more help? Check the documentation in docs/tecnico/desenvolvimento/scripts-powershell.md"