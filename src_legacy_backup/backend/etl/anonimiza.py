from google.cloud import bigquery
import pandas as pd

def anonimiza_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Anonimiza dados sensíveis em um DataFrame.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados a serem anonimizados.
    
    Retorna:
    pd.DataFrame: DataFrame com dados anonimizados.
    """
    # Exemplo de anonimização: substituindo CPF e CNPJ por IDs sintéticos
    df['funcionario_cpf'] = df['funcionario_cpf'].apply(lambda x: hash(x))
    df['empresa_cnpj'] = df['empresa_cnpj'].apply(lambda x: hash(x))
    
    # Remover ou anonimizar outros campos sensíveis conforme necessário
    return df

def anonimiza_dados_bigquery(project_id: str, dataset_id: str, table_id: str):
    """
    Anonimiza dados de uma tabela no BigQuery.
    
    Parâmetros:
    project_id (str): ID do projeto no Google Cloud.
    dataset_id (str): ID do dataset no BigQuery.
    table_id (str): ID da tabela a ser anonimizada.
    """
    client = bigquery.Client(project=project_id)
    
    # Carregar dados da tabela
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    df = client.query(query).to_dataframe()
    
    # Anonimizar dados
    df_anonimizado = anonimiza_dataframe(df)
    
    # Salvar dados anonimizados de volta no BigQuery
    table_ref = client.dataset(dataset_id).table(f"{table_id}_anonimizado")
    job = client.load_table_from_dataframe(df_anonimizado, table_ref)
    job.result()  # Espera o job terminar

    print(f"Tabela anonimizada salva como {table_id}_anonimizado no dataset {dataset_id}.")