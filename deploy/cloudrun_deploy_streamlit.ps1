# AUDITORIA360 - Streamlit Frontend Deployment Script for Google Cloud Run
# This script builds and deploys the Streamlit frontend to Google Cloud Run
# Requires: gcloud CLI installed and authenticated

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$true)]
    [string]$ApiBaseUrl,
    
    [string]$Region = "us-central1",
    
    [string]$ServiceName = "auditoria360-streamlit",
    
    [string]$ImageName = "",
    
    [string]$DockerfilePath = "deploy/Dockerfile.streamlit",
    
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
    if (!(Test-Path $DockerfilePath)) {
        Write-Error "Dockerfile not found at: $DockerfilePath"
        exit 1
    }
    
    Write-Success "Prerequisites check passed"
}

function Test-ApiEndpoint {
    param($ApiUrl)
    
    Write-Info "Testing API endpoint connectivity..."
    
    try {
        # Test if API URL is reachable (basic format validation)
        if ($ApiUrl -notmatch '^https?://') {
            Write-Warning "API URL should start with http:// or https://"
        }
        
        # Try to reach the API health endpoint if possible
        try {
            $healthUrl = "$ApiUrl/health"
            $response = Invoke-WebRequest -Uri $healthUrl -Method GET -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Success "API endpoint is reachable and healthy"
            }
        } catch {
            Write-Warning "Could not verify API health endpoint, but will proceed with deployment"
        }
        
    } catch {
        Write-Warning "API endpoint validation failed, but deployment will continue"
    }
}

function Build-ContainerImage {
    param($ImageTag, $DockerfilePath)
    
    if ($SkipBuild) {
        Write-Info "Skipping container build (--SkipBuild flag)"
        return
    }
    
    Write-Info "Building container image: $ImageTag"
    Write-Info "Using Dockerfile: $DockerfilePath"
    
    try {
        if ($VerboseOutput) {
            gcloud builds submit --tag $ImageTag --file $DockerfilePath --verbosity=debug
        } else {
            gcloud builds submit --tag $ImageTag --file $DockerfilePath
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
        "--set-env-vars", $EnvironmentVars,
        "--port", "8501"  # Default Streamlit port
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
        Write-Success "Frontend URL: $serviceUrl"
        
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
    
    if ([string]::IsNullOrEmpty($ApiBaseUrl)) {
        Write-Error "ApiBaseUrl parameter is required"
        exit 1
    }
    
    # Set default image name if not provided
    if ([string]::IsNullOrEmpty($ImageName)) {
        $script:ImageName = "gcr.io/$ProjectId/auditoria360-streamlit"
    }
    
    # Validate Dockerfile path
    if (!(Test-Path $DockerfilePath)) {
        Write-Error "Dockerfile not found at path: $DockerfilePath"
        exit 1
    }
    
    Write-Success "Parameter validation completed"
    
    if ($VerboseOutput) {
        Write-Info "Deployment Configuration:"
        Write-Host "  Project ID: $ProjectId" -ForegroundColor Cyan
        Write-Host "  Region: $Region" -ForegroundColor Cyan
        Write-Host "  Service Name: $ServiceName" -ForegroundColor Cyan
        Write-Host "  Image Name: $ImageName" -ForegroundColor Cyan
        Write-Host "  API Base URL: $ApiBaseUrl" -ForegroundColor Cyan
        Write-Host "  Dockerfile Path: $DockerfilePath" -ForegroundColor Cyan
    }
}

# Main execution function
function Main {
    Write-Host "🎨 AUDITORIA360 Frontend Deployment" -ForegroundColor Cyan
    Write-Host "===================================="
    
    try {
        # Validate input parameters
        Validate-Parameters
        
        # Check prerequisites
        Test-Prerequisites
        
        # Test API endpoint connectivity
        Test-ApiEndpoint -ApiUrl $ApiBaseUrl
        
        # Build environment variables string
        $envVars = "API_BASE_URL=$ApiBaseUrl"
        
        # Build container image
        Build-ContainerImage -ImageTag $ImageName -DockerfilePath $DockerfilePath
        
        # Deploy to Cloud Run
        Deploy-CloudRunService -ServiceName $ServiceName -ImageTag $ImageName -Region $Region -EnvironmentVars $envVars
        
        Write-Host ""
        Write-Success "🎉 Frontend deployment completed successfully!"
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Access the frontend URL and test the application"
        Write-Host "2. Verify API connectivity from the frontend"
        Write-Host "3. Check Cloud Run logs for any issues"
        Write-Host "4. Test authentication and key features"
        Write-Host "5. Update DNS/domain configuration if needed"
        
    } catch {
        Write-Error "Deployment failed: $($_.Exception.Message)"
        exit 1
    }
}

# Execute main function
Main
