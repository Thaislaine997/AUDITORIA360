# Auditoria RH 360

Sistema para análise de folhas de pagamento e CCTs com integração a Google Cloud, Document AI e Streamlit.

## Estrutura
- /src → Aplicação principal
- /config → Configuração de ambiente e autenticação
- /deploy → cloudbuild.yaml para deploy no GCP
- /scripts → Script para gerar .exe no Windows

## Deploy
Use `gcloud builds submit --config deploy/cloudbuild.yaml`.

## Offline
Execute `scripts/compilar_instalador_windows.bat`.
