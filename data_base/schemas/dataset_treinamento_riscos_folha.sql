CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.DatasetTreinamentoRiscosFolha (
    id_registro_treinamento STRING NOT NULL OPTIONS(description="ID único do registro no dataset de treinamento (PK)"),
    id_folha_processada_referencia STRING NOT NULL OPTIONS(description="FK para FolhasProcessadasHeader, identificando a folha original"),
    id_cliente_anonimizado STRING OPTIONS(description="ID anonimizado ou representação do perfil do cliente"),
    periodo_referencia_folha DATE NOT NULL,
    
    feature_num_total_rubricas INT64,
    feature_perc_rubricas_nao_mapeadas FLOAT64,
    feature_num_func_div_alta INT64,
    feature_var_total_bruto_3m FLOAT64,
    feature_flag_decimo_terceiro BOOLEAN,
    feature_dias_desde_ult_param_inss INT64,

    target_risco_alta_severidade_ocorreu BOOLEAN NOT NULL OPTIONS(description="TRUE se houve divergência de alta severidade na folha"),
    target_tipo_principal_risco STRING OPTIONS(description="Tipo da divergência mais crítica ou frequente"),
    target_score_risco_observado NUMERIC OPTIONS(description="Score de risco derivado das divergências ocorridas"),
    
    data_geracao_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Quando este registro de treinamento foi gerado")
) OPTIONS (
    description="Dataset consolidado e preparado para treinamento de modelos de previsão de riscos na folha de pagamento."
);