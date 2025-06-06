from google.cloud import aiplatform

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