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
