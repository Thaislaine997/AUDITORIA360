# filepath: src/ingestion/load_payroll_csv.py
import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import logging
import uuid

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configurações ---
# TODO: Considerar mover para um arquivo de configuração ou variáveis de ambiente
PROJECT_ID = "auditoria-folha"
DATASET_ID = "dataset_auditoria"
TABLE_ID = "Tabela_Folha_Pagamento"
# TODO: Obter o caminho da chave de forma segura (ex: Secret Manager ou variável de ambiente)
# Exemplo: SERVICE_ACCOUNT_KEY_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SERVICE_ACCOUNT_KEY_PATH = None # Defina o caminho para sua chave JSON se não estiver usando ADC padrão

# --- Funções Auxiliares ---
def get_bigquery_client(project_id, key_path=None):
    """Cria e retorna um cliente BigQuery."""
    if key_path:
        credentials = service_account.Credentials.from_service_account_file(key_path)
        client = bigquery.Client(credentials=credentials, project=project_id)
        logging.info(f"Cliente BigQuery criado usando chave de serviço: {key_path}")
    else:
        # Tenta usar Application Default Credentials (ADC)
        client = bigquery.Client(project=project_id)
        logging.info("Cliente BigQuery criado usando Application Default Credentials (ADC).")
    return client

def transform_data(df, id_folha):
    """Aplica transformações necessárias aos dados do DataFrame."""
    # Adiciona o ID único da folha
    df['id_folha'] = id_folha

    # Converte colunas de data (ajuste o formato se necessário)
    if 'competencia' in df.columns:
        df['competencia'] = pd.to_datetime(df['competencia'], errors='coerce').dt.date

    # Converte colunas numéricas (adicione outras colunas conforme necessário)
    numeric_cols = [
        'salario_base', 'horas_trabalhadas', 'horas_extras_50', 'horas_extras_100',
        'adicional_noturno', 'adicional_insalubridade', 'adicional_periculosidade',
        'valor_vale_transporte', 'desconto_vale_transporte', 'valor_vale_refeicao',
        'desconto_vale_refeicao', 'desconto_inss', 'desconto_irrf',
        'outros_descontos', 'total_proventos', 'total_descontos', 'valor_liquido'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce') # 'coerce' transforma erros em NaT/NaN

    # Garante que todas as colunas da tabela existam no DataFrame (preenche com None se faltar)
    # Isso evita erros se o CSV não tiver todas as colunas esperadas pela tabela BQ
    # Obtenha o schema da tabela BQ para fazer isso dinamicamente (mais avançado)
    # Por agora, vamos assumir que o CSV tem as colunas necessárias ou elas serão NULL
    # Exemplo simples:
    # expected_cols = ['id_folha', 'id_funcionario', 'nome_funcionario', ...] # Lista completa de colunas BQ
    # for col in expected_cols:
    #     if col not in df.columns:
    #         df[col] = None

    # Renomeia colunas se necessário para corresponder ao schema do BigQuery
    # Exemplo: df = df.rename(columns={'id_empregado': 'id_funcionario'})

    # Remove colunas extras que não existem na tabela do BigQuery (opcional)
    # df = df[expected_cols]

    logging.info("Transformação de dados concluída.")
    return df

def load_csv_to_bigquery(csv_path, project_id, dataset_id, table_id, key_path=None):
    """Lê um CSV, transforma e carrega os dados para o BigQuery."""
    try:
        logging.info(f"Iniciando carregamento do CSV: {csv_path}")
        df = pd.read_csv(csv_path)
        logging.info(f"CSV lido com sucesso. {len(df)} linhas encontradas.")

        if df.empty:
            logging.warning("Arquivo CSV está vazio. Nenhum dado para carregar.")
            return

        # Gera um ID único para este lote/folha
        id_folha_processada = f"folha_{uuid.uuid4()}"
        logging.info(f"ID único gerado para esta folha: {id_folha_processada}")

        df_transformed = transform_data(df.copy(), id_folha_processada)

        client = get_bigquery_client(project_id, key_path)
        table_ref = client.dataset(dataset_id).table(table_id)

        # Configuração do Job de Carga
        # WRITE_APPEND: Adiciona os novos dados à tabela
        # WRITE_TRUNCATE: Apaga a tabela e insere os novos dados
        # WRITE_EMPTY: Só insere se a tabela estiver vazia
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV, # Embora estejamos carregando de DataFrame, BQ otimiza
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            autodetect=False, # Usamos o schema da tabela existente
            # Se precisar especificar o schema explicitamente:
            # schema=[
            #     bigquery.SchemaField("id_folha", "STRING"),
            #     bigquery.SchemaField("id_funcionario", "STRING"),
            #     ... (resto do schema)
            # ]
        )

        # Carrega o DataFrame para o BigQuery
        job = client.load_table_from_dataframe(
            df_transformed, table_ref, job_config=job_config
        )
        job.result()  # Espera o job completar

        logging.info(f"Dados carregados com sucesso para a tabela {project_id}.{dataset_id}.{table_id}. Job ID: {job.job_id}")
        logging.info(f"{job.output_rows} linhas carregadas.")

    except FileNotFoundError:
        logging.error(f"Erro: Arquivo CSV não encontrado em {csv_path}")
    except Exception as e:
        logging.error(f"Erro durante o carregamento para o BigQuery: {e}", exc_info=True)

# --- Execução Principal ---
if __name__ == "__main__":
    # TODO: Obter o caminho do CSV de um argumento de linha de comando ou configuração
    # Exemplo:
    # import argparse
    # parser = argparse.ArgumentParser(description='Carrega dados de folha de pagamento CSV para o BigQuery.')
    # parser.add_argument('csv_file', help='Caminho para o arquivo CSV da folha de pagamento.')
    # args = parser.parse_args()
    # csv_file_path = args.csv_file

    # Para teste, use um caminho fixo (crie este arquivo ou ajuste o caminho)
    sample_csv_path = "data/sample_folha.csv" # Crie este diretório e arquivo

    # Cria o diretório 'data' se não existir
    if not os.path.exists("data"):
         os.makedirs("data")
         logging.info("Diretório 'data' criado.")
    # Cria um arquivo CSV de exemplo se não existir
    if not os.path.exists(sample_csv_path):
         sample_data = """id_funcionario,nome_funcionario,cpf_funcionario,cargo,competencia,salario_base,horas_trabalhadas,horas_extras_50,horas_extras_100,adicional_noturno,adicional_insalubridade,adicional_periculosidade,valor_vale_transporte,desconto_vale_transporte,valor_vale_refeicao,desconto_vale_refeicao,desconto_inss,desconto_irrf,outros_descontos,total_proventos,total_descontos,valor_liquido