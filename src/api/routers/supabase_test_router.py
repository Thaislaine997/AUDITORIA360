# /auditoria360/src/api/routers/supabase_test_router.py

from fastapi import APIRouter, HTTPException
import logging

# Direct import to avoid circular dependencies
try:
    from supabase import Client, create_client
    from config.settings import settings
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logging.warning("Supabase not available - install supabase library")

def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client instance.
    Uses the Service Key for backend operations with admin privileges.
    """
    if not SUPABASE_AVAILABLE:
        raise ImportError("Supabase library not available")
    
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_SERVICE_KEY
    
    return create_client(url, key)

router = APIRouter(
    prefix="/v1/test",
    tags=["Testes de Integração"],
)

@router.get("/supabase-connection", summary="Verifica a conexão com a base de dados Supabase")
def test_supabase_connection():
    """
    Endpoint de teste para verificar a conexão com a base de dados Supabase.
    Tenta buscar todos os registos da tabela 'Empresas'.
    """
    if not SUPABASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Supabase library not available"
        )
    
    try:
        logging.info("A tentar conectar-se à Supabase e a buscar dados da tabela 'Empresas'...")
        
        supabase = get_supabase_client()
        response = supabase.from_("Empresas").select("*").execute()
        
        logging.info(f"Resposta da Supabase recebida.")
        # A API devolve uma lista em 'data' mesmo que esteja vazia.
        return {
            "status": "Sucesso",
            "message": f"Conexão com a Supabase bem-sucedida! {len(response.data)} registos encontrados na tabela 'Empresas'.",
            "data": response.data,
        }

    except Exception as e:
        logging.error(f"Falha na conexão ou consulta à Supabase: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Falha crítica na comunicação com a Supabase: {str(e)}"
        )