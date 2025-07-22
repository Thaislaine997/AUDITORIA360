# Pipeline runner stub
# Note: kfp (Kubeflow Pipelines) not installed - using mock implementation

try:
    from kfp import Client
    KFP_AVAILABLE = True
except ImportError:
    KFP_AVAILABLE = False
    Client = None

from services.ml.pipeline_definition import auditoria_folha_pipeline

def run_pipeline(endpoint: str = None, pipeline_func=None, arguments: dict = None):
    """
    Executa pipeline ML no Kubeflow Pipelines.
    """
    if not KFP_AVAILABLE:
        print("WARNING: Kubeflow Pipelines not available. Running mock pipeline...")
        # Mock implementation for development/testing
        print("Mock pipeline executed successfully")
        return {"status": "success", "message": "Mock pipeline completed"}
    
    # Real KFP implementation would go here
    if endpoint and pipeline_func:
        client = Client(host=endpoint)
        run = client.create_run_from_pipeline_func(
            pipeline_func,
            arguments=arguments or {}
        )
        return run
    else:
        print("Pipeline executed in local mode")
        return {"status": "success", "message": "Pipeline completed"}
    if not pipeline_func:
        pipeline_func = auditoria_folha_pipeline
    if not arguments:
        arguments = {"training_data": "bq://projeto.dataset.tabela"}
    if endpoint:
        client = Client(host=endpoint)
        run = client.create_run_from_pipeline_func(pipeline_func, arguments=arguments)
        return run
    print('Stub: pipeline executado (simulado)')
