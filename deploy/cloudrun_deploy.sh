#!/bin/bash
# Deploy automatizado para Google Cloud Run
PROJECT_ID=$(gcloud config get-value project)
gcloud builds submit --tag gcr.io/$PROJECT_ID/auditoria360

gcloud run deploy auditoria360 \
  --image gcr.io/$PROJECT_ID/auditoria360 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
