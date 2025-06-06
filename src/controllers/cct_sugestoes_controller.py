"""
Controller para processar ações do usuário sobre sugestões de impacto de CCTs.
"""
from src.utils import bq_utils
from datetime import datetime
import json

async def processar_sugestao_usuario(id_sugestao_impacto: str, payload):
    bq = bq_utils.BigQueryUtils(project_id="auditoria-folha")
    # Buscar sugestão original
    sugestao_db = bq.query(f"""
        SELECT * FROM auditoria_folha_dataset.CCTsSugestoesImpacto WHERE id_sugestao_impacto='{id_sugestao_impacto}'
    """)
    if not sugestao_db:
        return {"erro": "Sugestão não encontrada."}
    sugestao_db = sugestao_db[0]
    if sugestao_db["status_sugestao"] != 'PENDENTE_REVISAO_USUARIO':
        return {"erro": "Esta sugestão já foi processada."}

    dados_para_aplicar = json.loads(payload.dados_sugestao_atualizados_json) if payload.dados_sugestao_atualizados_json else sugestao_db

    if payload.acao_usuario == "REJEITAR":
        bq.run_query(f"""
            UPDATE auditoria_folha_dataset.CCTsSugestoesImpacto SET status_sugestao='REJEITADA_USUARIO',
            usuario_revisao_sugestao='{payload.usuario_revisao}', data_revisao_sugestao=TIMESTAMP('{datetime.now().isoformat()}'),
            notas_revisao_sugestao='{payload.notas_revisao_usuario or ''}'
            WHERE id_sugestao_impacto='{id_sugestao_impacto}'
        """)
        return {"message": "Sugestão rejeitada com sucesso."}

    elif payload.acao_usuario == "APROVAR_APLICAR":
        # Aqui seria chamada a integração com o Módulo 1
        sucesso_aplicacao_modulo1 = True
        status_final = 'APLICADA_COM_SUCESSO' if dados_para_aplicar == sugestao_db else 'APLICADA_COM_AJUSTES'
        bq.run_query(f"""
            UPDATE auditoria_folha_dataset.CCTsSugestoesImpacto SET status_sugestao='{status_final}',
            usuario_revisao_sugestao='{payload.usuario_revisao}', data_revisao_sugestao=TIMESTAMP('{datetime.now().isoformat()}'),
            notas_revisao_sugestao='{payload.notas_revisao_usuario or ''}',
            json_dados_editados_pelo_usuario='{payload.dados_sugestao_atualizados_json or ''}'
            WHERE id_sugestao_impacto='{id_sugestao_impacto}'
        """)
        return {"message": "Sugestão aplicada com sucesso!"}

    return {"erro": "Ação de usuário inválida."}
