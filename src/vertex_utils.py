from google.cloud import aiplatform
import os

ENDPOINT_ID = os.getenv("VERTEX_ENDPOINT_ID", "vertex-cct-endpoint")  # Idealmente via config
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")  # Ou do config
LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")

_vertex_initialized = False

def inicializar_vertex():
    global _vertex_initialized
    if not _vertex_initialized:
        aiplatform.init(project=PROJECT_ID, location=LOCATION)
        _vertex_initialized = True


def prever_rubrica_com_vertex(texto_clausula: str) -> str:
    """
    Envia uma cláusula para o endpoint da Vertex AI para prever a rubrica.
    """
    try:
        inicializar_vertex()
        endpoint = aiplatform.Endpoint(
            endpoint_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
        )
        instances = [{"content": texto_clausula}]
        prediction = endpoint.predict(instances=instances)

        if prediction is None:
            return "Erro na predição da rubrica: A predição retornou None."

        if not prediction.predictions:  # Checa se a lista de predições está vazia
            return "Erro na predição da rubrica: Nenhuma predição retornada."
            
        # Acessa o primeiro item da lista de predições
        primeira_predicao = prediction.predictions[0]
        
        # Checa se 'displayName' existe no dicionário da primeira predição
        rubrica_prevista = primeira_predicao.get('displayName')
        if rubrica_prevista is None:
            return "Rubrica não encontrada na predição."  # Mensagem mais específica
            
        return rubrica_prevista
        
    except Exception as e:
        # Log detalhado do erro pode ser útil aqui
        # import logging
        # logging.exception("Erro detalhado em prever_rubrica_com_vertex")
        return f"Erro na predição da rubrica: {e}"
