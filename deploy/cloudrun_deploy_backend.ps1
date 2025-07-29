# AUDITORIA360 - Backend Deployment Script for Google Cloud Run
# This script builds and deploys the backend API to Google Cloud Run
# Requires: gcloud CLI installed and authenticated

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [string]$Region = "us-central1",
    
    [string]$ServiceName = "auditoria360-backend",
    
    [string]$ImageName = "",
    
    [string]$ProcessorId = "",
    
    [string]$BQDatasetId = "auditoria_folha_dataset",
    
    [string]$TextBucketName = "auditoria360-ccts-textos-extraidos",
    
    [switch]$SkipBuild,
    
    [switch]$AllowUnauthenticated,
    
    [switch]$VerboseOutput
)

# Set error action preference
$ErrorActionPreference = "Stop"

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

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    # Check if gcloud CLI is installed
    if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
        Write-Error "gcloud CLI not found. Please install Google Cloud SDK."
        exit 1
    }
    
    # Check if user is authenticated
    try {
        $currentProject = gcloud config get-value project --quiet 2>$null
        if ([string]::IsNullOrEmpty($currentProject)) {
            Write-Error "No active gcloud project. Please run 'gcloud auth login' and 'gcloud config set project PROJECT_ID'"
            exit 1
        }
        Write-Success "gcloud CLI authenticated with project: $currentProject"
    } catch {
        Write-Error "Failed to verify gcloud authentication"
        exit 1
    }
    
    # Check if Dockerfile exists
    if (!(Test-Path "Dockerfile")) {
        Write-Error "Dockerfile not found in current directory"
        exit 1
    }
    
    Write-Success "Prerequisites check passed"
}

function Build-ContainerImage {
    param($ImageTag)
    
    if ($SkipBuild) {
        Write-Info "Skipping container build (--SkipBuild flag)"
        return
    }
    
    Write-Info "Building container image: $ImageTag"
    
    try {
        if ($VerboseOutput) {
            gcloud builds submit --tag $ImageTag --verbosity=debug
        } else {
            gcloud builds submit --tag $ImageTag
        }
        Write-Success "Container image built successfully"
    } catch {
        Write-Error "Failed to build container image: $($_.Exception.Message)"
        exit 1
    }
}

function Deploy-CloudRunService {
    param($ServiceName, $ImageTag, $Region, $EnvironmentVars)
    
    Write-Info "Deploying Cloud Run service: $ServiceName"
    Write-Info "Image: $ImageTag"
    Write-Info "Region: $Region"
    
    $deployArgs = @(
        "run", "deploy", $ServiceName,
        "--image", $ImageTag,
        "--platform", "managed",
        "--region", $Region,
        "--set-env-vars", $EnvironmentVars
    )
    
    # Add authentication flag if specified
    if ($AllowUnauthenticated) {
        $deployArgs += "--allow-unauthenticated"
        Write-Warning "Service will allow unauthenticated access"
    }
    
    # Add verbosity if specified
    if ($VerboseOutput) {
        $deployArgs += "--verbosity=debug"
    }
    
    try {
        & gcloud $deployArgs
        Write-Success "Cloud Run service deployed successfully"
        
        # Get service URL
        $serviceUrl = gcloud run services describe $ServiceName --region=$Region --format="value(status.url)"
        Write-Success "Service URL: $serviceUrl"
        
    } catch {
        Write-Error "Failed to deploy Cloud Run service: $($_.Exception.Message)"
        exit 1
    }
}

function Validate-Parameters {
    Write-Info "Validating deployment parameters..."
    
    # Validate required parameters
    if ([string]::IsNullOrEmpty($ProjectId)) {
        Write-Error "ProjectId parameter is required"
        exit 1
    }
    
    if ([string]::IsNullOrEmpty($ProcessorId) -and !$SkipBuild) {
        Write-Warning "ProcessorId not provided. Using placeholder value."
        $script:ProcessorId = "YOUR_PROCESSOR_ID_HERE"
    }
    
    # Set default image name if not provided
    if ([string]::IsNullOrEmpty($ImageName)) {
        $script:ImageName = "gcr.io/$ProjectId/auditoria360-backend"
    }
    
    Write-Success "Parameter validation completed"
    
    if ($VerboseOutput) {
        Write-Info "Deployment Configuration:"
        Write-Host "  Project ID: $ProjectId" -ForegroundColor Cyan
        Write-Host "  Region: $Region" -ForegroundColor Cyan
        Write-Host "  Service Name: $ServiceName" -ForegroundColor Cyan
        Write-Host "  Image Name: $ImageName" -ForegroundColor Cyan
        Write-Host "  Processor ID: $ProcessorId" -ForegroundColor Cyan
        Write-Host "  BigQuery Dataset: $BQDatasetId" -ForegroundColor Cyan
        Write-Host "  Text Bucket: $TextBucketName" -ForegroundColor Cyan
    }
}

# Main execution function
function Main {
    Write-Host "🚀 AUDITORIA360 Backend Deployment" -ForegroundColor Cyan
    Write-Host "==================================="
    
    try {
        # Validate input parameters
        Validate-Parameters
        
        # Check prerequisites
        Test-Prerequisites
        
        # Build environment variables string
        $envVars = "GCP_PROJECT_ID=$ProjectId,BQ_DATASET_ID=$BQDatasetId,CCT_TEXT_BUCKET_NAME=$TextBucketName,CCT_EXTRATOR_PROCESSOR_ID=$ProcessorId"
        
        # Build container image
        Build-ContainerImage -ImageTag $ImageName
        
        # Deploy to Cloud Run
        Deploy-CloudRunService -ServiceName $ServiceName -ImageTag $ImageName -Region $Region -EnvironmentVars $envVars
        
        Write-Host ""
        Write-Success "🎉 Backend deployment completed successfully!"
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Test the deployed service endpoint"
        Write-Host "2. Verify environment variables are correctly set"
        Write-Host "3. Check Cloud Run logs for any issues"
        Write-Host "4. Update frontend configuration if needed"
        
    } catch {
        Write-Error "Deployment failed: $($_.Exception.Message)"
        exit 1
    }
}

# Execute main function
Main
