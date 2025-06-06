import re
import json
from typing import Optional # Adicionado Optional
from vertexai.preview.generative_models import GenerativeModel
from .log_utils import logger  # Supondo que log_utils está no mesmo nível

def _extrair_json_de_texto(texto: str) -> str:
    """
    Extrai um bloco JSON de uma string, procurando por ```json ... ``` ou ``` ... ```.
    Se um bloco é encontrado, seu conteúdo é retornado (mesmo que não seja JSON válido,
    ou "" se o bloco estiver vazio).
    Se nenhum bloco é encontrado, o texto original é retornado (após strip).
    """
    patterns = [
        r"```json\s*(.*?)\s*```",  # Procura por ```json ... ```
        r"```\s*(.*?)\s*```"      # Procura por ``` ... ``` (mais genérico)
    ]

    for pattern in patterns:
        match = re.search(pattern, texto, re.DOTALL)
        if match:
            candidate = match.group(1).strip()
            # Se um bloco de código foi encontrado (match), retornamos seu conteúdo.
            # Se o conteúdo do bloco estiver vazio (ex: ```json\n```), candidate será "".
            # Se o conteúdo não for JSON válido (ex: ```json\nINVALID\n```), candidate será "INVALID".
            # A função chamadora (classificar_clausula_com_gemini) lidará com json.loads().
            if not candidate:
                logger.debug(f"Bloco de código encontrado com padrão '{pattern}' estava vazio. Retornando string vazia.")
            else:
                logger.debug(f"Bloco de código encontrado com padrão '{pattern}'. Conteúdo candidato: '{candidate[:100]}...'")
            return candidate # Retorna o conteúdo do bloco (pode ser "", "VALID_JSON", ou "INVALID_JSON_FROM_BLOCK")

    # Se nenhum bloco de código ``` foi encontrado, o texto inteiro pode ser o JSON.
    # Retornamos o texto como está (strip para remover espaços em branco).
    # A função chamadora tentará json.loads() nele.
    logger.debug("Nenhum bloco de código ```...``` encontrado. Retornando texto original (strip) para tentativa de parse.")
    return texto.strip()

def classificar_clausula_com_gemini(texto_clausula: str) -> dict:
    model = GenerativeModel("gemini-pro")
    prompt = f"""Você é um classificador de cláusulas trabalhistas. Com base na cláusula abaixo, informe:
1. A rubrica correspondente (em MAIÚSCULO, formato técnico, como PISO_SALARIAL, HORA_EXTRA, REAJUSTE_PERC, INSALUBRIDADE etc)
2. Uma explicação curta da cláusula
3. Se for irrelevante ou genérica, retorne "OUTRAS"

Cláusula:
{texto_clausula}

Responda no formato JSON:
{{
  "rubrica": "...",
  "descricao": "..."
}}
"""
    try:
        resposta = model.generate_content(prompt)
        # Verificação robusta para o objeto de resposta e o atributo .text
        if resposta is None or not hasattr(resposta, 'text') or resposta.text is None:
            return {"erro": "Resposta do modelo inválida ou não contém atributo 'text' ou o texto é None."}

        text_content = resposta.text.strip()  # Faz strip uma vez no início

        json_text = _extrair_json_de_texto(text_content)  # Utiliza a função para extrair JSON

        if json_text:
            return json.loads(json_text)
        else:
            # Se json_text for None ou vazio após a extração (ou se text_content original era só whitespace)
            return {"erro": "Resposta do modelo vazia ou inválida após extração."}

    except json.JSONDecodeError as json_e:
        # Este bloco será alcançado se json_text não for um JSON válido
        return {"erro": f"Falha ao decodificar JSON da resposta do modelo: {json_e}", "resposta_bruta": resposta.text if hasattr(resposta, 'text') else str(resposta)}
    except Exception as e:  # Captura outras exceções inesperadas
        return {"erro": str(e)}

def gerar_dica_checklist_com_gemini(descricao_item_checklist: str, categoria_item: Optional[str] = None, criticidade_item: Optional[str] = None) -> dict:
    """
    Gera uma dica contextual para um item de checklist de fechamento de folha usando o Gemini.

    Args:
        descricao_item_checklist: A descrição do item do checklist.
        categoria_item: A categoria do item do checklist (opcional).
        criticidade_item: A criticidade do item do checklist (opcional).

    Returns:
        Um dicionário contendo a dica ou um erro. Ex: {"dica": "Verifique..."} ou {"erro": "..."}
    """
    model = GenerativeModel("gemini-pro") # Ou o modelo mais apropriado

    contexto_adicional = ""
    if categoria_item:
        contexto_adicional += f" Categoria do item: {categoria_item}."
    if criticidade_item:
        contexto_adicional += f" Criticidade do item: {criticidade_item}."

    prompt = f"""
    Você é um assistente especialista em fechamento de folha de pagamento no Brasil.
    Forneça uma dica prática e acionável para o seguinte item de um checklist de fechamento de folha:

    Item do Checklist: "{descricao_item_checklist}"
    {contexto_adicional}

    A dica deve ajudar o usuário a entender o que verificar ou como proceder para concluir este item.
    Seja conciso e direto ao ponto. Máximo de 2 frases.

    Exemplo de resposta:
    "Verifique se todos os lançamentos de férias foram corretamente importados e se os saldos batem com o sistema de ponto."

    Dica:
    """
    try:
        logger.info(f"Gerando dica para o item: '{descricao_item_checklist}'. Contexto: {contexto_adicional}")
        resposta = model.generate_content(prompt)

        if resposta is None or not hasattr(resposta, 'text') or not resposta.text:
            logger.error(f"Resposta do modelo inválida ou vazia para o item: {descricao_item_checklist}")
            return {"erro": "Resposta do modelo inválida ou vazia."}

        dica_gerada = resposta.text.strip()
        logger.info(f"Dica gerada para '{descricao_item_checklist}': {dica_gerada}")
        
        # Validação simples da dica (ex: não ser muito curta ou conter mensagens de erro do modelo)
        if len(dica_gerada) < 10 or "não posso ajudar" in dica_gerada.lower():
             logger.warning(f"Dica gerada para '{descricao_item_checklist}' parece inválida: {dica_gerada}")
             return {"erro": "A dica gerada parece inválida ou o modelo não pôde fornecer uma resposta útil."}

        return {"dica": dica_gerada}

    except Exception as e:
        logger.error(f"Erro ao gerar dica com Gemini para '{descricao_item_checklist}': {e}", exc_info=True)
        return {"erro": f"Erro ao contatar o serviço de IA: {str(e)}"}

def gerar_resposta_estruturada_gemini(prompt: str) -> str:
    """
    Gera uma resposta textual do Gemini, forçando o modelo a responder em JSON (ou markdown JSON).
    Retorna apenas o JSON extraído da resposta.
    """
    model = GenerativeModel("gemini-pro")
    resposta = model.generate_content(prompt)
    if resposta is None or not hasattr(resposta, 'text') or resposta.text is None:
        raise Exception("Resposta do modelo Gemini inválida ou vazia.")
    text_content = resposta.text.strip()
    json_text = _extrair_json_de_texto(text_content)
    return json_text
