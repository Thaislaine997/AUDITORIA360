#!/bin/bash
# auditoria_gcp.sh - Auditoria recorrente de recursos e permissões GCP para o projeto AUDITORIA360
# Uso: ./auditoria_gcp.sh > relatorio_auditoria_$(date +%Y%m%d).txt

PROJECT_ID="auditoria-folha"
LOGFILE="auditoria_gcp_$(date +%Y%m%d_%H%M%S).log"

echo "==== Auditoria GCP - Projeto: $PROJECT_ID ====" | tee $LOGFILE
echo "Data: $(date)" | tee -a $LOGFILE

echo -e "\n1. Instâncias Cloud SQL:" | tee -a $LOGFILE
gcloud sql instances list --project=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n2. Verificar bancos e usuários Cloud SQL:" | tee -a $LOGFILE
for INSTANCE in $(gcloud sql instances list --project=$PROJECT_ID --format="value(name)"); do
  echo "  > Banco: $INSTANCE" | tee -a $LOGFILE
  gcloud sql users list --instance=$INSTANCE --project=$PROJECT_ID | tee -a $LOGFILE
done

echo -e "\n3. Firewalls e regras de rede:" | tee -a $LOGFILE
gcloud compute firewall-rules list --project=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n4. Conectores VPC Serverless:" | tee -a $LOGFILE
gcloud compute networks vpc-access connectors list --project=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n5. Service Accounts vinculadas:" | tee -a $LOGFILE
gcloud iam service-accounts list --project=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n6. Permissões e papéis (IAM):" | tee -a $LOGFILE
gcloud projects get-iam-policy $PROJECT_ID --format="table(bindings.role,bindings.members)" | tee -a $LOGFILE

echo -e "\n7. Backups automáticos Cloud SQL:" | tee -a $LOGFILE
for INSTANCE in $(gcloud sql instances list --project=$PROJECT_ID --format="value(name)"); do
  echo "  > Banco: $INSTANCE" | tee -a $LOGFILE
  gcloud sql backups list --instance=$INSTANCE --project=$PROJECT_ID | tee -a $LOGFILE
done

echo -e "\n8. Datasets BigQuery:" | tee -a $LOGFILE
bq ls --project_id=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n9. Perfis Datastream:" | tee -a $LOGFILE
gcloud datastream connection-profiles list --project=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n10. Secret Manager:" | tee -a $LOGFILE
gcloud secrets list --project=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n11. Verificação de auditoria de logs:" | tee -a $LOGFILE
gcloud logging sinks list --project=$PROJECT_ID | tee -a $LOGFILE

echo -e "\n==== Auditoria Finalizada ====" | tee -a $LOGFILE