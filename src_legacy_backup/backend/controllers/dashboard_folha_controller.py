# src/controllers/dashboard_folha_controller.py
from datetime import date
from typing import Dict, Any, Optional
from decimal import Decimal
from google.cloud import bigquery # Para interagir com BigQuery
import pandas as pd

from src.schemas import DashboardSaudeFolhaResponse, KPIDashboardSaudeFolha, ResumoDivergenciaPorSeveridade, ResumoDivergenciaPorTipo
from src.config_manager import get_background_task_config
from src.bq_loader import get_bigquery_client
from src.utils.bq_executor import BQExecutor # Nova importação

async def gerar_dados_dashboard_saude(id_folha_processada: str, id_cliente: str) -> Optional[DashboardSaudeFolhaResponse]:
    """
    Busca e consolida os dados para o Dashboard de Saúde da Folha.
    """
    try:
        client_config = get_background_task_config(id_cliente)
        bq_client = get_bigquery_client(client_config)
        
        auditoria_folha_dataset_id = client_config.get("auditoria_folha_dataset_id") # Exemplo de chave
        if not auditoria_folha_dataset_id:
            raise ValueError(f"\'auditoria_folha_dataset_id\' não encontrado na configuração do cliente {id_cliente}")

        bq_executor = BQExecutor(
            bq_client=bq_client,
            project_id=client_config["gcp_project_id"],
            dataset_id=auditoria_folha_dataset_id 
        )

    except Exception as e:
        print(f"Erro ao inicializar dependências para dashboard: {e}") # Substituir por logging real
        return None

    # 1. Buscar dados do cabeçalho da folha
    query_header = """
        SELECT total_bruto_folha_extrato, total_liquido_folha_extrato, total_funcionarios_identificados, status_geral_folha
        FROM auditoria_folha_dataset.FolhasProcessadasHeader
        WHERE id_folha_processada = @id_folha AND id_cliente = @id_cliente_param
    """
    params_header = [
        bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha_processada),
        bigquery.ScalarQueryParameter("id_cliente_param", "STRING", id_cliente), # Renomeado para evitar conflito com client_id da config
    ]
    df_header = bq_executor.execute_query_to_dataframe(query_header, params_header)


    if df_header.empty:
        return None # Folha não encontrada ou não pertence ao cliente

    header_data = df_header.iloc[0]

    # 2. Resumo das divergências por severidade
    query_div_severidade = """
        SELECT severidade_divergencia, COUNT(*) as quantidade
        FROM auditoria_folha_dataset.DivergenciasAnaliseFolha
        WHERE id_folha_processada_fk = @id_folha 
        GROUP BY severidade_divergencia
    """
    params_div = [bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha_processada)]
    df_div_severidade = bq_executor.execute_query_to_dataframe(query_div_severidade, params_div)
    
    divergencias_por_severidade = [
        ResumoDivergenciaPorSeveridade(severidade=row["severidade_divergencia"], quantidade=row["quantidade"])
        for index, row in df_div_severidade.iterrows()
    ]
    total_divergencias = sum(item.quantidade for item in divergencias_por_severidade)

    # 3. Resumo das divergências por tipo e impacto financeiro
    query_div_tipo = """
        SELECT tipo_divergencia, COUNT(*) as quantidade, SUM(diferenca_absoluta) as soma_diferenca_absoluta
        FROM auditoria_folha_dataset.DivergenciasAnaliseFolha
        WHERE id_folha_processada_fk = @id_folha
        GROUP BY tipo_divergencia
        ORDER BY quantidade DESC
    """
    df_div_tipo = bq_executor.execute_query_to_dataframe(query_div_tipo, params_div)
    divergencias_por_tipo = [
        ResumoDivergenciaPorTipo(
            tipo_divergencia=row["tipo_divergencia"], 
            quantidade=row["quantidade"],
            soma_diferenca_absoluta=Decimal(str(row["soma_diferenca_absoluta"] or "0.00"))
        )
        for index, row in df_div_tipo.iterrows()
    ]

    # 4. Montar KPIs
    kpis = KPIDashboardSaudeFolha(
        total_bruto_folha_extrato=Decimal(str(header_data.get("total_bruto_folha_extrato", "0.00"))),
        total_liquido_folha_extrato=Decimal(str(header_data.get("total_liquido_folha_extrato", "0.00"))),
        numero_funcionarios_identificados=int(header_data.get("total_funcionarios_identificados", 0)),
        status_geral_folha=str(header_data.get("status_geral_folha", "N/A")),
        total_divergencias_identificadas=total_divergencias
    )

    # (Opcional) Lógica para comparativo com mês anterior aqui

    return DashboardSaudeFolhaResponse(
        kpis=kpis,
        divergencias_por_severidade=divergencias_por_severidade,
        divergencias_por_tipo=divergencias_por_tipo
    )
