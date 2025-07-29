"""
Script de restauração automatizada do backup Neon (PostgreSQL) a partir do Cloudflare R2.
Requer: python-dotenv, boto3
"""

import os
from dotenv import load_dotenv
import boto3

load_dotenv()


def download_from_r2(object_name, dest_path):
    client = boto3.client(
        service_name="s3",
        endpoint_url=f"https://{os.getenv('CLOUDFLARE_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
        region_name="auto",
    )
    bucket = os.getenv("R2_BUCKET_NAME")
    client.download_file(bucket, object_name, dest_path)
    print(f"Backup baixado de R2: {dest_path}")


def restore_neon(sql_file):
    url = os.getenv("DATABASE_URL")
    if not url:
        raise Exception("DATABASE_URL não definida!")
    os.system(f"psql '{url}' < {sql_file}")


if __name__ == "__main__":
    # Exemplo de uso: python restore_neon_r2.py nome_do_backup.sql
    import sys

    if len(sys.argv) < 2:
        print("Uso: python restore_neon_r2.py nome_do_backup.sql")
        exit(1)
    backup_file = sys.argv[1]
    download_from_r2(backup_file, backup_file)
    restore_neon(backup_file)
