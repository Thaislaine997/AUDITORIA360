from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from src.schemas.folha_processada_schemas import FolhaProcessadaSelecaoSchema
from google.cloud import bigquery
from src.utils.auth_utils import get_current_active_user, User
from src.utils.bq_executor import BQExecutor
from src.utils.config_manager import config_manager # Importar a instância global
from datetime import datetime

router = APIRouter(
    prefix="/api/v1/clientes/{id_cliente}/folhas-processadas",
    tags=["Folhas Processadas"]
)

@router.get("/disponiveis-para-checklist", response_model=List[FolhaProcessadaSelecaoSchema])
async def listar_folhas_disponiveis_para_checklist(
    id_cliente: str = Path(...),
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_admin and current_user.client_id != id_cliente:
        raise HTTPException(status_code=403, detail="Acesso não autorizado ao cliente.")

    # Corrigido: usa get_client_config para obter config sem Request e a instância global
    client_config = config_manager.get_client_config(id_cliente) # Usar o método correto e a instância global

    # Garante que os campos obrigatórios existem
    project_id = client_config.get("gcp_project_id")
    dataset_id = client_config.get("bq_dataset_folhas")
    if not project_id or not dataset_id:
        raise HTTPException(status_code=500, detail="Configuração do cliente incompleta: gcp_project_id ou bq_dataset_folhas ausente.")

    bq_client = bigquery.Client(project=project_id)
    bq_executor = BQExecutor(
        bq_client=bq_client,
        project_id=project_id,
        dataset_id=dataset_id
    )
    table_id = f"{dataset_id}.FolhasProcessadasHeader"

    query = f"""
        SELECT id_folha_processada, periodo_referencia, status_geral_folha
        FROM `{table_id}`
        WHERE id_cliente = @id_cliente
          AND status_geral_folha IN ('PROCESSADA_COM_SUCESSO', 'FECHADA_PELO_CLIENTE')
        ORDER BY periodo_referencia DESC
        LIMIT 100
    """
    query_params = [
        bigquery.ScalarQueryParameter("id_cliente", "STRING", id_cliente)
    ]
    df = bq_executor.execute_query_to_dataframe(query, query_params=query_params)
    folhas = df.to_dict(orient="records")

    def make_display(row):
        periodo = row['periodo_referencia']
        status = row.get('status_geral_folha', '') or ''
        mes_ano = periodo.strftime('%m/%Y') if hasattr(periodo, 'strftime') else str(periodo)
        return f"Folha Mensal - {mes_ano} ({status.replace('_', ' ').title()})"

    return [
        FolhaProcessadaSelecaoSchema(
            id_folha_processada=row['id_folha_processada'],
            descricao_display=make_display(row),
            periodo_referencia=row['periodo_referencia'],
            status_geral_folha=row.get('status_geral_folha') or ''
        )
        for row in folhas
    ]
