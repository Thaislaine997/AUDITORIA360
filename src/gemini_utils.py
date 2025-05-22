import google.generativeai as genai
import json
import re
import os
from typing import Optional

try:
    from google.generativeai.generative_models import GenerativeModel
except ImportError:
    GenerativeModel = None

MODEL_NAME = "gemini-pro"

def _extrair_json_de_texto(texto: str) -> dict:
    match = re.search(r"```json\s*(\{.*?\})\s*```", texto, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        match_direct = re.search(r"(\{.*?\})", texto, re.DOTALL)
        if match_direct:
            json_str = match_direct.group(1)
        else:
            return {}
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}

def gerar_descricao_da_clausula_com_gemini(texto_clausula: str, rubrica_identificada: Optional[str] = None) -> dict:
    if GenerativeModel is None:
        return {"erro": "A classe GenerativeModel não está disponível na sua versão da biblioteca google-generativeai. Atualize a biblioteca ou ajuste o código para o novo SDK python-genai."}
    prompt_parts = [
        "Você é um assistente especialista em legislação trabalhista e interpretação de cláusulas contratuais.",
        "Analise a seguinte cláusula trabalhista:",
        f"--- CLÁUSULA ---\n{texto_clausula}\n--- FIM DA CLÁUSULA ---",
    ]
    if rubrica_identificada:
        prompt_parts.extend([
            f"Esta cláusula foi identificada como pertencente à rubrica: '{rubrica_identificada}'.",
            "Forneça uma descrição clara e concisa sobre o que esta cláusula implica para o trabalhador e para o empregador, considerando a rubrica fornecida.",
            "A resposta deve ser um objeto JSON com a chave 'descricao'."
        ])
        json_structure_example = '\nExemplo de formato da resposta JSON esperada: {"descricao": "Explicação detalhada da cláusula..."}'
    else:
        prompt_parts.extend([
            "Identifique a principal rubrica trabalhista relacionada a esta cláusula e forneça uma descrição clara e concisa sobre o que esta cláusula implica.",
            "A resposta deve ser um objeto JSON com as chaves 'rubrica' e 'descricao'."
        ])
        json_structure_example = '\nExemplo de formato da resposta JSON esperada: {"rubrica": "Nome da Rubrica", "descricao": "Explicação detalhada da cláusula..."}'
    prompt_parts.append(json_structure_example)
    prompt = "\n\n".join(prompt_parts)
    try:
        model = GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        resultado_json = _extrair_json_de_texto(response.text)
        if not resultado_json:
            if not rubrica_identificada:
                return {"rubrica": "Não identificada", "descricao": response.text or "Não foi possível gerar descrição."}
            return {"descricao": response.text or "Não foi possível gerar descrição."}
        return resultado_json
    except Exception as e:
        if not rubrica_identificada:
            return {"rubrica": "Erro", "descricao": f"Erro ao contatar o Gemini: {str(e)}"}
        return {"descricao": f"Erro ao contatar o Gemini: {str(e)}"}

def classificar_clausula_com_gemini(texto_clausula: str) -> dict:
    if GenerativeModel is None:
        return {"erro": "A classe GenerativeModel não está disponível na sua versão da biblioteca google-generativeai. Atualize a biblioteca ou ajuste o código para o novo SDK python-genai."}
    prompt = f"""
    Analise a seguinte cláusula de um contrato ou acordo trabalhista e me forneça a rubrica correspondente em formato técnico e uma breve descrição.
    A resposta DEVE ser um objeto JSON com as chaves "rubrica" e "descricao".

    Texto da cláusula:
    "{texto_clausula}"

    Exemplo de formato da resposta JSON esperada:
    {{
      "rubrica": "HORAS EXTRAS",
      "descricao": "Pagamento adicional por horas trabalhadas além da jornada normal."
    }}
    """
    try:
        model = GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        resultado_json = _extrair_json_de_texto(response.text)
        if not resultado_json or "rubrica" not in resultado_json or "descricao" not in resultado_json:
            return {"rubrica": "Verificar manualmente", "descricao": response.text or "Resposta não obtida."}
        return resultado_json
    except Exception as e:
        return {"rubrica": "Erro", "descricao": f"Erro ao contatar o Gemini: {str(e)}"}
    return {"rubrica": "Erro", "descricao": "Erro desconhecido ao classificar cláusula."}
