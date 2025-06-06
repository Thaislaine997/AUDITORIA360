# Script PowerShell para build e deploy do backend no Cloud Run
$project = "SEU_PROJECT_ID"
$region = "us-central1"
$img = "gcr.io/$project/auditoria360-backend"
$service = "auditoria360-backend"
$envVars = "GCP_PROJECT_ID=$project,BQ_DATASET_ID=auditoria_folha_dataset,CCT_TEXT_BUCKET_NAME=auditoria360-ccts-textos-extraidos,CCT_EXTRATOR_PROCESSOR_ID=SEU_PROCESSOR_ID_DOCAI"

gcloud builds submit --tag $img

gcloud run deploy $service `
  --image $img `
  --platform managed `
  --region $region `
  --allow-unauthenticated `
  --set-env-vars $envVars
