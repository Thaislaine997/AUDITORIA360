"""
API Router for AI Development Assistant
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from ia_desenvolvimento.cerebro import create_ai_brain, CerebroAuditoria360

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Global AI brain instance (singleton pattern)
ai_brain: Optional[CerebroAuditoria360] = None


def get_ai_brain() -> CerebroAuditoria360:
    """Get or create the AI brain singleton."""
    global ai_brain
    if ai_brain is None:
        logger.info("🧠 Inicializando cérebro da IA pela primeira vez...")
        ai_brain = create_ai_brain()
    return ai_brain


class QueryRequest(BaseModel):
    """Request model for AI queries."""
    pergunta: str


class QueryResponse(BaseModel):
    """Response model for AI queries."""
    resposta: str
    status: str
    timestamp: float
    sources: List[Dict[str, str]] = []


class StatusResponse(BaseModel):
    """Response model for status checks."""
    database_exists: bool
    retrieval_ready: bool
    files_processed: int
    last_training: Optional[float]
    message: str


@router.post("/query", response_model=QueryResponse)
async def query_dev_assistant(request: QueryRequest):
    """
    Query the AI development assistant.
    
    Args:
        request: The query request containing the question
        
    Returns:
        QueryResponse: The AI's response with sources
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        if not request.pergunta.strip():
            raise HTTPException(
                status_code=400, 
                detail="Pergunta não pode estar vazia"
            )
        
        brain = get_ai_brain()
        result = brain.fazer_pergunta(request.pergunta)
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Erro na consulta ao assistente: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )


@router.get("/status", response_model=StatusResponse)
async def get_dev_assistant_status():
    """
    Get the current status of the AI development assistant.
    
    Returns:
        StatusResponse: Current status information
    """
    try:
        brain = get_ai_brain()
        status = brain.get_status()
        
        # Add descriptive message based on status
        if status["retrieval_ready"]:
            message = f"✅ Assistente ativo com {status['files_processed']} arquivos processados"
        elif status["database_exists"]:
            message = "⚠️ Base de dados existe mas sistema de recuperação não está pronto"
        else:
            message = "🔄 Assistente em modo básico - treinamento necessário"
        
        return StatusResponse(
            **status,
            message=message
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar status: {str(e)}"
        )


@router.post("/retrain")
async def retrain_assistant():
    """
    Retrain the AI assistant on the current codebase.
    
    Returns:
        dict: Status of retraining operation
    """
    try:
        global ai_brain
        logger.info("🔄 Iniciando retreinamento do assistente...")
        
        # Force recreation of the AI brain to retrain
        ai_brain = None
        
        # This will trigger retraining
        brain = get_ai_brain()
        
        status = brain.get_status()
        
        return {
            "message": "✅ Retreinamento concluído com sucesso!",
            "files_processed": status["files_processed"],
            "retrieval_ready": status["retrieval_ready"],
            "timestamp": status["last_training"]
        }
        
    except Exception as e:
        logger.error(f"❌ Erro durante retreinamento: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro durante retreinamento: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": "AI Development Assistant",
        "version": "1.0.0"
    }