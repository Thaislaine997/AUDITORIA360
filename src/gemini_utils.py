
from vertexai.preview.generative_models import GenerativeModel

def classificar_clausula_com_gemini(texto_clausula: str) -> dict:
    model = GenerativeModel("gemini-pro")
    prompt = f"""
Você é um classificador de cláusulas trabalhistas. Com base na cláusula abaixo, informe:
1. A rubrica correspondente (em MAIÚSCULO, formato técnico, como PISO_SALARIAL, HORA_EXTRA, REAJUSTE_PERC, INSALUBRIDADE etc)
2. Uma explicação curta da cláusula
3. Se for irrelevante ou genérica, retorne "OUTRAS"

Cláusula:
"""
{texto_clausula}
"""

Responda no formato JSON:
{{
  "rubrica": "...",
  "descricao": "..."
}}
"""
    try:
        resposta = model.generate_content(prompt)
        return resposta.text
    except Exception as e:
        return {"erro": str(e)}
