import os
from sqlalchemy import create_engine
import boto3

# Teste conexão Neon
print('Testando conexão com o banco Neon...')
db_url = os.getenv('DATABASE_URL')
try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute("SELECT 1;")
        print('Conexão com Neon OK:', result.scalar())
except Exception as e:
    print('Erro ao conectar no Neon:', e)

# Teste conexão Cloudflare R2
print('\nTestando conexão com Cloudflare R2...')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
R2_SECRET_KEY = os.getenv('R2_SECRET_KEY')
R2_BUCKET = os.getenv('R2_BUCKET')
try:
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY
    )
    buckets = s3.list_buckets()
    print('Conexão com R2 OK. Buckets disponíveis:', [b['Name'] for b in buckets.get('Buckets', [])])
except Exception as e:
    print('Erro ao conectar no R2:', e)
