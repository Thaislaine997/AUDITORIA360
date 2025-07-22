# src/controllers/relatorios_folha_controller.py
import pandas as pd
import io
from typing import Tuple, Optional
from google.cloud import bigquery
from fastapi import HTTPException

from src.config_manager import get_background_task_config
from src.bq_loader import get_bigquery_client
from src.utils.bq_executor import BQExecutor # Nova importação

async def gerar_e_formatar_relatorio(
    id_folha_processada: str,
    id_cliente: str,
    nome_relatorio: str,
    formato: str
) -> Tuple[bytes, str]:
    """
    Busca dados, formata em DataFrame e converte para CSV ou XLSX bytes.
    """
    df = pd.DataFrame() 
    filename = f"relatorio_vazio.{formato}"

    try:
        client_config = get_background_task_config(id_cliente)
        bq_client = get_bigquery_client(client_config)
        
        auditoria_folha_dataset_id = client_config.get("auditoria_folha_dataset_id")
        if not auditoria_folha_dataset_id:
            raise ValueError(f"\'auditoria_folha_dataset_id\' não encontrado na configuração do cliente {id_cliente} para relatórios")

        bq_executor = BQExecutor(
            bq_client=bq_client,
            project_id=client_config["gcp_project_id"],
            dataset_id=auditoria_folha_dataset_id
        )
    except Exception as e:
        # Logar o erro de configuração/inicialização
        print(f"Erro ao inicializar dependências para relatórios: {e}") # Substituir por logging real
        raise HTTPException(status_code=500, detail=f"Erro interno ao configurar acesso aos dados: {e}")

    query = ""
    params: Optional[list] = None

    if nome_relatorio == "divergencias_completo":
        query = """
            SELECT 
                da.id_divergencia, da.funcionario_cpf, 
                COALESCE(lff.funcionario_nome_extrato, tff.funcionario_nome_extrato, 'N/A') as nome_funcionario,
                da.tipo_divergencia, da.campo_auditado, 
                da.valor_calculado_sistema, da.valor_extrato_cliente, 
                da.diferenca_absoluta, da.diferenca_percentual, 
                da.status_divergencia, da.severidade_divergencia, da.explicacao_ia_gerada,
                da.timestamp_identificacao
            FROM auditoria_folha_dataset.DivergenciasAnaliseFolha da
            LEFT JOIN auditoria_folha_dataset.LinhasFolhaFuncionario lff 
                ON da.funcionario_cpf = lff.funcionario_cpf AND da.id_folha_processada_fk = lff.id_folha_processada_fk
            LEFT JOIN auditoria_folha_dataset.TotaisFolhaFuncionario tff
                ON da.funcionario_cpf = tff.funcionario_cpf AND da.id_folha_processada_fk = tff.id_folha_processada_fk
            WHERE da.id_folha_processada_fk = @id_folha
            -- AND da.id_cliente = @id_cliente_param -- Adicionar se a tabela DivergenciasAnaliseFolha tiver id_cliente
            GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13 
            ORDER BY da.funcionario_cpf, da.tipo_divergencia
        """
        params = [
            bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha_processada),
            # bigquery.ScalarQueryParameter("id_cliente_param", "STRING", id_cliente), # Se necessário
        ]
        df = bq_executor.execute_query_to_dataframe(query, params)
        filename = f"relatorio_divergencias_{id_folha_processada}.{formato}"

    elif nome_relatorio == "conferencia_encargos":
        query = """
            SELECT
                COALESCE(tff.funcionario_cpf, rcs.funcionario_cpf) as funcionario_cpf,
                COALESCE(tff.funcionario_nome_extrato, 'N/A_SISTEMA') as nome_funcionario, 
                rcs.base_inss_empregado_calc as base_inss_sistema, -- Ajustar nome da coluna se mudou
                tff.base_inss_extrato as base_inss_cliente,
                (rcs.base_inss_empregado_calc - tff.base_inss_extrato) as diff_base_inss,
                rcs.valor_inss_empregado_calc as valor_inss_sistema, -- Ajustar nome da coluna se mudou
                tff.valor_inss_descontado_extrato as valor_inss_cliente,
                (rcs.valor_inss_empregado_calc - tff.valor_inss_descontado_extrato) as diff_valor_inss,
                
                rcs.base_fgts_mensal_calc as base_fgts_sistema, -- Ajustar nome da coluna se mudou
                tff.base_fgts_extrato as base_fgts_cliente,
                (rcs.base_fgts_mensal_calc - tff.base_fgts_extrato) as diff_base_fgts,
                rcs.valor_fgts_mensal_calc as valor_fgts_sistema, -- Ajustar nome da coluna se mudou
                tff.valor_fgts_depositado_extrato as valor_fgts_cliente,
                (rcs.valor_fgts_mensal_calc - tff.valor_fgts_depositado_extrato) as diff_valor_fgts,

                rcs.base_irrf_liquida_calc as base_irrf_sistema, -- Ajustar nome da coluna se mudou
                tff.base_irrf_extrato as base_irrf_cliente,
                (rcs.base_irrf_liquida_calc - tff.base_irrf_extrato) as diff_base_irrf,
                rcs.valor_irrf_calc as valor_irrf_sistema, -- Ajustar nome da coluna se mudou
                tff.valor_irrf_retido_extrato as valor_irrf_cliente,
                (rcs.valor_irrf_calc - tff.valor_irrf_retido_extrato) as diff_valor_irrf,

                rcs.total_liquido_calc as liquido_sistema, -- Ajustar nome da coluna se mudou
                tff.total_liquido_funcionario_extrato as liquido_cliente,
                (rcs.total_liquido_calc - tff.total_liquido_funcionario_extrato) as diff_liquido

            FROM auditoria_folha_dataset.ResultadosCalculoSistemaFolha rcs
            FULL OUTER JOIN auditoria_folha_dataset.TotaisFolhaFuncionario tff 
                ON rcs.funcionario_cpf = tff.funcionario_cpf 
                AND rcs.id_folha_processada_fk = tff.id_folha_processada_fk
            WHERE (rcs.id_folha_processada_fk = @id_folha OR tff.id_folha_processada_fk = @id_folha)
            -- AND rcs.id_cliente = @id_cliente_param -- Adicionar se a tabela ResultadosCalculoSistemaFolha tiver id_cliente
            -- AND tff.id_cliente = @id_cliente_param -- Adicionar se a tabela TotaisFolhaFuncionario tiver id_cliente
            ORDER BY funcionario_cpf
        """
        params = [
            bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha_processada),
            # bigquery.ScalarQueryParameter("id_cliente_param", "STRING", id_cliente), # Se necessário
        ]
        df = bq_executor.execute_query_to_dataframe(query, params)
        filename = f"relatorio_conferencia_encargos_{id_folha_processada}.{formato}"
    
    elif nome_relatorio == "composicao_bases_sistema":
        # Esta query precisaria ser adaptada para buscar e processar o JSON da coluna
        # 'json_detalhamento_composicao_bases' da tabela ResultadosCalculoSistemaFolha.
        # Por enquanto, manteremos o comportamento de "não implementado" ou retornar vazio.
        # query = "SELECT ... FROM auditoria_folha_dataset.ResultadosCalculoSistemaFolha WHERE ..."
        # df = bq_executor.execute_query_to_dataframe(query, params)
        # ... (lógica de processamento do JSON para DataFrame) ...
        filename = f"relatorio_composicao_bases_{id_folha_processada}.{formato}"
        df = pd.DataFrame([{"aviso": "Relatório de composição de bases ainda não implementado."}])
        # Ou: raise HTTPException(status_code=501, detail=f"Relatório '{nome_relatorio}' ainda não implementado.")

    else:
        raise HTTPException(status_code=400, detail=f"Relatório '{nome_relatorio}' não suportado.")

    if df.empty and nome_relatorio != "composicao_bases_sistema":
        if formato == "csv":
            return "".encode('utf-8-sig'), filename 
        elif formato == "xlsx":
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                pd.DataFrame([{"status": "Nenhum dado encontrado para este relatório."}]).to_excel(writer, sheet_name='Relatorio', index=False)
            return output.getvalue(), filename

    try:
        if formato == "csv":
            output = io.StringIO()
            df.to_csv(output, index=False, sep=';', encoding='utf-8-sig')
            return output.getvalue().encode('utf-8-sig'), filename
        elif formato == "xlsx":
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Relatorio', index=False)
            return output.getvalue(), filename
    except Exception as e:
        print(f"Erro ao formatar relatório para {formato}: {e}") # Substituir por logging
        raise HTTPException(status_code=500, detail=f"Erro ao formatar o relatório para {formato}.")
    
    # Este raise não deve ser alcançado se tudo correr bem
    raise HTTPException(status_code=400, detail="Formato de relatório não suportado ou erro inesperado na formatação.")
