# Script PowerShell para build e deploy do Streamlit no Cloud Run
$project = "SEU_PROJECT_ID"
$region = "us-central1"
$img = "gcr.io/$project/auditoria360-streamlit"
$service = "auditoria360-streamlit"
$apiUrl = "https://URL_DO_BACKEND"

gcloud builds submit --tag $img --file deploy/Dockerfile.streamlit

gcloud run deploy $service `
  --image $img `
  --platform managed `
  --region $region `
  --allow-unauthenticated `
  --set-env-vars "API_BASE_URL=$apiUrl"
