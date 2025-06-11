# Arquivo movido de src/gemini_utils.py
import re
import json
import sys
import os
from typing import Optional
from vertexai.preview.generative_models import GenerativeModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.log_utils import logger

def _extrair_json_de_texto(texto: str) -> str:
    patterns = [
        r"```json\s*(.*?)\s*```",
        r"```\s*(.*?)\s*```"
    ]
    for pattern in patterns:
        match = re.search(pattern, texto, re.DOTALL)
        if match:
            candidate = match.group(1).strip()
            if not candidate:
                logger.debug(f"Bloco de código encontrado com padrão '{pattern}' estava vazio. Retornando string vazia.")
            else:
                logger.debug(f"Bloco de código encontrado com padrão '{pattern}'. Conteúdo candidato: '{candidate[:100]}...'")
            return candidate
    logger.debug("Nenhum bloco de código ```...``` encontrado. Retornando texto original (strip) para tentativa de parse.")
    return texto.strip()

def classificar_clausula_com_gemini(texto_clausula: str) -> dict:
    model = GenerativeModel("gemini-pro")
    prompt = f"""Você é um classificador de cláusulas trabalhistas. Com base na cláusula abaixo, informe:\n1. A rubrica correspondente (em MAIÚSCULO, formato técnico, como PISO_SALARIAL, HORA_EXTRA, REAJUSTE_PERC, INSALUBRIDADE etc)\n2. Uma explicação curta da cláusula\n3. Se for irrelevante ou genérica, retorne \"OUTRAS\"\n\nCláusula:\n{texto_clausula}\n\nResponda no formato JSON:\n{{\n  \"rubrica\": \"...\",\n  \"descricao\": \"...\"\n}}\n"""
    try:
        resposta = model.generate_content(prompt)
        if resposta is None or not hasattr(resposta, 'text') or resposta.text is None:
            return {"erro": "Resposta do modelo inválida ou não contém atributo 'text' ou o texto é None."}
        text_content = resposta.text.strip()
        json_text = _extrair_json_de_texto(text_content)
        if json_text:
            return json.loads(json_text)
        else:
            return {"erro": "Resposta do modelo vazia ou inválida após extração."}
    except json.JSONDecodeError as json_e:
        return {"erro": f"Falha ao decodificar JSON da resposta do modelo: {json_e}", "resposta_bruta": resposta.text if hasattr(resposta, 'text') else str(resposta)}
    except Exception as e:
        return {"erro": str(e)}

def gerar_dica_checklist_com_gemini(prompt: str, categoria_item: Optional[str] = None) -> str:
    """
    Gera uma dica de checklist usando o modelo Gemini.
    """
    model = GenerativeModel("gemini-pro")
    prompt_final = prompt
    if categoria_item:
        prompt_final += f"\nCategoria: {categoria_item}"
    try:
        resposta = model.generate_content(prompt_final)
        if resposta is None or not hasattr(resposta, 'text') or resposta.text is None:
            return "Dica não disponível."
        return resposta.text.strip()
    except Exception as e:
        return f"Erro ao gerar dica com Gemini: {e}"
