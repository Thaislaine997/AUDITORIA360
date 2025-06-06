import pandas as pd
from google.cloud import bigquery

def extrair_dados(query: str, project_id: str) -> pd.DataFrame:
    """
    Extrai dados do BigQuery com base na consulta SQL fornecida.

    Args:
        query (str): A consulta SQL para extrair os dados.
        project_id (str): O ID do projeto do Google Cloud.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados extraídos.
    """
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    results = query_job.result()
    return results.to_dataframe()

def extrair_dados_treinamento(project_id: str) -> pd.DataFrame:
    """
    Extrai dados para o treinamento do modelo de risco.

    Args:
        project_id (str): O ID do projeto do Google Cloud.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados de treinamento.
    """
    query = """
    SELECT *
    FROM `seu_dataset.seu_tabela_treinamento`
    """
    return extrair_dados(query, project_id)

def extrair_dados_predicoes(project_id: str) -> pd.DataFrame:
    """
    Extrai dados de predições de risco.

    Args:
        project_id (str): O ID do projeto do Google Cloud.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados de predições.
    """
    query = """
    SELECT *
    FROM `seu_dataset.seu_tabela_predicoes`
    """
    return extrair_dados(query, project_id)