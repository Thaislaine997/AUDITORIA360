-- DDLs para tabelas históricas de parâmetros legais do Módulo 1 (AUDITORIA360)

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosINSSHistorico (
    id_parametro_inss STRING NOT NULL,
    data_inicio_vigencia DATE NOT NULL,
    data_fim_vigencia DATE,
    descricao STRING,
    PRIMARY KEY (id_parametro_inss, data_inicio_vigencia) NOT ENFORCED
);

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosINSSFaixas (
    id_parametro_inss STRING NOT NULL,
    faixa_numero INT64 NOT NULL,
    valor_inicial NUMERIC NOT NULL,
    valor_final NUMERIC,
    aliquota NUMERIC NOT NULL,
    PRIMARY KEY (id_parametro_inss, faixa_numero) NOT ENFORCED
);

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosIRRFHistorico (
    id_parametro_irrf STRING NOT NULL,
    data_inicio_vigencia DATE NOT NULL,
    data_fim_vigencia DATE,
    descricao STRING,
    PRIMARY KEY (id_parametro_irrf, data_inicio_vigencia) NOT ENFORCED
);

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosIRRFFaixas (
    id_parametro_irrf STRING NOT NULL,
    faixa_numero INT64 NOT NULL,
    valor_inicial NUMERIC NOT NULL,
    valor_final NUMERIC,
    aliquota NUMERIC NOT NULL,
    deducao NUMERIC,
    PRIMARY KEY (id_parametro_irrf, faixa_numero) NOT ENFORCED
);

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosSalarioFamiliaHistorico (
    id_parametro_salario_familia STRING NOT NULL,
    data_inicio_vigencia DATE NOT NULL,
    data_fim_vigencia DATE,
    descricao STRING,
    PRIMARY KEY (id_parametro_salario_familia, data_inicio_vigencia) NOT ENFORCED
);

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosSalarioFamiliaFaixas (
    id_parametro_salario_familia STRING NOT NULL,
    faixa_numero INT64 NOT NULL,
    valor_inicial NUMERIC NOT NULL,
    valor_final NUMERIC,
    valor_cota NUMERIC NOT NULL,
    PRIMARY KEY (id_parametro_salario_familia, faixa_numero) NOT ENFORCED
);

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosSalarioMinimoHistorico (
    id_parametro_salario_minimo STRING NOT NULL,
    data_inicio_vigencia DATE NOT NULL,
    data_fim_vigencia DATE,
    valor_salario_minimo NUMERIC NOT NULL,
    PRIMARY KEY (id_parametro_salario_minimo, data_inicio_vigencia) NOT ENFORCED
);

CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.ParametrosFGTSHistorico (
    id_parametro_fgts STRING NOT NULL,
    data_inicio_vigencia DATE NOT NULL,
    data_fim_vigencia DATE,
    percentual_fgts NUMERIC NOT NULL,
    PRIMARY KEY (id_parametro_fgts, data_inicio_vigencia) NOT ENFORCED
);

-- Sugestões de atualização de parâmetros (para workflow de IA)
CREATE TABLE IF NOT EXISTS auditoria_folha_dataset.SugestoesAtualizacaoParametros (
    id_sugestao_parametro STRING NOT NULL,
    tipo_parametro STRING NOT NULL,
    valor_sugerido STRING NOT NULL,
    data_inicio_vigencia_sugerida DATE NOT NULL,
    status_sugestao STRING DEFAULT 'PENDENTE_REVISAO_USUARIO',
    usuario_revisao_sugestao STRING,
    data_revisao_sugestao TIMESTAMP,
    notas_revisao_sugestao STRING,
    timestamp_geracao_sugestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (id_sugestao_parametro) NOT ENFORCED
);
