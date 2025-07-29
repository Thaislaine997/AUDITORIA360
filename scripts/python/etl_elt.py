"""
Script ETL/ELT para geração do Dataset de Treinamento de Riscos da Folha
AUDITORIA360 – Módulo 3

Etapas:
- Conexão ao BigQuery
- Extração dos dados principais (Tabela_Folha_Pagamento e auxiliares)
- Transformação, limpeza e engenharia de features
- Anonimização de dados sensíveis
- Carga na tabela DatasetTreinamentoRiscosFolha

Preencha as funções conforme as regras de negócio e features desejadas.
"""

import hashlib
import logging
import os

from google.cloud import bigquery
from google.oauth2 import service_account

# Configurações (ajuste conforme seu ambiente)
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "auditoria-folha")
DATASET_ID = os.getenv("BQ_DATASET_ID", "auditoria_folha_dataset")
TABELA_FOLHA = f"{PROJECT_ID}.{DATASET_ID}.Tabela_Folha_Pagamento"
TABELA_DESTINO = f"{PROJECT_ID}.{DATASET_ID}.DatasetTreinamentoRiscosFolha"
SERVICE_ACCOUNT_KEY_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # Opcional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_bigquery_client():
    if SERVICE_ACCOUNT_KEY_PATH:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_PATH
        )
        return bigquery.Client(credentials=credentials, project=PROJECT_ID)
    return bigquery.Client(project=PROJECT_ID)


def extrair_dados_folha(client):
    """Extrai dados da tabela principal de folha de pagamento."""
    query = f"""
        SELECT * FROM `{TABELA_FOLHA}`
    """
    df = client.query(query).to_dataframe()
    logging.info(f"Extraídos {len(df)} registros da folha.")
    return df


def transformar_features(df):
    """Realiza limpeza, transformação e engenharia de features."""
    # Exemplo: criar feature de proporção descontos/proventos
    df["proporcao_descontos"] = df["total_descontos"] / df["total_proventos"].replace(
        0, 1
    )
    # Exemplo: flag de inconsistência (ajuste conforme regras reais)
    df["flag_inconsistencia"] = df["total_descontos"] > (0.5 * df["total_proventos"])
    # ...adicione outras features relevantes...
    return df


def anonimizar_dados(df):
    """Anonimiza dados sensíveis (ex: CPF, nome)."""
    if "cpf_funcionario" in df.columns:
        df["cpf_funcionario_hash"] = df["cpf_funcionario"].apply(
            lambda x: hashlib.sha256(str(x).encode()).hexdigest()
        )
        df = df.drop(columns=["cpf_funcionario"])
    if "nome_funcionario" in df.columns:
        df = df.drop(columns=["nome_funcionario"])
    return df


def carregar_dataset_treinamento(client, df):
    """Carrega o DataFrame final na tabela de destino do BigQuery."""
    job = client.load_table_from_dataframe(df, TABELA_DESTINO)
    job.result()
    logging.info(
        f"Carregado dataset de treinamento com {len(df)} registros para {TABELA_DESTINO}."
    )


def main():
    client = get_bigquery_client()
    df_folha = extrair_dados_folha(client)
    df_features = transformar_features(df_folha)
    df_final = anonimizar_dados(df_features)
    carregar_dataset_treinamento(client, df_final)
    logging.info("ETL/ELT concluído com sucesso.")


if __name__ == "__main__":
    main()
