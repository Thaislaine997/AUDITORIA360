# Pipeline runner stub


from prefect import flow, task
from services.ml.pipeline_definition import auditoria_folha_pipeline


@task
def run_auditoria_pipeline(arguments=None):
    if not arguments:
        arguments = {"training_data": "bq://projeto.dataset.tabela"}
    # Chama a função do pipeline diretamente
    result = auditoria_folha_pipeline(**arguments)
    print("Pipeline ML executado via Prefect.")
    return result


@flow
def pipeline_flow(arguments=None):
    return run_auditoria_pipeline(arguments)


def run_pipeline(arguments=None):
    """
    Executa pipeline ML usando Prefect Flow.
    """
    return pipeline_flow(arguments)
