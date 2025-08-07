# /auditoria360/src/lib/supabase_client.py

from supabase import create_client, Client, create_async_client, AsyncClient
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

async def get_supabase_async_client() -> AsyncClient:
    """
    Cria e retorna uma instância assíncrona do cliente Supabase.
    Usa a Service Key para operações de backend com privilégios de administrador.
    Esta função será usada como uma dependência no FastAPI para operações assíncronas.
    """
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_SERVICE_KEY
    
    return await create_async_client(url, key)