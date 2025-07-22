# Pipeline runner stub


from kfp import Client
from services.ml.pipeline_definition import auditoria_folha_pipeline

def run_pipeline(endpoint: str = None, pipeline_func=None, arguments: dict = None):
    """
    Executa pipeline ML no Kubeflow Pipelines.
    """
    if not pipeline_func:
        pipeline_func = auditoria_folha_pipeline
    if not arguments:
        arguments = {"training_data": "bq://projeto.dataset.tabela"}
    if endpoint:
        client = Client(host=endpoint)
        run = client.create_run_from_pipeline_func(pipeline_func, arguments=arguments)
        return run
    print('Stub: pipeline executado (simulado)')
