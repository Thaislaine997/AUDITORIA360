import os
from sqlalchemy import create_engine, text
import boto3
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

print('Testando conexão com o banco Neon...')
db_url = os.getenv('DATABASE_URL')
if not db_url:
    print('DATABASE_URL não encontrada no ambiente!')
else:
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print('Conexão com Neon OK:', result.scalar())
    except Exception as e:
        print('Erro ao conectar no Neon:', e)

print('\nTestando conexão com Cloudflare R2...')
R2_ENDPOINT = os.getenv('R2_ENDPOINT')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
R2_SECRET_KEY = os.getenv('R2_SECRET_KEY')
R2_BUCKET = os.getenv('R2_BUCKET')
if not all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET]):
    print('Alguma variável do R2 não encontrada no ambiente!')
else:
    if len(R2_ACCESS_KEY) != 32:
        print(f'R2_ACCESS_KEY deve ter 32 caracteres, mas tem {len(R2_ACCESS_KEY)}. Corrija no .env!')
    else:
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
