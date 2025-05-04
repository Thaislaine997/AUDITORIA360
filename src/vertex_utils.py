
from google.cloud import aiplatform
from typing import Optional

# Inicialização global (ajustar seu ID de projeto e localização)
PROJECT_ID = "auditoria-folha"
LOCATION = "us-central1"
ENDPOINT_ID = "vertex-cct-endpoint"  # Substitua pelo seu endpoint real
MODEL_NAME = "modelo-cct-regras"     # Nome lógico do seu modelo Vertex

def inicializar_vertex():
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

def prever_rubrica_com_vertex(texto_clausula: str) -> Optional[str]:
    try:
        inicializar_vertex()
        endpoint = aiplatform.Endpoint(endpoint_name=ENDPOINT_ID)

        response = endpoint.predict(instances=[{"content": texto_clausula}])

        if response and hasattr(response, "predictions"):
            prediction = response.predictions[0]
            predicted_label = prediction.get("displayNames", [""])[0]
            return predicted_label
        else:
            return None
    except Exception as e:
        print(f"[ERRO Vertex] {e}")
        return None
