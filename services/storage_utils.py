# Utilitário para integração com Cloudflare R2 via boto3
import boto3
import os

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")

R2_BUCKET = os.getenv("R2_BUCKET")
if not R2_BUCKET:
    raise ValueError("A variável de ambiente R2_BUCKET não está definida. Verifique seu .env!")

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY
)

def upload_arquivo(nome_arquivo, caminho_local):
    s3.upload_file(caminho_local, R2_BUCKET, nome_arquivo)

def download_arquivo(nome_arquivo, caminho_destino):
    s3.download_file(R2_BUCKET, nome_arquivo, caminho_destino)
