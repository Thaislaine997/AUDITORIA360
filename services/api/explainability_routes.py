from fastapi import APIRouter
from services.orchestrator import run_full_pipeline

router = APIRouter()

@router.post("/executar-pipeline")
def executar_pipeline(event: dict):
    """
    Endpoint para disparar pipeline completo: ingestion → ML → explainability.
    """
    context = None
    run_full_pipeline(event, context)
    return {"status": "Pipeline executado"}
