
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_r2_client():
    r2_client = boto3.client(
        service_name='s3',
        endpoint_url=f"https://{os.getenv('CLOUDFLARE_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
        region_name="auto"
    )
    return r2_client

def upload_file_to_r2(file_path: str, object_name: str):
    client = get_r2_client()
    bucket_name = os.getenv('R2_BUCKET_NAME')
    client.upload_file(file_path, bucket_name, object_name)
    print(f"Arquivo '{file_path}' enviado para '{object_name}' no R2.")
