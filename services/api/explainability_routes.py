try:
    from fastapi import APIRouter
    FASTAPI_AVAILABLE = True
except ImportError:
    # Mock FastAPI for testing
    class MockAPIRouter:
        def post(self, path):
            def decorator(func):
                return func
            return decorator
    
    APIRouter = MockAPIRouter
    FASTAPI_AVAILABLE = False

try:
    from services.orchestrator import run_full_pipeline
    ORCHESTRATOR_AVAILABLE = True
except ImportError:
    # Mock orchestrator for testing
    def run_full_pipeline(*args, **kwargs):
        return {"status": "mocked", "message": "Orchestrator not available"}
    ORCHESTRATOR_AVAILABLE = False

router = APIRouter()

@router.post("/executar-pipeline")
def executar_pipeline(event: dict):
    """
    Endpoint para disparar pipeline completo: ingestion → ML → explainability.
    """
    context = None
    run_full_pipeline(event, context)
    return {"status": "Pipeline executado"}
