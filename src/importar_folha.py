import streamlit as st
from datetime import datetime
import time # Para simular o polling
import requests # Para futuras chamadas de API

# Placeholder para a URL base da API (deve ser configurada)
API_BASE_URL = "http://localhost:8000/api/v1" # Exemplo, ajuste conforme necessário

# Placeholder para obter o ID do cliente logado
# Em um cenário real, isso viria do sistema de autenticação
def get_logged_in_client_id():
    # Tenta obter do session_state, se já logado e armazenado lá
    if 'cliente_id' in st.session_state and st.session_state.cliente_id:
        return st.session_state.cliente_id
    # Fallback para um valor padrão para desenvolvimento, ou poderia levantar um erro/redirecionar
    st.warning("ID do cliente não encontrado no session_state, usando valor padrão 'CLIENTE_TESTE_01'. Faça login para obter o ID correto.")
    return "CLIENTE_TESTE_01"

def mostrar_pagina_importar_folha():
    st.title("📄 Importação de Folha de Pagamento")

    id_cliente = get_logged_in_client_id()
    if not id_cliente:
        st.error("Não foi possível identificar o cliente. Por favor, faça login novamente.")
        return

    st.write(f"Cliente ID: `{id_cliente}`") # Apenas para depuração

    # Usar o primeiro dia do mês atual como padrão
    default_date = datetime.now().replace(day=1)
    
    # O widget date_input retorna um objeto date.
    # Para exibir MM/YYYY, precisaríamos de um componente customizado ou aceitar a seleção do dia.
    # Por simplicidade, vamos usar o date_input padrão e o usuário seleciona qualquer dia do mês desejado.
    # O backend pode normalizar para o primeiro dia do mês se necessário.
    periodo_referencia_dt = st.date_input(
        "🗓️ Mês/Ano de Referência da Folha:",
        value=default_date,
        # format="MM/YYYY", # format não é suportado diretamente para exibição, mas para parsing.
        help="Selecione qualquer dia do mês de referência. O sistema considerará o mês/ano."
    )

    uploaded_pdf = st.file_uploader("Selecione o PDF da folha de pagamento:", type=["pdf"])

    if 'job_id' not in st.session_state:
        st.session_state.job_id = None
    if 'job_status' not in st.session_state:
        st.session_state.job_status = None
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None

    if uploaded_pdf and periodo_referencia_dt:
        if st.button("🚀 Processar PDF da Folha", key="processar_pdf"):
            st.session_state.job_id = None # Resetar job_id anterior
            st.session_state.job_status = "INICIANDO"
            st.session_state.error_message = None
            
            # Normalizar periodo_referencia para o primeiro dia do mês (formato YYYY-MM-DD)
            periodo_referencia_str = periodo_referencia_dt.replace(day=1).strftime("%Y-%m-%d")

            files = {'file': (uploaded_pdf.name, uploaded_pdf, uploaded_pdf.type)}
            payload = {'periodo_referencia': periodo_referencia_str}
            
            try:
                with st.spinner(f"Enviando arquivo {uploaded_pdf.name} para processamento..."):
                    # Simulação de chamada de API para iniciar o processamento
                    # response = requests.post(f"{API_BASE_URL}/clientes/{id_cliente}/folhas/importar-pdf-async", files=files, data=payload)
                    # response.raise_for_status()
                    # st.session_state.job_id = response.json().get("job_id")
                    
                    # Simulação para desenvolvimento sem backend real
                    st.session_state.job_id = f"sim_job_{int(time.time())}" 
                    st.success(f"Arquivo enviado. Job ID: {st.session_state.job_id}. Iniciando monitoramento...")
                    st.session_state.job_status = "PENDENTE"

            except requests.exceptions.RequestException as e:
                st.session_state.error_message = f"Erro ao enviar arquivo: {e}"
                st.session_state.job_status = "FALHA_ENVIO"
            except Exception as e:
                st.session_state.error_message = f"Ocorreu um erro inesperado: {e}"
                st.session_state.job_status = "FALHA_ENVIO"

    if st.session_state.job_id and st.session_state.job_status not in ["FALHA_ENVIO", "CONCLUIDO_SUCESSO", "FALHA_PROCESSAMENTO", "CONCLUIDO_COM_PENDENCIAS"]:
        with st.spinner(f"Processando Job ID: {st.session_state.job_id} - Status: {st.session_state.job_status}..."):
            # Simulação de polling de status
            time.sleep(5) # Simula o tempo de espera da API
            
            # Lógica de simulação de atualização de status
            # Em um cenário real, faria uma chamada GET para /status/{job_id}
            # current_status_response = requests.get(f"{API_BASE_URL}/clientes/{id_cliente}/folhas/importar-pdf-async/status/{st.session_state.job_id}")
            # current_status_response.raise_for_status()
            # status_data = current_status_response.json()
            # st.session_state.job_status = status_data.get("status_job")
            # st.session_state.error_message = status_data.get("detalhes_erro")
            
            # Simulação de progressão de status
            if st.session_state.job_status == "PENDENTE":
                st.session_state.job_status = "PROCESSANDO_DOCAI"
            elif st.session_state.job_status == "PROCESSANDO_DOCAI":
                st.session_state.job_status = "PROCESSANDO_MAPEAMENTO"
            elif st.session_state.job_status == "PROCESSANDO_MAPEAMENTO":
                # Simular um resultado aleatório
                if time.time() % 2 == 0:
                    st.session_state.job_status = "CONCLUIDO_SUCESSO"
                else:
                    st.session_state.job_status = "CONCLUIDO_COM_PENDENCIAS"
                    st.session_state.error_message = "Algumas rubricas não foram mapeadas automaticamente. Verifique os detalhes."
            
            st.rerun() # Força o rerun para atualizar o spinner e o status

    if st.session_state.job_status:
        if st.session_state.job_status == "FALHA_ENVIO":
            st.error(f"Falha no envio do arquivo: {st.session_state.error_message}")
        elif st.session_state.job_status == "FALHA_PROCESSAMENTO":
            st.error(f"Falha no processamento do Job ID {st.session_state.job_id}: {st.session_state.error_message}")
        elif st.session_state.job_status == "CONCLUIDO_SUCESSO":
            st.success(f"Job ID {st.session_state.job_id} processado com sucesso!")
            # Aqui você poderia adicionar um link para ver os resultados ou o dashboard da folha
        elif st.session_state.job_status == "CONCLUIDO_COM_PENDENCIAS":
            st.warning(f"Job ID {st.session_state.job_id} processado com pendências: {st.session_state.error_message}")
            # Guiar usuário para ação, ex: mapear rubricas
        
        # Botão para limpar o status e permitir novo upload
        if st.button("Limpar Status e Iniciar Nova Importação", key="limpar_status"):
            st.session_state.job_id = None
            st.session_state.job_status = None
            st.session_state.error_message = None
            st.rerun()

def upload_pdf_and_track_status():
    st.subheader("Upload de PDF e Acompanhamento de Status")

    # Upload do arquivo PDF
    uploaded_file = st.file_uploader("Faça o upload do arquivo PDF da folha de pagamento:", type=["pdf"])

    if uploaded_file is not None:
        st.write("Arquivo carregado com sucesso! Iniciando o processamento...")

        # Simular envio para o backend
        with st.spinner("Enviando arquivo para processamento..."):
            # Placeholder para chamada de API
            response = requests.post(
                f"{API_BASE_URL}/processar-pdf",
                files={"file": uploaded_file},
                data={"cliente_id": get_logged_in_client_id()}
            )

            if response.status_code == 200:
                job_id = response.json().get("job_id")
                st.success(f"Processamento iniciado! ID do Job: {job_id}")

                # Polling para acompanhar o status do job
                with st.spinner("Acompanhando o status do processamento..."):
                    while True:
                        status_response = requests.get(f"{API_BASE_URL}/status-job/{job_id}")
                        if status_response.status_code == 200:
                            status = status_response.json().get("status")
                            if status == "COMPLETED":
                                st.success("Processamento concluído com sucesso!")
                                break
                            elif status == "FAILED":
                                st.error("O processamento falhou. Verifique os logs para mais detalhes.")
                                break
                            else:
                                st.info(f"Status atual: {status}. Aguardando...")
                        time.sleep(5)  # Aguardar antes de verificar novamente
            else:
                st.error("Erro ao iniciar o processamento. Tente novamente.")

# Adicionar a funcionalidade à página principal
upload_pdf_and_track_status()

if __name__ == '__main__':
    # Para testar esta página isoladamente
    # Certifique-se de ter uma forma de definir st.session_state.cliente_id se necessário
    # Exemplo: st.session_state.cliente_id = "CLIENTE_TESTE_01"
    mostrar_pagina_importar_folha()
