# filepath: src/bq_loader.py
import json
import logging
import os
from datetime import datetime, timezone
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from typing import Optional

# Configuração de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

# --- Schema da Tabela BigQuery ---
TABLE_SCHEMA = [
    bigquery.SchemaField("id_extracao", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("id_item", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("nome_arquivo_origem", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("pagina", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("tipo_campo", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("texto_extraido", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("valor_limpo", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("valor_numerico", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("confianca", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("timestamp_carga", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),  # Isolamento multi-cliente obrigatório
]

# ATENÇÃO: Todas as queries e cargas DEVEM usar o filtro client_id para garantir isolamento de dados entre clientes (white-label/multi-tenant).

def get_bigquery_client(config_dict: dict):
    """Cria e retorna um cliente BigQuery usando a configuração fornecida."""
    if not config_dict:
        raise ValueError("O argumento 'config_dict' é obrigatório para get_bigquery_client.")
    key_path = config_dict.get("service_account_key_path_local_dev")
    project_id = config_dict.get("gcp_project_id")

    if not project_id:
        logging.error("gcp_project_id não encontrado na configuração para get_bigquery_client.")
        raise ValueError("gcp_project_id é necessário.")

    try:
        if key_path:
            logging.info(f"Criando cliente BigQuery usando chave local: {key_path}")
            credentials = service_account.Credentials.from_service_account_file(key_path)
            client = bigquery.Client(credentials=credentials, project=project_id)
        else:
            logging.info("Criando cliente BigQuery usando Application Default Credentials (ADC).")
            client = bigquery.Client(project=project_id)
        logging.info("Cliente BigQuery criado com sucesso.")
        return client
    except Exception as e:
        logging.error(f"Falha ao criar cliente BigQuery: {e}", exc_info=True)
        raise

def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str, location: str):
    """Cria o dataset no BigQuery se ele não existir."""
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        logging.info(f"Dataset '{dataset_id}' já existe.")
    except Exception:
        logging.info(f"Dataset '{dataset_id}' não encontrado. Criando...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        client.create_dataset(dataset, timeout=30)
        logging.info(f"Dataset '{dataset_id}' criado em '{location}'.")

def create_or_update_table(client: bigquery.Client, dataset_id: str, table_id: str, schema: list):
    """Cria ou atualiza a tabela no BigQuery com o schema especificado."""
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        client.get_table(table_ref)
        logging.info(f"Tabela '{dataset_id}.{table_id}' já existe.")
    except Exception:
        logging.info(f"Tabela '{dataset_id}.{table_id}' não encontrada. Criando...")
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        logging.info(f"Tabela '{dataset_id}.{table_id}' criada.")

def load_data_to_bigquery(data: list[dict], config: dict):
    """
    Carrega uma lista de dicionários (registros) para a tabela BigQuery especificada na configuração.

    Args:
        data: Lista de dicionários, onde cada dicionário representa uma linha.
        config: Dicionário de configuração obrigatório.
    """
    if not data:
        logging.warning("Nenhum dado fornecido para carregar no BigQuery.")
        return

    if not config:
        logging.error("Configuração não fornecida para load_data_to_bigquery.")
        raise ValueError("O argumento 'config' é obrigatório.")

    client_id = config.get("client_id")
    if not client_id:
        raise ValueError("O campo 'client_id' é obrigatório na configuração para isolamento multi-cliente.")

    try:
        project_id = config["gcp_project_id"]
        dataset_id = config["bq_dataset_id"]
        table_id = config["bq_table_id"]
        location = config["gcp_location"]
    except KeyError as e:
        logging.error(f"Chave de configuração ausente para BigQuery em 'config': {e}")
        raise ValueError(f"Configuração do BigQuery (passada) incompleta: falta {e}")

    client = get_bigquery_client(config)
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    try:
        create_dataset_if_not_exists(client, dataset_id, location)
        create_or_update_table(client, dataset_id, table_id, TABLE_SCHEMA)

        timestamp_agora_iso = datetime.now(timezone.utc).isoformat()
        for row in data:
            row['timestamp_carga'] = timestamp_agora_iso
            row['client_id'] = client_id  # Garante isolamento multi-cliente

        job_config = bigquery.LoadJobConfig(
            schema=TABLE_SCHEMA,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        logging.info(f"Iniciando carregamento de {len(data)} registros para '{full_table_id}'...")
        load_job = client.load_table_from_json(
            data,
            full_table_id,
            job_config=job_config
        )
        load_job.result()

        if load_job.errors:
            logging.error(f"Erro ao carregar dados para '{full_table_id}': {load_job.errors}")
            raise RuntimeError(f"Erro no job de carregamento do BigQuery: {load_job.errors}")
        else:
            logging.info(f"Carregamento concluído com sucesso. {load_job.output_rows} linhas carregadas para '{full_table_id}'.")
    except Exception as e:
        logging.error(f"Erro durante o processo de carregamento para BigQuery '{full_table_id}': {e}", exc_info=True)
        raise

class ControleFolhaLoader:
    def __init__(self, config: dict):
        if not config:
            raise ValueError("A configuração é obrigatória para ControleFolhaLoader.")
        
        self.client_id = config.get("client_id")
        self.project_id = config.get("gcp_project_id")
        dataset_id_from_config = config.get("control_bq_dataset_id", config.get("bq_dataset_id"))
        if not isinstance(dataset_id_from_config, str):
            raise ValueError("control_bq_dataset_id ou bq_dataset_id (string) não encontrado ou inválido na configuração para ControleFolhaLoader.")
        self.dataset_id: str = dataset_id_from_config

        if not self.client_id:
            raise ValueError("client_id não encontrado na configuração para ControleFolhaLoader.")
        if not self.project_id:
            raise ValueError("gcp_project_id não encontrado na configuração para ControleFolhaLoader.")

        logger.info(f"Inicializando ControleFolhaLoader para client_id: {self.client_id}, projeto: {self.project_id}, dataset: {self.dataset_id}")
        try:
            client_config = config.copy() 
            self.client = get_bigquery_client(client_config)
            logger.info(f"Cliente BigQuery inicializado com sucesso para ControleFolhaLoader (client_id: {self.client_id}).")
        except Exception as e:
            logger.error(f"Falha ao inicializar o cliente BigQuery para ControleFolhaLoader (client_id: {self.client_id}): {e}", exc_info=True)
            raise ValueError(f"Não foi possível conectar ao BigQuery: {e}")

    def _ensure_client(self):
        if not self.client:
            logger.error(f"Cliente BigQuery não inicializado para ControleFolhaLoader (client_id: {self.client_id}).")
            raise RuntimeError("Cliente BigQuery não está disponível.")

    def listar_todas_as_empresas(self) -> pd.DataFrame:
        self._ensure_client()
        table_empresas_id = f"{self.project_id}.{self.dataset_id}.empresas" 
        query = f"SELECT codigo_empresa, cnpj, nome_empresa, contato, email, cidade, sindicato, particularidades, forma_envio, data_cadastro, id_contabilidade, id_sindicato, client_id FROM `{table_empresas_id}` WHERE client_id = @client_id"
        params = [bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id)]
        try:
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            df = self.client.query(query, job_config=job_config).to_dataframe()
            logger.info(f"Empresas listadas para o client_id {self.client_id} do dataset {self.dataset_id}: {len(df)} encontradas.")
            return df
        except Exception as e:
            logger.error(f"Erro ao listar empresas para client_id {self.client_id} do dataset {self.dataset_id}: {e}", exc_info=True)
            return pd.DataFrame()

    def get_empresa_by_id(self, empresa_id: int) -> Optional[dict]:
        self._ensure_client()
        table_empresas_id = f"{self.project_id}.{self.dataset_id}.empresas"
        query = f"SELECT codigo_empresa, cnpj, nome_empresa, contato, email, cidade, sindicato, particularidades, forma_envio, data_cadastro, id_contabilidade, id_sindicato, client_id FROM `{table_empresas_id}` WHERE codigo_empresa = @empresa_id AND client_id = @client_id"
        params = [
            bigquery.ScalarQueryParameter("empresa_id", "INTEGER", empresa_id),
            bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id)
        ]
        try:
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            query_job = self.client.query(query, job_config=job_config)
            results = list(query_job)
            if results:
                logger.info(f"Empresa com codigo_empresa {empresa_id} encontrada para client_id {self.client_id} no dataset {self.dataset_id}.")
                return dict(results[0])
            else:
                logger.info(f"Nenhuma empresa encontrada com codigo_empresa {empresa_id} para client_id {self.client_id} no dataset {self.dataset_id}.")
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar empresa por codigo_empresa {empresa_id} para client_id {self.client_id} no dataset {self.dataset_id}: {e}", exc_info=True)
            return None

    def inserir_folha(self, 
                      id_folha: str, 
                      codigo_empresa: int, 
                      cnpj_empresa: str, 
                      mes_ano: str, 
                      status: str, 
                      data_envio_cliente: Optional[datetime] = None, 
                      data_guia_fgts: Optional[datetime] = None,
                      data_darf_inss: Optional[datetime] = None, 
                      observacoes: Optional[str] = None):
        self._ensure_client()
        table_folhas_id = f"{self.project_id}.{self.dataset_id}.folhas"
        
        if not all([id_folha, isinstance(codigo_empresa, int), cnpj_empresa, mes_ano, status]):
            logger.error(f"Dados obrigatórios ausentes ou inválidos para inserir folha (client_id: {self.client_id}). id_folha: {id_folha}, codigo_empresa: {codigo_empresa}, cnpj_empresa: {cnpj_empresa}, mes_ano: {mes_ano}, status: {status}")
            raise ValueError("id_folha, codigo_empresa, cnpj_empresa, mes_ano e status são obrigatórios.")

        try:
            datetime.strptime(mes_ano, '%Y-%m-%d')
        except ValueError:
            logger.error(f"Formato de mes_ano inválido: {mes_ano}. Use YYYY-MM-DD. (client_id: {self.client_id})")
            raise ValueError("Formato de mes_ano inválido. Use YYYY-MM-DD.")

        row_to_insert = {
            "id_folha": id_folha,
            "codigo_empresa": codigo_empresa,
            "cnpj_empresa": cnpj_empresa,
            "mes_ano": mes_ano,
            "status": status,
            "data_envio_cliente": data_envio_cliente.isoformat() if data_envio_cliente else None,
            "data_guia_fgts": data_guia_fgts.isoformat() if data_guia_fgts else None,
            "data_darf_inss": data_darf_inss.isoformat() if data_darf_inss else None,
            "observacoes": observacoes,
            "client_id": self.client_id
        }

        try:
            errors = self.client.insert_rows_json(table_folhas_id, [row_to_insert])
            if not errors:
                logger.info(f"Folha {id_folha} inserida com sucesso para client_id {self.client_id} na tabela {table_folhas_id}.")
                return True
            else:
                logger.error(f"Erro ao inserir folha {id_folha} para client_id {self.client_id} na tabela {table_folhas_id}: {errors}")
                raise RuntimeError(f"Falha ao inserir dados no BigQuery: {errors}")
        except Exception as e:
            logger.error(f"Exceção ao inserir folha {id_folha} para client_id {self.client_id} na tabela {table_folhas_id}: {e}", exc_info=True)
            raise

    def get_folha_by_id(self, id_folha: str) -> Optional[dict]:
        self._ensure_client()
        table_folhas_id = f"{self.project_id}.{self.dataset_id}.folhas"
        query = f"SELECT id_folha, codigo_empresa, cnpj_empresa, mes_ano, status, data_envio_cliente, data_guia_fgts, data_darf_inss, observacoes, client_id FROM `{table_folhas_id}` WHERE id_folha = @id_folha AND client_id = @client_id"
        params = [
            bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
            bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id)
        ]
        try:
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            query_job = self.client.query(query, job_config=job_config)
            results = list(query_job)
            if results:
                logger.info(f"Folha com id_folha {id_folha} encontrada para client_id {self.client_id} no dataset {self.dataset_id}.")
                return dict(results[0])
            else:
                logger.info(f"Nenhuma folha encontrada com id_folha {id_folha} para client_id {self.client_id} no dataset {self.dataset_id}.")
                return None
        except Exception as e:
            logger.error(f"Erro ao buscar folha por id_folha {id_folha} para client_id {self.client_id} no dataset {self.dataset_id}: {e}", exc_info=True)
            return None

    def update_folha_status(self, id_folha: str, novo_status: str) -> bool:
        self._ensure_client()
        table_folhas_id = f"{self.project_id}.{self.dataset_id}.folhas"
        query = f"""
            UPDATE `{table_folhas_id}`
            SET status = @novo_status
            WHERE id_folha = @id_folha AND client_id = @client_id
        """
        params = [
            bigquery.ScalarQueryParameter("novo_status", "STRING", novo_status),
            bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
            bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id)
        ]
        try:
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()
            
            if query_job.num_dml_affected_rows is not None and query_job.num_dml_affected_rows > 0:
                logger.info(f"Status da folha {id_folha} atualizado para '{novo_status}' para client_id {self.client_id} no dataset {self.dataset_id}. Linhas afetadas: {query_job.num_dml_affected_rows}.")
                return True
            elif query_job.num_dml_affected_rows == 0:
                logger.warning(f"Nenhuma folha encontrada com id_folha {id_folha} para client_id {self.client_id} no dataset {self.dataset_id} para atualizar status, ou o status já era '{novo_status}'.")
                return False
            else:
                logger.warning(f"A atualização do status da folha {id_folha} para client_id {self.client_id} no dataset {self.dataset_id} não retornou o número de linhas afetadas como esperado.")
                return False
        except Exception as e:
            logger.error(f"Erro ao atualizar status da folha {id_folha} para client_id {self.client_id} no dataset {self.dataset_id}: {e}", exc_info=True)
            return False
            
    def consolidar_dados_planilha_para_folhas(self, nome_arquivo_origem_especifico: str) -> bool:
        self._ensure_client()
        table_raw_data_id = f"`{self.project_id}.{self.dataset_id}.controle_folha_planilha_raw_data`"
        table_folhas_id = f"`{self.project_id}.{self.dataset_id}.folhas`"
        table_empresas_id = f"`{self.project_id}.{self.dataset_id}.empresas`"
        table_status_map_id = f"`{self.project_id}.{self.dataset_id}.status_map`"

        query = f"""
        MERGE {table_folhas_id} T
        USING (
            SELECT
                raw.cnpj_empresa,
                PARSE_DATE('%Y-%m-%d', raw.mes_ano_referencia) AS mes_ano_date, -- Assumindo string 'YYYY-MM-DD'
                raw.nome_arquivo_origem,
                raw.client_id AS source_client_id,
                emp.codigo_empresa,
                CASE
                    WHEN emp.codigo_empresa IS NULL THEN 'AGUARDANDO_CADASTRO_EMPRESA'
                    ELSE COALESCE(sm.status_final, raw.status_valor_cliente, 'PENDENTE_PROCESSAMENTO')
                END AS status_calculado,
                CASE
                    WHEN emp.codigo_empresa IS NULL THEN 'CNPJ não encontrado no cadastro de empresas.'
                    ELSE NULL -- Limpa/nenhuma observação se empresa encontrada
                END AS observacao_calculada
            FROM {table_raw_data_id} raw
            LEFT JOIN {table_empresas_id} emp ON raw.cnpj_empresa = emp.cnpj AND raw.client_id = emp.client_id
            LEFT JOIN {table_status_map_id} sm ON raw.status_aba_origem = sm.status_aba AND raw.status_valor_cliente = sm.status_valor AND raw.client_id = sm.client_id
            WHERE raw.nome_arquivo_origem = @nome_arquivo AND raw.client_id = @client_id_param
        ) S
        ON T.cnpj_empresa = S.cnpj_empresa AND T.mes_ano = S.mes_ano_date AND T.client_id = S.source_client_id
        WHEN MATCHED THEN
            UPDATE SET
                T.status = S.status_calculado,
                T.observacoes = CASE
                                 WHEN T.status = 'AGUARDANDO_CADASTRO_EMPRESA' AND S.codigo_empresa IS NOT NULL THEN NULL -- Limpa observação se empresa foi cadastrada
                                 ELSE S.observacao_calculada -- Mantém ou define nova observação (pode ser NULL)
                               END,
                T.codigo_empresa = S.codigo_empresa, -- Atualiza com o codigo_empresa da origem (pode ser NULL se ainda não encontrado, ou o código se encontrado)
                T.data_processamento_gcs = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN
            INSERT (
                id_folha, codigo_empresa, cnpj_empresa, mes_ano, status,
                client_id, nome_arquivo_origem, observacoes,
                data_envio_cliente, data_guia_fgts, data_darf_inss, data_processamento_gcs
            )
            VALUES (
                GENERATE_UUID(),
                S.codigo_empresa,       -- Será NULL se a empresa não for encontrada
                S.cnpj_empresa,
                S.mes_ano_date,         -- Usando o campo convertido para DATE
                S.status_calculado,
                S.source_client_id,
                S.nome_arquivo_origem,
                S.observacao_calculada,
                CURRENT_TIMESTAMP(),    -- data_envio_cliente (default)
                NULL,                   -- data_guia_fgts (não disponível na raw)
                NULL,                   -- data_darf_inss (não disponível na raw)
                CURRENT_TIMESTAMP()     -- data_processamento_gcs
            );
        """
        params = [
            bigquery.ScalarQueryParameter("nome_arquivo", "STRING", nome_arquivo_origem_especifico),
            bigquery.ScalarQueryParameter("client_id_param", "STRING", self.client_id)
        ]
        try:
            logger.info(f"Iniciando consolidação para arquivo: {nome_arquivo_origem_especifico}, client_id: {self.client_id}")
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            query_job = self.client.query(query, job_config=job_config)
            query_job.result() # Aguarda a conclusão do job
            
            affected_rows = query_job.num_dml_affected_rows
            logger.info(f"Consolidação para {nome_arquivo_origem_especifico} (client_id: {self.client_id}) concluída. Linhas afetadas: {affected_rows if affected_rows is not None else 'N/A'}.")
            return True
        except Exception as e:
            logger.error(f"Erro ao consolidar dados da planilha {nome_arquivo_origem_especifico} (client_id: {self.client_id}): {e}", exc_info=True)
            return False

    def buscar_pendencias_dashboard(self) -> dict:
        self._ensure_client()
        table_dashboard_id = f"{self.project_id}.{self.dataset_id}.dashboard"
        query = f"SELECT tarefa, quantidade_concluida, percentual_concluido, quantidade_pendente, percentual_pendente, data_atualizacao, client_id FROM `{table_dashboard_id}` WHERE client_id = @client_id ORDER BY data_atualizacao DESC"
        params = [bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id)]
        try:
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            df = self.client.query(query, job_config=job_config).to_dataframe()
            if not df.empty:
                if 'data_atualizacao' in df.columns and not df['data_atualizacao'].empty:
                    df['data_atualizacao'] = df['data_atualizacao'].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
                logger.info(f"Busca de pendências do dashboard para client_id {self.client_id} bem-sucedida. {len(df)} registros encontrados.")
                return {"status": "success", "data": df.to_dict(orient='records')}
            else:
                logger.info(f"Nenhum dado de dashboard encontrado para client_id {self.client_id}.")
                return {"status": "success", "data": [], "message": "Nenhum dado de dashboard encontrado."}
        except Exception as e:
            logger.error(f"Erro ao buscar pendências do dashboard para client_id {self.client_id}: {e}", exc_info=True)
            return {"status": "error", "message": str(e), "data": []}

if __name__ == "__main__":
    logging.info("Executando bq_loader.py como script principal (modo de teste).")
    print("\n[INFO] Para testar este módulo, execute: python -m src.bq_loader (a partir da raiz do projeto)")
    try:
        from src.config_manager import config_manager, CLIENT_CONFIGS_DIR
        
        CLIENT_ID_TESTE_STANDALONE = "test_client_standalone" 
        config_teste = None
        try:
            standalone_client_config_path = os.path.join(CLIENT_CONFIGS_DIR, f"{CLIENT_ID_TESTE_STANDALONE}.json")
            
            if os.path.exists(standalone_client_config_path):
                logger.info(f"Tentando carregar configuração para o cliente de teste standalone: {CLIENT_ID_TESTE_STANDALONE} a partir de {standalone_client_config_path}")
                with open(standalone_client_config_path, 'r') as f_config_client:
                    client_specific_config = json.load(f_config_client)
                config_teste = config_manager.base_config.copy()
                config_teste.update(client_specific_config)
                config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE
            else:
                logger.warning(f"Arquivo de configuração para cliente de teste standalone '{standalone_client_config_path}' não encontrado.")
                logger.info("Usando configuração base para o teste standalone do bq_loader e adicionando client_id.")
                config_teste = config_manager.base_config.copy()
                config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE

            default_values = {
                "gcp_project_id": "default-project-for-standalone",
                "bq_dataset_id": "default_dataset_standalone",
                "bq_table_id": "default_table_standalone",
                "gcp_location": "us-central1",
                "service_account_key_path_local_dev": config_manager.base_config.get("service_account_key_path_local_dev"),
                "control_bq_dataset_id": config_manager.base_config.get("control_bq_dataset_id", "default_control_dataset")
            }
            for key, value in default_values.items():
                if key not in config_teste or not config_teste[key]:
                    config_teste[key] = value
            
            if "client_id" not in config_teste:
                config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE

        except Exception as e_config:
            logger.error(f"Erro ao tentar carregar configuração para teste standalone: {e_config}. Usando base_config com defaults.")
            config_teste = config_manager.base_config.copy()
            config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE
            default_values_fallback = {
                "gcp_project_id": "default-project-for-standalone",
                "bq_dataset_id": "default_dataset_standalone",
                "bq_table_id": "default_table_standalone",
                "gcp_location": "us-central1",
                "service_account_key_path_local_dev": config_manager.base_config.get("service_account_key_path_local_dev"),
                "control_bq_dataset_id": config_manager.base_config.get("control_bq_dataset_id", "default_control_dataset")
            }
            for key, value in default_values_fallback.items():
                if key not in config_teste or not config_teste[key]:
                    config_teste[key] = value

        if not config_teste:
            logger.error("Configuração de teste não pôde ser carregada. Teste de bq_loader não executado.")
            print("Configuração de teste não carregada, teste de carregamento no BigQuery não executado.")
        else:
            logger.info(f"Configuração para teste standalone do bq_loader: {config_teste}")
            sample_data = [
                {'id_extracao': 'docai_test_123', 'id_item': 'item_1', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'SALARIO', 'texto_extraido': '1.000,00', 'valor_limpo': '1.000,00', 'valor_numerico': 1000.0, 'confianca': 0.99},
                {'id_extracao': 'docai_test_123', 'id_item': 'item_2', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'INSS', 'texto_extraido': '100,00 D', 'valor_limpo': '100,00', 'valor_numerico': -100.0, 'confianca': 0.98},
                {'id_extracao': 'docai_test_123', 'id_item': 'item_3', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'NOME_FUNC', 'texto_extraido': 'Fulano Teste', 'valor_limpo': 'Fulano Teste', 'valor_numerico': None, 'confianca': 0.95},
            ]
            
            required_keys_for_load = ["gcp_project_id", "bq_dataset_id", "bq_table_id", "gcp_location", "client_id"]
            missing_keys = [key for key in required_keys_for_load if key not in config_teste or not config_teste[key]]
            if missing_keys:
                logger.error(f"Configuração de teste incompleta para load_data_to_bigquery. Chaves ausentes ou vazias: {missing_keys}. Config: {config_teste}")
                print(f"Configuração de teste incompleta. Chaves ausentes ou vazias: {missing_keys}")
            else:
                import json
                load_data_to_bigquery(sample_data, config_teste)
                print("Teste de carregamento no BigQuery concluído (verifique o BQ e os logs).")

    except ImportError as ie:
        print(f"Erro de importação ao testar bq_loader.py: {ie}. Certifique-se de que o PYTHONPATH está configurado.")
    except ValueError as ve:
        print(f"Erro de valor (possivelmente configuração) ao testar bq_loader.py: {ve}")
    except Exception as e:
        print(f"Teste de carregamento no BigQuery falhou: {e}")
        logger.exception("Falha no teste standalone do bq_loader.")
