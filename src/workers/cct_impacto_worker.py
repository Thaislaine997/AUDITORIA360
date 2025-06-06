"""
Worker para análise de impacto das cláusulas de CCTs sobre rubricas e parâmetros legais dos clientes.
Gera sugestões de atualização (BigQuery: CCTsSugestoesImpacto) usando Gemini e integrações.
"""
import os
import uuid
import json
from datetime import datetime
from src.utils import bq_utils
from src.gemini_utils import gerar_resposta_estruturada_gemini

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "seu-projeto-gcp")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "auditoria_folha_dataset")
bq = bq_utils.BigQueryUtils(PROJECT_ID)

async def analisar_impacto_cct_para_clientes(id_cct_documento: str):
    print(f"Iniciando análise de impacto para CCT Documento ID: {id_cct_documento}")
    # Atualizar status do documento para 'EM_ANALISE_DE_IMPACTO'
    # bq.run_query(f"UPDATE {BQ_DATASET_ID}.CCTsDocumentos SET status_processamento_ia='EM_ANALISE_DE_IMPACTO' WHERE id_cct_documento='{id_cct_documento}'")

    # 1. Buscar cláusulas aprovadas
    clausulas_aprovadas = bq.query(f"""
        SELECT id_clausula_extraida, tipo_clausula_identificada, texto_clausula_extraido
        FROM {BQ_DATASET_ID}.CCTsClausulasExtraidas
        WHERE id_cct_documento_fk='{id_cct_documento}' AND status_revisao='APROVADA'
    """)
    if not clausulas_aprovadas:
        # bq.run_query(f"UPDATE {BQ_DATASET_ID}.CCTsDocumentos SET status_processamento_ia='ANALISE_IMPACTO_CONCLUIDA_SEM_CLAUSULAS' WHERE id_cct_documento='{id_cct_documento}'")
        return

    # 2. Buscar clientes afetados
    clientes_afetados = bq.query(f"""
        SELECT id_cliente_afetado FROM {BQ_DATASET_ID}.CCTsClientesAfetados WHERE id_cct_documento_fk='{id_cct_documento}'
    """)
    ids_clientes = [c['id_cliente_afetado'] for c in clientes_afetados]

    # 3. Buscar info da CCT
    cct_info = bq.query(f"""
        SELECT nome_documento_original, data_inicio_vigencia_cct FROM {BQ_DATASET_ID}.CCTsDocumentos WHERE id_cct_documento='{id_cct_documento}'
    """)
    cct_info = cct_info[0] if cct_info else {}

    sugestoes_para_inserir = []

    for id_cliente in ids_clientes:
        # Buscar rubricas do cliente
        rubricas_cliente = bq.query(f"""
            SELECT codigo_rubrica_cliente, descricao_rubrica_cliente, incide_inss_empregado, incide_irrf, incide_fgts_mensal, tipo_rubrica_cliente
            FROM {BQ_DATASET_ID}.DicionarioRubricasCliente
            WHERE id_cliente='{id_cliente}'
        """)
        rubricas_prompt = [
            f"- Código: {r['codigo_rubrica_cliente']}, Descrição: {r['descricao_rubrica_cliente']}, INSS: {r['incide_inss_empregado']}, IRRF: {r['incide_irrf']}, FGTS: {r['incide_fgts_mensal']}, Tipo: {r['tipo_rubrica_cliente']}"
            for r in rubricas_cliente
        ]
        rubricas_contexto = "\n".join(rubricas_prompt)

        for clausula in clausulas_aprovadas:
            prompt = f"""
            Você é um especialista em legislação trabalhista e parametrização de folha de pagamento no Brasil.\n\nAnalise a cláusula extraída da CCT '{cct_info.get('nome_documento_original','')}' (ID: {clausula['id_clausula_extraida']}), vigência geral: {cct_info.get('data_inicio_vigencia_cct','')}.\n\nCláusula (Tipo: {clausula['tipo_clausula_identificada']}):\n\"{clausula['texto_clausula_extraido']}\"\n\nRubricas ATUAIS do cliente ID '{id_cliente}':\n{rubricas_contexto}\n\nResponda em JSON com as chaves:\n- sugestoes_alteracao_rubricas_cliente\n- sugestoes_novas_rubricas_cliente\n- sugestoes_atualizacao_parametros_legais\n"""
            resposta = gerar_resposta_estruturada_gemini(prompt)
            try:
                sugestoes_json = json.loads(resposta)
            except Exception as e:
                print(f"Erro ao decodificar resposta Gemini: {e}\nPrompt: {prompt}\nResposta: {resposta}")
                continue
            # Processar sugestões e montar objetos para inserção
            for alt in sugestoes_json.get('sugestoes_alteracao_rubricas_cliente', []):
                sugestoes_para_inserir.append({
                    "id_sugestao_impacto": str(uuid.uuid4()),
                    "id_cct_documento_fk": id_cct_documento,
                    "id_clausula_extraida_fk": clausula['id_clausula_extraida'],
                    "id_cliente_afetado": id_cliente,
                    "tipo_sugestao": "ALTERACAO_RUBRICA_CLIENTE",
                    "codigo_rubrica_cliente_existente": alt.get("codigo_rubrica_cliente_afetada"),
                    "json_alteracoes_sugeridas_rubrica": json.dumps(alt.get("alteracoes_campos", [])),
                    "texto_clausula_cct_base": clausula['texto_clausula_extraido'][:1000],
                    "justificativa_sugestao_ia": alt.get("justificativa_mudanca_cct"),
                    "data_inicio_vigencia_sugerida": alt.get("data_inicio_vigencia_mudanca"),
                    "timestamp_geracao_sugestao": datetime.now().isoformat()
                })
            for nova in sugestoes_json.get('sugestoes_novas_rubricas_cliente', []):
                sugestoes_para_inserir.append({
                    "id_sugestao_impacto": str(uuid.uuid4()),
                    "id_cct_documento_fk": id_cct_documento,
                    "id_clausula_extraida_fk": clausula['id_clausula_extraida'],
                    "id_cliente_afetado": id_cliente,
                    "tipo_sugestao": "NOVA_RUBRICA_CLIENTE",
                    "codigo_sugerido_nova_rubrica": nova.get("codigo_sugerido_nova_rubrica"),
                    "descricao_sugerida_nova_rubrica": nova.get("descricao_sugerida_nova_rubrica"),
                    "tipo_sugerido_nova_rubrica": nova.get("tipo_rubrica_sugerido"),
                    "natureza_esocial_sugerida": nova.get("natureza_esocial_sugerida"),
                    "json_sugestao_incidencias_completa_nova_rubrica": json.dumps(nova.get("sugestao_configuracao_incidencias_completa", {})),
                    "texto_clausula_cct_base": clausula['texto_clausula_extraido'][:1000],
                    "justificativa_sugestao_ia": nova.get("justificativa_criacao_cct"),
                    "data_inicio_vigencia_sugerida": nova.get("data_inicio_vigencia_nova_rubrica"),
                    "timestamp_geracao_sugestao": datetime.now().isoformat()
                })
            for param in sugestoes_json.get('sugestoes_atualizacao_parametros_legais', []):
                sugestoes_para_inserir.append({
                    "id_sugestao_impacto": str(uuid.uuid4()),
                    "id_cct_documento_fk": id_cct_documento,
                    "id_clausula_extraida_fk": clausula['id_clausula_extraida'],
                    "id_cliente_afetado": id_cliente,
                    "tipo_sugestao": "ATUALIZACAO_PARAMETRO_LEGAL_GERAL",
                    "nome_parametro_afetado": param.get("nome_parametro_afetado"),
                    "contexto_parametro": param.get("contexto_parametro"),
                    "novo_valor_sugerido_parametro": str(param.get("novo_valor_parametro")),
                    "unidade_parametro": param.get("unidade_parametro"),
                    "texto_clausula_cct_base": clausula['texto_clausula_extraido'][:1000],
                    "justificativa_sugestao_ia": param.get("justificativa_parametro_cct"),
                    "data_inicio_vigencia_sugerida": param.get("data_inicio_vigencia_parametro"),
                    "timestamp_geracao_sugestao": datetime.now().isoformat()
                })
    if sugestoes_para_inserir:
        bq.insert_rows_json(f"{BQ_DATASET_ID}.CCTsSugestoesImpacto", sugestoes_para_inserir)
        print(f"Inseridas {len(sugestoes_para_inserir)} sugestões de impacto.")
    # Atualizar status do documento para 'IMPACTO_ANALISADO_PENDENTE_REVISAO_USUARIO'
    # bq.run_query(f"UPDATE {BQ_DATASET_ID}.CCTsDocumentos SET status_processamento_ia='IMPACTO_ANALISADO_PENDENTE_REVISAO_USUARIO' WHERE id_cct_documento='{id_cct_documento}'")
    print(f"Análise de impacto concluída para CCT {id_cct_documento}.")
