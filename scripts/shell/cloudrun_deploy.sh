#!/bin/bash
# Deploy automatizado para Google Cloud Run
PROJECT_ID=$(gcloud config get-value project)
gcloud builds submit --tag gcr.io/$PROJECT_ID/auditoria360

gcloud run deploy auditoria360 \
  --image gcr.io/$PROJECT_ID/auditoria360 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances "auditoria-folha:us-central1:auditoria360portal" \
  --set-env-vars "CLOUD_SQL_DB_NAME=auditoria_db" \
  --set-env-vars "CLOUD_SQL_DB_USER=datastream_user" \
  --set-env-vars "CLOUD_SQL_DB_PASSWORD=41283407"
