import streamlit as st
import requests
import json

st.set_page_config(page_title="Sugestões de Impacto das CCTs", layout="wide")
st.title("Sugestões de Impacto das CCTs - Revisão e Aprovação")

API_URL = st.secrets.get("API_URL") or "http://localhost:8000"

# Filtros iniciais
id_cliente = st.text_input("ID do Cliente (para filtrar)")
id_cct_documento = st.text_input("ID do Documento CCT (opcional)")

if st.button("Buscar Sugestões Pendentes"):
    with st.spinner("Buscando sugestões..."):
        params = {}
        if id_cliente:
            params["id_cliente_afetado"] = id_cliente
        if id_cct_documento:
            params["id_cct_documento_fk"] = id_cct_documento
        try:
            r = requests.get(f"{API_URL}/api/v1/ccts/sugestoes-impacto", params=params)
            r.raise_for_status()
            sugestoes = r.json()
        except Exception as e:
            st.error(f"Erro ao buscar sugestões: {e}")
            sugestoes = []

    if not sugestoes:
        st.info("Nenhuma sugestão pendente encontrada.")
    else:
        for sugestao in sugestoes:
            with st.expander(f"Sugestão {sugestao['id_sugestao_impacto']} - {sugestao['tipo_sugestao']}"):
                st.markdown(f"**Cláusula Base:** {sugestao['texto_clausula_cct_base']}")
                st.markdown(f"**Justificativa IA:** {sugestao['justificativa_sugestao_ia']}")
                st.markdown(f"**Data de Vigência Sugerida:** {sugestao['data_inicio_vigencia_sugerida']}")
                st.markdown(f"**Status:** {sugestao['status_sugestao']}")
                # Campos editáveis conforme tipo
                dados_editados = {}
                if sugestao['tipo_sugestao'] == 'ALTERACAO_RUBRICA_CLIENTE':
                    st.markdown(f"**Rubrica Afetada:** {sugestao['codigo_rubrica_cliente_existente']}")
                    alteracoes = json.loads(sugestao['json_alteracoes_sugeridas_rubrica'])
                    for alt in alteracoes:
                        novo_valor = st.text_input(f"{alt['campo_a_alterar']}", value=str(alt['novo_valor_sugerido']), key=f"{sugestao['id_sugestao_impacto']}_{alt['campo_a_alterar']}")
                        alt['novo_valor_sugerido'] = novo_valor
                    dados_editados['json_alteracoes_sugeridas_rubrica'] = json.dumps(alteracoes)
                elif sugestao['tipo_sugestao'] == 'NOVA_RUBRICA_CLIENTE':
                    dados_editados['codigo_sugerido_nova_rubrica'] = st.text_input("Código Nova Rubrica", value=sugestao['codigo_sugerido_nova_rubrica'])
                    dados_editados['descricao_sugerida_nova_rubrica'] = st.text_input("Descrição Nova Rubrica", value=sugestao['descricao_sugerida_nova_rubrica'])
                    dados_editados['tipo_sugerido_nova_rubrica'] = st.text_input("Tipo Nova Rubrica", value=sugestao['tipo_sugerido_nova_rubrica'])
                    dados_editados['natureza_esocial_sugerida'] = st.text_input("Natureza eSocial", value=sugestao['natureza_esocial_sugerida'])
                    incidencias = json.loads(sugestao['json_sugestao_incidencias_completa_nova_rubrica'])
                    for k, v in incidencias.items():
                        incidencias[k] = st.text_input(f"{k}", value=str(v), key=f"{sugestao['id_sugestao_impacto']}_{k}")
                    dados_editados['json_sugestao_incidencias_completa_nova_rubrica'] = json.dumps(incidencias)
                elif sugestao['tipo_sugestao'].startswith('ATUALIZACAO_PARAMETRO_LEGAL'):
                    dados_editados['novo_valor_sugerido_parametro'] = st.text_input("Novo Valor Sugerido", value=sugestao['novo_valor_sugerido_parametro'])
                # Notas e ações
                notas = st.text_area("Notas de Revisão", key=f"notas_{sugestao['id_sugestao_impacto']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Aprovar e Aplicar", key=f"aprovar_{sugestao['id_sugestao_impacto']}"):
                        payload = {
                            "acao_usuario": "APROVAR_APLICAR",
                            "usuario_revisao": st.session_state.get("usuario", "admin"),
                            "notas_revisao_usuario": notas,
                            "dados_sugestao_atualizados_json": json.dumps(dados_editados) if dados_editados else None
                        }
                        try:
                            r = requests.post(f"{API_URL}/api/v1/ccts/sugestoes-impacto/{sugestao['id_sugestao_impacto']}/processar", json=payload)
                            r.raise_for_status()
                            st.success("Sugestão aprovada e aplicada com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao aprovar: {e}")
                with col2:
                    if st.button("Rejeitar", key=f"rejeitar_{sugestao['id_sugestao_impacto']}"):
                        payload = {
                            "acao_usuario": "REJEITAR",
                            "usuario_revisao": st.session_state.get("usuario", "admin"),
                            "notas_revisao_usuario": notas,
                            "dados_sugestao_atualizados_json": None
                        }
                        try:
                            r = requests.post(f"{API_URL}/api/v1/ccts/sugestoes-impacto/{sugestao['id_sugestao_impacto']}/processar", json=payload)
                            r.raise_for_status()
                            st.success("Sugestão rejeitada com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao rejeitar: {e}")
