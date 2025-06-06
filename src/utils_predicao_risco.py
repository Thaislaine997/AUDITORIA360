"""
Utilitário para integração com o serviço de predição de risco da folha (Vertex AI)
AUDITORIA360 – Módulo 3

- Função assíncrona para chamada ao endpoint de predição
- Tratamento de erros e logging
- Pronto para uso em controllers FastAPI ou background tasks
"""
import httpx
import logging
from typing import Dict, Any

PREDICAO_RISCO_URL = "http://localhost:8000/predicao/risco-folha"  # Ajuste para o endpoint real em produção

async def chamar_predicao_risco_folha(payload: Dict[str, Any], url: str = PREDICAO_RISCO_URL, timeout: int = 30) -> Dict[str, Any]:
    """
    Envia um payload de folha para o serviço de predição de risco e retorna o resultado.
    Lança exceção em caso de erro HTTP ou timeout.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logging.error(f"Erro ao chamar serviço de predição de risco: {e}")
        raise
