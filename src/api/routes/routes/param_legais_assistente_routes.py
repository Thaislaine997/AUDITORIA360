"""
Rotas para o assistente IA de atualização legal de parâmetros.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from src.bq_loader import get_bigquery_client
from uuid import uuid4
from datetime import datetime, timezone
import hashlib
import json
from typing import Optional
from src.schemas_assistente import SugestaoAtualizacaoParametros, AprovarSugestaoPayload, RejeitarSugestaoPayload
from src.vertex_utils import prever_rubrica_com_vertex
from src.gemini_utils import gerar_dica_checklist_com_gemini

router = APIRouter(
    prefix="/api/v1/parametros/assistente-atualizacao",
    tags=["Assistente Atualização Legal"]
)

def hash_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

@router.post("/analisar-documento", summary="Analisa documento legal e gera sugestão IA", status_code=201)
async def analisar_documento(
    tipo_parametro: str = Form(..., description="Tipo de parâmetro legal afetado (ex: INSS, IRRF, FGTS, Salário Mínimo, etc)"),
    usuario_solicitante: str = Form(..., description="Usuário que está solicitando a análise"),
    arquivo: UploadFile = File(None),
    texto_manual: str = Form(None, description="Texto legal colado manualmente")
):
    """
    Analisa um documento legal (PDF/TXT) ou texto colado, extrai parâmetros regulatórios relevantes (INSS, IRRF, FGTS, etc.)
    e sugere atualização para tabelas do sistema, usando IA (Vertex + Gemini). O prompt é otimizado para máxima precisão.
    """
    if not arquivo and not texto_manual:
        raise HTTPException(status_code=400, detail="Envie um arquivo ou cole um texto para análise.")

    # 1. Extrair texto do arquivo ou usar texto_manual
    if arquivo:
        conteudo = await arquivo.read()
        try:
            texto_extraido = conteudo.decode("utf-8")
        except Exception:
            texto_extraido = "[Arquivo binário recebido. Extração real de PDF não implementada neste mock.]"
        nome_documento = arquivo.filename
    else:
        texto_extraido = texto_manual
        nome_documento = "texto_manual.txt"

    texto_hash = hash_texto(texto_extraido or "")

    # 2. Prompt aprimorado para IA (Vertex + Gemini)
    try:
        # Prompt detalhado para Vertex (classificação)
        prompt_vertex = f"""
        Você é um assistente jurídico especialista em legislação trabalhista e tributária brasileira.
        Analise o texto a seguir, identifique o TIPO DE PARÂMETRO REGULATÓRIO afetado (ex: INSS, IRRF, FGTS, Salário Mínimo, Salário Família, etc) e, se possível, a NATUREZA DA ATUALIZAÇÃO (ex: nova tabela, alteração de faixa, novo valor, vigência, etc).
        Extraia o parâmetro principal e retorne apenas o nome técnico do parâmetro (ex: INSS, IRRF, FGTS, SALARIO_MINIMO, SALARIO_FAMILIA).
        Texto legal/documento:
        """
        prompt_vertex += f"\n--- INÍCIO DO TEXTO ---\n{texto_extraido}\n--- FIM DO TEXTO ---"
        rubrica_vertex = prever_rubrica_com_vertex(prompt_vertex)

        # Prompt detalhado para Gemini (extração de dados e explicação)
        prompt_gemini = f"""
        Você é um assistente jurídico especialista em legislação trabalhista e tributária brasileira.
        Sua tarefa é analisar o texto legal/documento abaixo e extrair, de forma estruturada, os parâmetros regulatórios relevantes para atualização de sistemas de folha de pagamento.
        Siga as instruções:
        - Identifique o tipo de parâmetro (ex: INSS, IRRF, FGTS, Salário Mínimo, Salário Família, etc).
        - Extraia os valores, faixas, datas de vigência, percentuais, tetos, deduções, e demais campos relevantes para o parâmetro identificado.
        - Sempre que possível, retorne um objeto JSON com os campos: tipo_parametro, data_inicio_vigencia, data_fim_vigencia, faixas (se aplicável), valor_nacional, valores_regionais, aliquotas, deducoes, teto, observacao, etc.
        - Explique em linguagem natural, de forma resumida, o que mudou e o impacto da atualização.
        - Se o texto não contiver dados suficientes, retorne um JSON com "erro": "Não foi possível extrair parâmetros suficientes".
        Exemplo de resposta esperada:
        ```json
        {
          "tipo_parametro": "INSS",
          "data_inicio_vigencia": "2025-05-01",
          "data_fim_vigencia": null,
          "faixas": [
            {"valor_inicial": 0, "valor_final": 1412.00, "aliquota": 7.5},
            {"valor_inicial": 1412.01, "valor_final": 2666.68, "aliquota": 9.0}
          ],
          "valor_teto_contribuicao": 7500.00,
          "observacao": "Tabela INSS 2025 publicada no DOU em 22/05/2025."
        }
        ```
        Texto legal/documento:
        --- INÍCIO DO TEXTO ---
        {texto_extraido}
        --- FIM DO TEXTO ---
        """
        descricao_gemini = gerar_dica_checklist_com_gemini(prompt_gemini, categoria_item=rubrica_vertex)
        if isinstance(descricao_gemini, dict):
            descricao_ia = descricao_gemini.get("descricao") or descricao_gemini
        else:
            descricao_ia = descricao_gemini
        dados_sugeridos = {
            "parametro_classificado": rubrica_vertex,
            "dados_extraidos": descricao_ia,
            "data_inicio_vigencia": str(datetime.now().date()),
            "data_fim_vigencia": None
        }
        resumo_ia = f"Sugestão IA para {tipo_parametro}: {rubrica_vertex} - {descricao_ia if isinstance(descricao_ia,str) else str(descricao_ia)[:200]}"
    except Exception as e:
        dados_sugeridos = {
            "exemplo_parametro": "valor extraído pela IA",
            "data_inicio_vigencia": str(datetime.now().date()),
            "data_fim_vigencia": None,
            "erro": str(e)
        }
        resumo_ia = f"Sugestão mock para {tipo_parametro} extraída do documento {nome_documento}. Erro IA: {e}"

    # 3. Validação e pós-processamento dos dados extraídos
    validacao = {"erros": [], "avisos": [], "campos_obrigatorios": ["tipo_parametro", "data_inicio_vigencia"]}
    if isinstance(dados_sugeridos.get("dados_extraidos"), dict):
        dados = dados_sugeridos["dados_extraidos"]
    else:
        try:
            dados = json.loads(dados_sugeridos.get("dados_extraidos", "{}")) if isinstance(dados_sugeridos.get("dados_extraidos"), str) else {}
        except Exception:
            dados = {}
    for campo in validacao["campos_obrigatorios"]:
        if not dados.get(campo):
            validacao["erros"].append(f"Campo obrigatório ausente: {campo}")
    # Corrige tipos básicos
    if "faixas" in dados and isinstance(dados["faixas"], list):
        for faixa in dados["faixas"]:
            for k in ["valor_inicial", "valor_final", "aliquota"]:
                if k in faixa and isinstance(faixa[k], str):
                    try:
                        faixa[k] = float(faixa[k].replace(",", "."))
                    except Exception:
                        validacao["avisos"].append(f"Faixa com valor inválido para {k}: {faixa[k]}")
    # NOVO: Validação cruzada com tipo_parametro identificado pela IA
    tipo_param_extraido = dados.get("tipo_parametro")
    if tipo_param_extraido and tipo_param_extraido.upper() != tipo_parametro.upper():
        validacao["avisos"].append(f"Tipo de parâmetro extraído ('{tipo_param_extraido}') difere do informado pelo usuário ('{tipo_parametro}').")
    dados_sugeridos["dados_extraidos"] = dados
    dados_sugeridos["validacao"] = validacao

    client = get_bigquery_client(config_dict={"gcp_project_id": "auditoria-folha", "service_account_key_path_local_dev": None})
    id_sugestao = str(uuid4())
    agora = datetime.now(timezone.utc).isoformat()
    row = {
        "id_sugestao": id_sugestao,
        "tipo_parametro": tipo_parametro,
        "dados_sugeridos_json": json.dumps(dados_sugeridos, ensure_ascii=False),
        "nome_documento_fonte": nome_documento,
        "texto_documento_fonte_hash": texto_hash,
        "status_sugestao": "pendente",
        "data_sugestao": agora,
        "resumo_ia_sugestao": resumo_ia,
        "usuario_solicitante": usuario_solicitante,
        "justificativa_rejeicao": None,
        "data_aprovacao": None,
        "usuario_aprovador": None
    }
    table_id = "auditoria-folha.dataset_auditoria.SugestoesAtualizacaoParametros"
    errors = client.insert_rows_json(table_id, [row])
    if errors:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar sugestão no BigQuery: {errors}")

    return {"id_sugestao": id_sugestao, "resumo_ia": resumo_ia, "dados_sugeridos": dados_sugeridos}

@router.get("/sugestoes", response_model=list[SugestaoAtualizacaoParametros], summary="Lista sugestões IA para revisão")
async def listar_sugestoes(status: Optional[str] = None):
    client = get_bigquery_client(config_dict={"gcp_project_id": "auditoria-folha", "service_account_key_path_local_dev": None})
    query = f"""
        SELECT * FROM `auditoria-folha.dataset_auditoria.SugestoesAtualizacaoParametros`
        {f'WHERE status_sugestao = "{status}"' if status else ''}
        ORDER BY data_sugestao DESC
        LIMIT 100
    """
    rows = list(client.query(query))
    sugestoes = []
    for row in rows:
        sugestoes.append(SugestaoAtualizacaoParametros(**dict(row)))
    return sugestoes

@router.post("/sugestoes/{id_sugestao}/aprovar", summary="Aprova sugestão IA")
async def aprovar_sugestao(id_sugestao: str, payload: AprovarSugestaoPayload):
    client = get_bigquery_client(config_dict={"gcp_project_id": "auditoria-folha", "service_account_key_path_local_dev": None})
    query = f"""
        UPDATE `auditoria-folha.dataset_auditoria.SugestoesAtualizacaoParametros`
        SET status_sugestao = 'aprovada', data_aprovacao = CURRENT_TIMESTAMP(), usuario_aprovador = @usuario_aprovador
        WHERE id_sugestao = @id_sugestao
    """
    from google.cloud import bigquery
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_sugestao", "STRING", id_sugestao),
            bigquery.ScalarQueryParameter("usuario_aprovador", "STRING", payload.usuario_aprovador)
        ]
    )
    client.query(query, job_config=job_config).result()
    return {"status": "ok", "id_sugestao": id_sugestao}

@router.post("/sugestoes/{id_sugestao}/rejeitar", summary="Rejeita sugestão IA")
async def rejeitar_sugestao(id_sugestao: str, payload: RejeitarSugestaoPayload):
    client = get_bigquery_client(config_dict={"gcp_project_id": "auditoria-folha", "service_account_key_path_local_dev": None})
    query = f"""
        UPDATE `auditoria-folha.dataset_auditoria.SugestoesAtualizacaoParametros`
        SET status_sugestao = 'rejeitada', justificativa_rejeicao = @justificativa, data_aprovacao = CURRENT_TIMESTAMP(), usuario_aprovador = @usuario_aprovador
        WHERE id_sugestao = @id_sugestao
    """
    from google.cloud import bigquery
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_sugestao", "STRING", id_sugestao),
            bigquery.ScalarQueryParameter("usuario_aprovador", "STRING", payload.usuario_aprovador),
            bigquery.ScalarQueryParameter("justificativa", "STRING", payload.justificativa_rejeicao)
        ]
    )
    client.query(query, job_config=job_config).result()
    return {"status": "ok", "id_sugestao": id_sugestao}
