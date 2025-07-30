-- SQL script to query and analyze risk predictions for payroll processing

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.PredicoesRiscoFolha AS
SELECT
    id_predicao_risco,
    id_folha_processada_fk,
    id_cliente,
    id_modelo_vertex_usado,
    versao_modelo_vertex_usado,
    timestamp_predicao,
    probabilidade_risco_alta_severidade,
    classe_risco_predita,
    score_saude_folha_calculado,
    features_utilizadas_json,
    explicacao_predicao_json
FROM
    auditoria_folha_dataset.PredicoesRiscoFolha
WHERE
    timestamp_predicao >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY); 

-- This query retrieves risk predictions generated in the last 30 days for analysis.