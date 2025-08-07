# /auditoria360/src/lib/supabase_client.py

from supabase import create_client, Client
from config.settings import settings

def get_supabase_client() -> Client:
    """
    Cria e retorna uma instância do cliente Supabase.
    Usa a Service Key para operações de backend com privilégios de administrador.
    Esta função será usada como uma dependência no FastAPI.
    """
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_SERVICE_KEY
    
    return create_client(url, key)