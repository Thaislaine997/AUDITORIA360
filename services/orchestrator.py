from services.ingestion.main import main as ingestion_main
from services.ml.pipeline_runner import run_pipeline
from services.ml.components.explainers import explain_model


def run_full_pipeline(event, context):
    """
    Orquestra a execução: ingestion → ML pipeline → explainability.
    """
    # 1. Ingestão
    ingestion_main(event, context)
    # 2. Pipeline ML via Prefect
    run_pipeline()
    # 3. Explainability (mock)
    explain_model(model=None, data=None)
    print("Pipeline completo executado.")
