import requests
import streamlit as st

# import src.frontend.components.obrigacoes_componentes  # TODO: implementar ou ajustar caminho
# import src.frontend.utils.auth  # TODO: implementar ou ajustar caminho
# import src.frontend.utils.config  # TODO: implementar ou ajustar caminho

st.title("Obrigações e Prazos")


def obter_token():
    return st.text_input("Token JWT", type="password")


def get_obrigacoes(token):
    url = "http://localhost:8000/api/obrigacoes"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json(), url, headers
    except Exception as e:
        st.error(f"Erro ao buscar obrigações: {e}")
        return [], url, headers


token = obter_token()
if token:
    obrigacoes, url, headers = get_obrigacoes(token)
    filtro = st.text_input("Buscar por obrigação")
    obrigacoes_filtradas = [
        o for o in obrigacoes if filtro.lower() in o.get("descricao", "").lower()
    ]
    st.write(obrigacoes_filtradas)
    with st.form("Adicionar Obrigação"):
        descricao = st.text_input("Descrição")
        prazo = st.text_input("Prazo")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            payload = {"descricao": descricao, "prazo": prazo}
            resp = requests.post(url, json=payload, headers=headers)
            if resp.status_code == 201:
                st.success("Obrigação adicionado com sucesso!")
            else:
                st.error(f"Erro ao adicionar obrigação: {resp.text}")
else:
    st.warning("Informe o token JWT para acessar os dados.")
