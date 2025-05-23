CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.Tabela_Folha_Pagamento` (
    id_folha STRING NOT NULL OPTIONS(description="Identificador único da folha de pagamento processada"),
    id_funcionario STRING NOT NULL OPTIONS(description="Identificador único do funcionário"),
    nome_funcionario STRING OPTIONS(description="Nome do funcionário"),
    cpf_funcionario STRING OPTIONS(description="CPF do funcionário"),
    cargo STRING OPTIONS(description="Cargo do funcionário"),
    competencia DATE NOT NULL OPTIONS(description="Mês/Ano de referência da folha (ex: 2025-05-01)"),
    salario_base NUMERIC OPTIONS(description="Salário base do funcionário"),
    horas_trabalhadas NUMERIC OPTIONS(description="Total de horas normais trabalhadas"),
    horas_extras_50 NUMERIC OPTIONS(description="Total de horas extras com 50%"),
    horas_extras_100 NUMERIC OPTIONS(description="Total de horas extras com 100%"),
    adicional_noturno NUMERIC OPTIONS(description="Valor do adicional noturno"),
    adicional_insalubridade NUMERIC OPTIONS(description="Valor do adicional de insalubridade"),
    adicional_periculosidade NUMERIC OPTIONS(description="Valor do adicional de periculosidade"),
    valor_vale_transporte NUMERIC OPTIONS(description="Valor do vale transporte creditado"),
    desconto_vale_transporte NUMERIC OPTIONS(description="Valor do desconto do vale transporte"),
    valor_vale_refeicao NUMERIC OPTIONS(description="Valor do vale refeição/alimentação creditado"),
    desconto_vale_refeicao NUMERIC OPTIONS(description="Valor do desconto do vale refeição/alimentação"),
    desconto_inss NUMERIC OPTIONS(description="Valor do desconto do INSS"),
    desconto_irrf NUMERIC OPTIONS(description="Valor do desconto do IRRF"),
    outros_descontos NUMERIC OPTIONS(description="Soma de outros descontos"),
    total_proventos NUMERIC OPTIONS(description="Soma de todos os proventos"),
    total_descontos NUMERIC OPTIONS(description="Soma de todos os descontos"),
    valor_liquido NUMERIC OPTIONS(description="Valor líquido a receber"),
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Quando o registro foi inserido/processado")
);

CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.Tabela_Regras_CCT` (
    id_regra STRING NOT NULL OPTIONS(description="Identificador único da regra extraída"),
    id_cct STRING NOT NULL OPTIONS(description="Identificador da CCT de origem"),
    nome_sindicato STRING OPTIONS(description="Nome do sindicato associado à CCT"),
    vigencia_inicio DATE OPTIONS(description="Data de início da vigência da CCT/regra"),
    vigencia_fim DATE OPTIONS(description="Data de fim da vigência da CCT/regra"),
    tipo_regra STRING OPTIONS(description="Tipo da regra (ex: PISO_SALARIAL, HORA_EXTRA, BENEFICIO_VT, ADICIONAL_INSALUBRIDADE)"),
    cargo_aplicavel STRING OPTIONS(description="Cargo específico ao qual a regra se aplica (NULL se aplicável a todos)"),
    parametro_1 STRING OPTIONS(description="Parâmetro principal da regra (ex: Percentual HE, Valor diário VR)"),
    parametro_2 STRING OPTIONS(description="Parâmetro secundário (ex: Base de cálculo, Limite de desconto)"),
    valor_regra NUMERIC OPTIONS(description="Valor numérico da regra (ex: Piso salarial, Valor fixo benefício)"),
    texto_clausula STRING OPTIONS(description="Trecho original da cláusula da CCT (para referência)"),
    fonte_documento STRING OPTIONS(description="Nome/Caminho do arquivo PDF da CCT"),
    data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Quando a regra foi extraída")
);

CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.Tabela_Auditoria_Folha` (
    id_auditoria STRING NOT NULL OPTIONS(description="Identificador único da auditoria"),
    id_folha STRING NOT NULL OPTIONS(description="Referência à folha de pagamento auditada"),
    id_regra STRING OPTIONS(description="Referência à regra da CCT aplicada (se houver)"),
    tipo_divergencia STRING OPTIONS(description="Tipo de divergência encontrada (ex: SALARIO_INCORRETO, BENEFICIO_INCORRETO)"),
    mensagem_auditoria STRING OPTIONS(description="Descrição detalhada da auditoria/divergência"),
    status_auditoria STRING OPTIONS(description="Status da auditoria (ex: PENDENTE, RESOLVIDO, IGNORADO)"),
    data_auditoria TIMESTAMP DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Quando a auditoria foi realizada")
);

CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.Tabela_Extratos` (
    id_extracao STRING NOT NULL OPTIONS(description="Identificador único do processamento do extrato"),
    id_transacao STRING NOT NULL OPTIONS(description="Identificador único da transação dentro do extrato"),
    nome_arquivo_origem STRING OPTIONS(description="Nome do arquivo de extrato original"),
    data_transacao DATE OPTIONS(description="Data em que a transação ocorreu"),
    descricao STRING OPTIONS(description="Descrição da transação conforme extraída"),
    valor_transacao NUMERIC OPTIONS(description="Valor da transação (positivo para créditos, negativo para débitos)"),
    tipo_transacao STRING OPTIONS(description="Tipo inferido (ex: PAGAMENTO, TRANSFERENCIA, DEPOSITO, TARIFA)"),
    banco_origem STRING OPTIONS(description="Banco associado ao extrato (se disponível)"),
    agencia STRING OPTIONS(description="Agência associada ao extrato (se disponível)"),
    conta STRING OPTIONS(description="Conta associada ao extrato (se disponível)"),
    confianca_extracao FLOAT64 OPTIONS(description="Pontuação de confiança geral da extração do Document AI para esta transação"),
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Quando o registro foi inserido/processado")
);

-- Épico 1.4: Tabelas de Salário Mínimo e FGTS
CREATE TABLE IF NOT EXISTS `auditoria-folha.Tabelas_legais_dataseet.TabelaSalarioMinimoHistorico` (
    id_versao STRING NOT NULL OPTIONS(description="Identificador único para esta versão da tabela de Salário Mínimo"),
    data_inicio_vigencia DATE NOT NULL OPTIONS(description="Data em que esta versão da tabela começa a valer"),
    data_fim_vigencia DATE OPTIONS(description="Data em que esta versão da tabela deixa de valer. Nulo se for a versão atualmente ativa."),
    descricao STRING OPTIONS(description="Descrição ou observação sobre esta versão da tabela"),
    data_criacao_registro TIMESTAMP NOT NULL OPTIONS(description="Quando esta entrada de versão foi criada no sistema"),
    data_ultima_modificacao TIMESTAMP NOT NULL OPTIONS(description="Quando esta entrada de versão foi modificada pela última vez"),
    data_inativacao TIMESTAMP OPTIONS(description="Data e hora em que esta versão do registro foi inativada (deleção lógica). Nulo se estiver ativa."),
    valor_nacional NUMERIC NOT NULL OPTIONS(description="Valor do salário mínimo nacional"),
    valores_regionais JSON OPTIONS(description="JSON contendo valores de salários mínimos regionais. Ex: {'SP': 1500.00, 'RJ': 1450.00}"),
    observacao STRING OPTIONS(description="Observações adicionais sobre esta vigência do salário mínimo")
)
PARTITION BY DATE_TRUNC(data_inicio_vigencia, MONTH)
CLUSTER BY id_versao
OPTIONS(
    description="Histórico das tabelas de Salário Mínimo com suas vigências.",
    labels=[("auditoria360", "parametros_legais")]
);

CREATE TABLE IF NOT EXISTS `auditoria-folha.Tabelas_legais_dataseet.TabelaFGTSParametros` (
    id_versao STRING NOT NULL OPTIONS(description="Identificador único para esta versão dos parâmetros de FGTS"),
    data_inicio_vigencia DATE NOT NULL OPTIONS(description="Data em que esta versão dos parâmetros começa a valer"),
    data_fim_vigencia DATE OPTIONS(description="Data em que esta versão dos parâmetros deixa de valer. Nulo se for a versão atualmente ativa."),
    descricao STRING OPTIONS(description="Descrição ou observação sobre esta versão dos parâmetros"),
    data_criacao_registro TIMESTAMP NOT NULL OPTIONS(description="Quando esta entrada de versão foi criada no sistema"),
    data_ultima_modificacao TIMESTAMP NOT NULL OPTIONS(description="Quando esta entrada de versão foi modificada pela última vez"),
    data_inativacao TIMESTAMP OPTIONS(description="Data e hora em que esta versão do registro foi inativada (deleção lógica). Nulo se estiver ativa."),
    aliquota_mensal NUMERIC NOT NULL OPTIONS(description="Alíquota mensal padrão do FGTS (ex: 0.08 para 8%)"),
    aliquota_multa_rescisoria NUMERIC NOT NULL OPTIONS(description="Alíquota da multa rescisória do FGTS (ex: 0.40 para 40%)"),
    observacao STRING OPTIONS(description="Observações adicionais sobre esta vigência dos parâmetros de FGTS")
)
PARTITION BY DATE_TRUNC(data_inicio_vigencia, MONTH)
CLUSTER BY id_versao
OPTIONS(
    description="Histórico dos parâmetros de FGTS com suas vigências.",
    labels=[("auditoria360", "parametros_legais")]
);

CREATE TABLE IF NOT EXISTS LogVerificacaoManualParametros (
    id_log_verificacao STRING NOT NULL, -- UUID
    tipo_parametro STRING NOT NULL, -- Ex: "INSS", "IRRF", "SALARIO_MINIMO", "FGTS", "SALARIO_FAMILIA"
    data_verificacao TIMESTAMP NOT NULL,
    usuario_verificacao STRING, -- ID ou nome do usuário admin
    link_verificado STRING,
    houve_alteracao BOOLEAN, -- Opcional: O admin indica se encontrou alteração para ser tratada
    observacao_verificacao STRING,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_log_verificacao) NOT ENFORCED
);
CREATE TABLE IF NOT EXISTS LogVerificacaoManualParametros (
    id_log_verificacao STRING NOT NULL OPTIONS(description="ID único do registro de log (UUID)"),
    tipo_parametro STRING NOT NULL OPTIONS(description="Tipo do parâmetro legal verificado. Ex: INSS, IRRF, SALARIO_MINIMO, FGTS, SALARIO_FAMILIA"),
    data_verificacao TIMESTAMP NOT NULL OPTIONS(description="Data e hora em que a verificação manual foi realizada (UTC)"),
    usuario_verificacao STRING OPTIONS(description="ID ou nome/email do usuário administrador que realizou a verificação"),
    link_verificado STRING OPTIONS(description="URL da fonte oficial que foi consultada durante a verificação"),
    houve_alteracao BOOLEAN OPTIONS(description="Indica se o administrador identificou alguma alteração na fonte oficial que necessita atualização no sistema"),
    observacao_verificacao STRING OPTIONS(description="Observações ou anotações feitas pelo administrador durante a verificação"),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP OPTIONS(description="Data e hora de criação do registro de log"),
    PRIMARY KEY (id_log_verificacao) NOT ENFORCED
)
OPTIONS(
    description="Tabela para registrar as verificações manuais das tabelas de parâmetros legais nas fontes oficiais."
);

-- Novas tabelas para Contabilidades e Usuários de Contabilidade
CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.Contabilidades` (
    id_contabilidade STRING NOT NULL OPTIONS(description="Identificador único da contabilidade (UUID)"),
    cnpj STRING NOT NULL OPTIONS(description="CNPJ da empresa de contabilidade"),
    razao_social STRING OPTIONS(description="Razão Social da empresa de contabilidade"),
    nome_fantasia STRING OPTIONS(description="Nome Fantasia da empresa de contabilidade"),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP OPTIONS(description="Data de cadastro da contabilidade"),
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP OPTIONS(description="Data da última atualização dos dados da contabilidade"),
    ativo BOOLEAN DEFAULT TRUE OPTIONS(description="Indica se a contabilidade está ativa no sistema"),
    PRIMARY KEY (id_contabilidade) NOT ENFORCED,
    UNIQUE (cnpj) NOT ENFORCED -- Garante que cada CNPJ seja único
)
OPTIONS(
    description="Armazena informações cadastrais das empresas de contabilidade parceiras."
);

CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.UsuariosContabilidade` (
    id_usuario_contabilidade STRING NOT NULL OPTIONS(description="Identificador único do usuário da contabilidade (UUID)"),
    id_contabilidade STRING NOT NULL OPTIONS(description="Referência à tabela Contabilidades (FK)"),
    email STRING NOT NULL OPTIONS(description="Email de login do usuário"),
    senha_hash STRING NOT NULL OPTIONS(description="Hash da senha do usuário"),
    nome_usuario STRING OPTIONS(description="Nome do usuário"),
    cargo STRING OPTIONS(description="Cargo do usuário na contabilidade"),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP OPTIONS(description="Data de criação do registro do usuário"),
    data_ultimo_login TIMESTAMP OPTIONS(description="Data do último login do usuário"),
    ativo BOOLEAN DEFAULT TRUE OPTIONS(description="Indica se o usuário está ativo"),
    PRIMARY KEY (id_usuario_contabilidade) NOT ENFORCED,
    FOREIGN KEY (id_contabilidade) REFERENCES `auditoria-folha.dataset_auditoria.Contabilidades`(id_contabilidade) NOT ENFORCED,
    UNIQUE (email) NOT ENFORCED -- Garante que cada email seja único
)
OPTIONS(
    description="Armazena informações dos usuários vinculados às empresas de contabilidade, incluindo credenciais de acesso."
);

-- Tabela para Empresas Clientes da plataforma (hipotética para vinculação automática)
CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.EmpresasClientes` (
    id_empresa_cliente STRING NOT NULL OPTIONS(description="Identificador único da empresa cliente (UUID)"),
    cnpj_empresa STRING NOT NULL OPTIONS(description="CNPJ da empresa cliente"),
    razao_social STRING OPTIONS(description="Razão Social da empresa cliente"),
    nome_fantasia STRING OPTIONS(description="Nome Fantasia da empresa cliente"),
    cnpj_contabilidade_declarado STRING OPTIONS(description="CNPJ da contabilidade que esta empresa declarou como responsável. Usado para vínculo automático."),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP OPTIONS(description="Data de cadastro da empresa cliente"),
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP OPTIONS(description="Data da última atualização dos dados da empresa cliente"),
    ativo BOOLEAN DEFAULT TRUE OPTIONS(description="Indica se a empresa cliente está ativa no sistema"),
    PRIMARY KEY (id_empresa_cliente) NOT ENFORCED,
    UNIQUE (cnpj_empresa) NOT ENFORCED -- Garante que cada CNPJ de empresa cliente seja único
)
OPTIONS(
    description="Armazena informações cadastrais das empresas clientes da plataforma de auditoria."
);

-- Tabela de ligação entre Contabilidades e EmpresasClientes
CREATE TABLE IF NOT EXISTS `auditoria-folha.dataset_auditoria.ContabilidadeEmpresaClienteLink` (
    id_link STRING NOT NULL OPTIONS(description="Identificador único do vínculo (UUID)"),
    id_contabilidade STRING NOT NULL OPTIONS(description="Referência à tabela Contabilidades (FK)"),
    id_empresa_cliente STRING NOT NULL OPTIONS(description="Referência à tabela EmpresasClientes (FK)"),
    data_vinculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP OPTIONS(description="Data em que o vínculo foi estabelecido"),
    ativo BOOLEAN DEFAULT TRUE OPTIONS(description="Indica se o vínculo está ativo"),
    origem_vinculo STRING OPTIONS(description="Como o vínculo foi criado (ex: AUTOMATICO_REGISTRO_CONTABILIDADE, MANUAL_ADMIN)"),
    PRIMARY KEY (id_link) NOT ENFORCED,
    FOREIGN KEY (id_contabilidade) REFERENCES `auditoria-folha.dataset_auditoria.Contabilidades`(id_contabilidade) NOT ENFORCED,
    FOREIGN KEY (id_empresa_cliente) REFERENCES `auditoria-folha.dataset_auditoria.EmpresasClientes`(id_empresa_cliente) NOT ENFORCED,
    UNIQUE (id_contabilidade, id_empresa_cliente) NOT ENFORCED -- Garante que um par contabilidade-cliente seja único
)
OPTIONS(
    description="Tabela de associação entre Contabilidades e as Empresas Clientes que elas atendem."
);