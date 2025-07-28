"""
Script de backup automatizado para Neon (PostgreSQL) e Cloudflare R2.
Requer: python-dotenv, boto3, sqlalchemy, psycopg2-binary
"""
import os
from dotenv import load_dotenv
import boto3
from sqlalchemy import create_engine
from datetime import datetime

load_dotenv()

# Backup do banco Neon (dump SQL)
def backup_neon():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise Exception("DATABASE_URL não definida!")
    dump_file = f"neon_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    os.system(f"pg_dump '{url}' > {dump_file}")
    return dump_file

# Upload para R2
def upload_to_r2(file_path):
    client = boto3.client(
        service_name='s3',
        endpoint_url=f"https://{os.getenv('CLOUDFLARE_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        region_name="auto"
    )
    bucket = os.getenv('R2_BUCKET_NAME')
    client.upload_file(file_path, bucket, os.path.basename(file_path))
    print(f"Backup enviado para R2: {file_path}")

if __name__ == "__main__":
    dump = backup_neon()
    upload_to_r2(dump)
