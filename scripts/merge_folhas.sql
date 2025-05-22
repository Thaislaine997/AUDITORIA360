MERGE `auditoria-folha.controle_folha_dataset.folhas` T
USING (
  SELECT
    CONCAT(cnpj_empresa, '_', FORMAT_DATE('%Y%m', mes_ano_referencia)) AS id_folha,
    mes_ano_referencia,
    cnpj_empresa,
    status_aba_origem,
    status_valor_cliente,
    nome_arquivo_origem
  FROM `auditoria-folha.controle_folha_dataset.control_folha_planilha_raw_data`
) S
ON T.id_folha = S.id_folha
WHEN MATCHED AND EXISTS(
  SELECT 1 FROM `auditoria-folha.controle_folha_dataset.status_map` SM
  WHERE SM.status_aba = S.status_aba_origem
    AND SM.status_valor = S.status_valor_cliente
)
THEN UPDATE SET
  status        = (SELECT status_final FROM `auditoria-folha.controle_folha_dataset.status_map` SM
                   WHERE SM.status_aba = S.status_aba_origem
                     AND SM.status_valor = S.status_valor_cliente),
  data_envio_cliente = IF((SELECT data_field FROM `auditoria-folha.controle_folha_dataset.status_map` SM
                           WHERE SM.status_aba = S.status_aba_origem
                             AND SM.status_valor = S.status_valor_cliente) = 'data_envio_cliente', CURRENT_TIMESTAMP(), T.data_envio_cliente),
  data_guia_fgts     = IF((SELECT data_field FROM `auditoria-folha.controle_folha_dataset.status_map` SM
                           WHERE SM.status_aba = S.status_aba_origem
                             AND SM.status_valor = S.status_valor_cliente) = 'data_guia_fgts', CURRENT_TIMESTAMP(), T.data_guia_fgts),
  data_darf_inss     = IF((SELECT data_field FROM `auditoria-folha.controle_folha_dataset.status_map` SM
                           WHERE SM.status_aba = S.status_aba_origem
                             AND SM.status_valor = S.status_valor_cliente) = 'data_darf_inss', CURRENT_TIMESTAMP(), T.data_darf_inss),
  observacoes        = CONCAT('Atualizado via ', S.nome_arquivo_origem, ' (', S.status_aba_origem, ')')
WHEN NOT MATCHED THEN
  INSERT (id_folha, codigo_empresa, cnpj_empresa, mes_ano, status, observacoes)
  VALUES (
    S.id_folha,
    (SELECT codigo_empresa FROM `auditoria-folha.controle_folha_dataset.empresas` E WHERE E.cnpj = S.cnpj_empresa),
    S.cnpj_empresa,
    S.mes_ano_referencia,
    'Pendente Documentação',
    CONCAT('Criado via ', S.nome_arquivo_origem)
  );