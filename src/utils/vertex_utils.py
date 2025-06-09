from google.cloud import aiplatform
import os

# --- Configurações e variáveis de ambiente ---
ENDPOINT_ID = os.getenv("VERTEX_ENDPOINT_ID", "vertex-cct-endpoint")
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")
LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")

_vertex_initialized = False

# --- Funções utilitárias do Vertex AI (unificadas) ---
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

        if not prediction.predictions:
            return "Erro na predição da rubrica: Nenhuma predição retornada."
        primeira_predicao = prediction.predictions[0]
        rubrica_prevista = primeira_predicao.get('displayName')
        if rubrica_prevista is None:
            return "Rubrica não encontrada na predição."
        return rubrica_prevista
    except Exception as e:
        return f"Erro na predição da rubrica: {e}"

# --- Funções genéricas do Vertex AI ---
def init_vertex_ai(project: str, location: str):
    aiplatform.init(project=project, location=location)

def create_endpoint(display_name: str) -> str:
    endpoint = aiplatform.Endpoint.create(display_name=display_name)
    return endpoint.name

def deploy_model_to_endpoint(endpoint_id: str, model_id: str, traffic_percentage: int = 100):
    endpoint = aiplatform.Endpoint(endpoint_id)
    model = aiplatform.Model(model_id)
    endpoint.deploy(model=model, traffic_percentage=traffic_percentage)

def predict_with_endpoint(endpoint_id: str, instances: list):
    endpoint = aiplatform.Endpoint(endpoint_id)
    prediction = endpoint.predict(instances=instances)
    return prediction

def list_models() -> list:
    return aiplatform.Model.list()