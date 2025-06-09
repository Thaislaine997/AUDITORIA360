# src/controllers/checklist_folha_controller.py
import uuid
from typing import List, Optional, Dict, Any
from datetime import date
from src.schemas.checklist_schemas import ChecklistItemCreateSchema, ChecklistItemResponseSchema

class ChecklistFolhaController:
    def __init__(self, client_id: str, id_folha_processada: str, current_user):
        from src.config_manager import ConfigManager
        from src.utils.bq_executor import BQExecutor
        from google.cloud import bigquery
        config_manager = ConfigManager()
        client_config = config_manager.get_config_for_client_id(client_id)
        project_id = client_config.get("gcp_project_id")
        dataset_id = client_config.get("bq_dataset_folhas")
        if not project_id or not dataset_id:
            raise ValueError("Configuração do cliente incompleta: gcp_project_id ou bq_dataset_folhas ausente.")
        bq_client = bigquery.Client(project=project_id)
        self.bq_executor = BQExecutor(bq_client=bq_client, project_id=project_id, dataset_id=dataset_id)
        self.client_id = client_id
        self.id_folha_processada = id_folha_processada
        self.dataset_id = dataset_id
        self.table_id = f"{self.dataset_id}.ChecklistFechamentoFolha"
        self.header_table_id = f"{self.dataset_id}.FolhasProcessadasHeader"
        self.divergencias_table_id = f"{self.dataset_id}.DivergenciasAnaliseFolha"
        self.linhas_folha_table_id = f"{self.dataset_id}.LinhasFolhaFuncionario"


    def _run_query_to_dict(self, query, query_params):
        df = self.bq_executor.execute_query_to_dataframe(query, query_params=query_params)
        return df.to_dict(orient="records")

    def _get_folha_processada_header_info(self) -> Optional[Dict[str, Any]]:
        from google.cloud import bigquery
        query = f"""
            SELECT periodo_referencia, status_geral_folha
            FROM `{self.header_table_id}`
            WHERE id_folha_processada = @id_folha_processada AND id_cliente = @id_cliente
        """
        query_params = [
            bigquery.ScalarQueryParameter("id_folha_processada", "STRING", self.id_folha_processada),
            bigquery.ScalarQueryParameter("id_cliente", "STRING", self.client_id)
        ]
        results = self._run_query_to_dict(query, query_params)
        if results:
            # Garante que todas as chaves são str
            return {str(k): v for k, v in results[0].items()}
        return None

    def _get_itens_checklist_bd(self) -> List[ChecklistItemResponseSchema]:
        from google.cloud import bigquery
        query = f"""
            SELECT *
            FROM `{self.table_id}`
            WHERE id_folha_processada_fk = @id_folha_processada_fk AND id_cliente = @id_cliente
            ORDER BY ordem_item ASC
        """
        query_params = [
            bigquery.ScalarQueryParameter("id_folha_processada_fk", "STRING", self.id_folha_processada),
            bigquery.ScalarQueryParameter("id_cliente", "STRING", self.client_id)
        ]
        results = self._run_query_to_dict(query, query_params)
        return [ChecklistItemResponseSchema(**{str(k): v for k, v in row.items()}) for row in results]

    def _get_divergencias_alta_severidade(self, periodo_referencia: date) -> int:
        from google.cloud import bigquery
        query = f"""
            SELECT COUNT(*) as count_alta_severidade
            FROM `{self.divergencias_table_id}`
            WHERE id_folha_processada_fk = @id_folha_processada
              AND id_cliente = @id_cliente
              AND periodo_referencia = @periodo_referencia
              AND severidade_divergencia = 'ALTA'
        """
        query_params = [
            bigquery.ScalarQueryParameter("id_folha_processada", "STRING", self.id_folha_processada),
            bigquery.ScalarQueryParameter("id_cliente", "STRING", self.client_id),
            bigquery.ScalarQueryParameter("periodo_referencia", "DATE", periodo_referencia)
        ]
        results = self._run_query_to_dict(query, query_params)
        return results[0]['count_alta_severidade'] if results and results[0] else 0

    def _get_rubricas_nao_mapeadas(self, periodo_referencia: date) -> int:
        from google.cloud import bigquery
        query = f"""
            SELECT COUNT(DISTINCT codigo_rubrica_original) as count_nao_mapeadas
            FROM `{self.linhas_folha_table_id}`
            WHERE id_folha_processada_fk = @id_folha_processada
              AND id_cliente = @id_cliente
              AND periodo_referencia = @periodo_referencia
              AND id_rubrica_sistema IS NULL
        """
        query_params = [
            bigquery.ScalarQueryParameter("id_folha_processada", "STRING", self.id_folha_processada),
            bigquery.ScalarQueryParameter("id_cliente", "STRING", self.client_id),
            bigquery.ScalarQueryParameter("periodo_referencia", "DATE", periodo_referencia)
        ]
        results = self._run_query_to_dict(query, query_params)
        return results[0]['count_nao_mapeadas'] if results and results[0] else 0

    def _criar_itens_dinamicos(self, periodo_referencia: date, ordem_inicio: int) -> List[ChecklistItemCreateSchema]:
        itens_dinamicos = []
        count_alta_severidade = self._get_divergencias_alta_severidade(periodo_referencia)
        if count_alta_severidade > 0:
            itens_dinamicos.append(ChecklistItemCreateSchema(
                id_folha_processada_fk=self.id_folha_processada,
                id_cliente=self.client_id,
                periodo_referencia=periodo_referencia,
                ordem_item=ordem_inicio,
                categoria_item="ANALISE_DIVERGENCIAS",
                descricao_item_checklist=f"Resolver/Justificar {count_alta_severidade} divergências de severidade ALTA",
                tipo_item="BLOQUEADOR",
                status_item_checklist="PENDENTE"
            ))
            ordem_inicio += 1
        count_rubricas_nao_mapeadas = self._get_rubricas_nao_mapeadas(periodo_referencia)
        if count_rubricas_nao_mapeadas > 0:
            itens_dinamicos.append(ChecklistItemCreateSchema(
                id_folha_processada_fk=self.id_folha_processada,
                id_cliente=self.client_id,
                periodo_referencia=periodo_referencia,
                ordem_item=ordem_inicio,
                categoria_item="ANALISE_DIVERGENCIAS",
                descricao_item_checklist=f"Mapear/Cadastrar {count_rubricas_nao_mapeadas} Rubricas Não Identificadas",
                tipo_item="BLOQUEADOR",
                status_item_checklist="PENDENTE"
            ))
        return itens_dinamicos

    def get_checklist_folha(self) -> List[ChecklistItemResponseSchema]:
        header_info = self._get_folha_processada_header_info()
        if not header_info:
            raise Exception("Folha processada não encontrada.")
        periodo_referencia = header_info["periodo_referencia"]
        itens_existentes = self._get_itens_checklist_bd()
        if itens_existentes:
            return itens_existentes
        ordem_atual = 1
        itens_dinamicos = self._criar_itens_dinamicos(periodo_referencia, ordem_atual)
        # Aqui você pode converter para ChecklistItemResponseSchema se necessário
        return [ChecklistItemResponseSchema(**item.dict()) for item in itens_dinamicos]

    async def update_item_checklist_bd(self, id_item_checklist: str, item_update_data, usuario_responsavel: str):
        # Placeholder: implemente a lógica real conforme necessário
        return None

    async def get_dica_ia_para_item(self, id_item_checklist: str, descricao_item_externa=None):
        # Placeholder: implemente a lógica real conforme necessário
        return {"dica": "Funcionalidade não implementada."}

    async def marcar_folha_como_fechada(self, usuario_fechamento: str):
        # Placeholder: implemente a lógica real conforme necessário
        return {"message": "Funcionalidade não implementada.", "novo_status_folha": "FECHADA"}

