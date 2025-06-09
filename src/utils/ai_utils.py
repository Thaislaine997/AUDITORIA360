# Arquivo movido de src/ai_utils.py
import os
from typing import Optional, Dict, Any
from .vertex_utils import prever_rubrica_com_vertex
from .gemini_utils import classificar_clausula_com_gemini

AI_PROVIDER = os.getenv("AI_PROVIDER", "vertex").lower()

def classificar_clausula(texto_clausula: str, provider: Optional[str] = None) -> Dict[str, Any]:
    prov = (provider or AI_PROVIDER).lower()
    if prov == "vertex":
        rubrica = prever_rubrica_com_vertex(texto_clausula)
        return {"rubrica": rubrica, "provider": "vertex"}
    elif prov == "gemini":
        resultado = classificar_clausula_com_gemini(texto_clausula)
        resultado["provider"] = "gemini"
        return resultado
    else:
        raise ValueError(f"Provedor de IA desconhecido: {prov}")
