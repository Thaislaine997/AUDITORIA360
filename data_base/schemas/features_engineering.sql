-- SQL script for feature engineering processes

-- This script includes the necessary SQL transformations to create features
-- for the predictive modeling of payroll risks.

-- Example of feature engineering for the payroll dataset

WITH base_data AS (
    SELECT 
        id_folha_processada,
        id_cliente,
        COUNT(rubrica_codigo_original_extrato) AS num_total_rubricas,
        SUM(CASE WHEN status_mapeamento_rubrica = 'NAO_ENCONTRADA' THEN 1 ELSE 0 END) AS num_rubricas_nao_mapeadas,
        COUNT(DISTINCT CASE WHEN severidade_divergencia = 'ALTA' THEN funcionario_cpf END) AS num_funcionarios_com_divergencias_alta_severidade,
        AVG(valor_provento) AS media_valor_proventos,
        AVG(valor_liquido) AS media_valor_liquido,
        -- Add more aggregations as needed
        DATE_DIFF(CURRENT_DATE(), MAX(data_inicio_vigencia), DAY) AS dias_desde_ultima_atualizacao_param_legal
    FROM 
        auditoria_folha_dataset.FolhasProcessadasHeader f
    JOIN 
        auditoria_folha_dataset.LinhasFolhaFuncionario l ON f.id_folha_processada = l.id_folha_processada_fk
    LEFT JOIN 
        auditoria_folha_dataset.DivergenciasAnaliseFolha d ON f.id_folha_processada = d.id_folha_processada_fk
    GROUP BY 
        id_folha_processada, id_cliente
)

SELECT 
    id_folha_processada,
    id_cliente,
    num_total_rubricas,
    num_rubricas_nao_mapeadas / NULLIF(num_total_rubricas, 0) AS perc_rubricas_nao_mapeadas,
    num_funcionarios_com_divergencias_alta_severidade,
    media_valor_proventos,
    media_valor_liquido,
    dias_desde_ultima_atualizacao_param_legal
FROM 
    base_data;