# Consultas BigQuery Utilizadas no `bq_loader.py`

Este arquivo documenta as principais consultas BigQuery geradas e executadas pela classe `ControleFolhaLoader` no arquivo `src/bq_loader.py`.

## `ControleFolhaLoader`

### 1. `listar_todas_as_empresas()`

**Objetivo:** Lista todas as empresas para o `client_id` atual.

```sql
SELECT 
    codigo_empresa, 
    cnpj, 
    nome_empresa, 
    contato, 
    email, 
    cidade, 
    sindicato, 
    particularidades, 
    forma_envio, 
    data_cadastro, 
    id_contabilidade, 
    id_sindicato, 
    client_id 
FROM 
    `[PROJECT_ID].[DATASET_ID].empresas` 
WHERE 
    client_id = @client_id
```

**Parâmetros:**

- `@client_id`: STRING - O ID do cliente.

### 2. `get_empresa_by_id(empresa_id: int)`

**Objetivo:** Busca uma empresa específica pelo seu `codigo_empresa` e `client_id`.

```sql
SELECT 
    codigo_empresa, 
    cnpj, 
    nome_empresa, 
    contato, 
    email, 
    cidade, 
    sindicato, 
    particularidades, 
    forma_envio, 
    data_cadastro, 
    id_contabilidade, 
    id_sindicato, 
    client_id 
FROM 
    `[PROJECT_ID].[DATASET_ID].empresas` 
WHERE 
    codigo_empresa = @empresa_id AND client_id = @client_id
```

**Parâmetros:**

- `@empresa_id`: INTEGER - O código da empresa.
- `@client_id`: STRING - O ID do cliente.

### 3. `get_folha_by_id(id_folha: str)`

**Objetivo:** Busca uma folha de pagamento específica pelo seu `id_folha` e `client_id`.

```sql
SELECT 
    id_folha, 
    codigo_empresa, 
    cnpj_empresa, 
    mes_ano, 
    status, 
    data_envio_cliente, 
    data_guia_fgts, 
    data_darf_inss, 
    observacoes, 
    client_id 
FROM 
    `[PROJECT_ID].[DATASET_ID].folhas` 
WHERE 
    id_folha = @id_folha AND client_id = @client_id
```

**Parâmetros:**

- `@id_folha`: STRING - O ID da folha.
- `@client_id`: STRING - O ID do cliente.

### 4. `update_folha_status(id_folha: str, novo_status: str)`

**Objetivo:** Atualiza o status de uma folha de pagamento específica.

```sql
UPDATE 
    `[PROJECT_ID].[DATASET_ID].folhas`
SET 
    status = @novo_status
WHERE 
    id_folha = @id_folha AND client_id = @client_id
```

**Parâmetros:**

- `@novo_status`: STRING - O novo status para a folha.
- `@id_folha`: STRING - O ID da folha.
- `@client_id`: STRING - O ID do cliente.

### 5. `consolidar_dados_planilha_para_folhas(nome_arquivo_origem_especifico: str)`

**Objetivo:** Consolida dados da tabela `controle_folha_planilha_raw_data` para a tabela `folhas`, atualizando registros existentes ou inserindo novos.

```sql
MERGE `[PROJECT_ID].[DATASET_ID].folhas` T
USING (
    SELECT
        raw.cnpj_empresa,
        PARSE_DATE('%Y-%m-%d', raw.mes_ano_referencia) AS mes_ano_date,
        raw.nome_arquivo_origem,
        raw.client_id AS source_client_id,
        emp.codigo_empresa,
        CASE
            WHEN emp.codigo_empresa IS NULL THEN 'AGUARDANDO_CADASTRO_EMPRESA'
            ELSE COALESCE(sm.status_final, raw.status_valor_cliente, 'PENDENTE_PROCESSAMENTO')
        END AS status_calculado,
        CASE
            WHEN emp.codigo_empresa IS NULL THEN 'CNPJ não encontrado no cadastro de empresas.'
            ELSE NULL
        END AS observacao_calculada
    FROM `[PROJECT_ID].[DATASET_ID].controle_folha_planilha_raw_data` raw
    LEFT JOIN `[PROJECT_ID].[DATASET_ID].empresas` emp ON raw.cnpj_empresa = emp.cnpj AND raw.client_id = emp.client_id
    LEFT JOIN `[PROJECT_ID].[DATASET_ID].status_map` sm ON raw.status_aba_origem = sm.status_aba AND raw.status_valor_cliente = sm.status_valor AND raw.client_id = sm.client_id
    WHERE raw.nome_arquivo_origem = @nome_arquivo AND raw.client_id = @client_id_param
) S
ON T.cnpj_empresa = S.cnpj_empresa AND T.mes_ano = S.mes_ano_date AND T.client_id = S.source_client_id
WHEN MATCHED THEN
    UPDATE SET
        T.status = S.status_calculado,
        T.observacoes = CASE
                         WHEN T.status = 'AGUARDANDO_CADASTRO_EMPRESA' AND S.codigo_empresa IS NOT NULL THEN NULL
                         ELSE S.observacao_calculada
                       END,
        T.codigo_empresa = S.codigo_empresa,
        T.data_processamento_gcs = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
    INSERT (
        id_folha, codigo_empresa, cnpj_empresa, mes_ano, status,
        client_id, nome_arquivo_origem, observacoes,
        data_envio_cliente, data_guia_fgts, data_darf_inss, data_processamento_gcs
    )
    VALUES (
        GENERATE_UUID(),
        S.codigo_empresa,
        S.cnpj_empresa,
        S.mes_ano_date,
        S.status_calculado,
        S.source_client_id,
        S.nome_arquivo_origem,
        S.observacao_calculada,
        CURRENT_TIMESTAMP(),
        NULL,
        NULL,
        CURRENT_TIMESTAMP()
    );
```

**Parâmetros:**

- `@nome_arquivo`: STRING - O nome do arquivo de origem na tabela `controle_folha_planilha_raw_data`.
- `@client_id_param`: STRING - O ID do cliente.

### 6. `buscar_pendencias_dashboard()`

**Objetivo:** Busca dados de pendências para o dashboard do cliente.

```sql
SELECT 
    tarefa, 
    quantidade_concluida, 
    percentual_concluido, 
    quantidade_pendente, 
    percentual_pendente, 
    data_atualizacao, 
    client_id 
FROM 
    `[PROJECT_ID].[DATASET_ID].dashboard` 
WHERE 
    client_id = @client_id 
ORDER BY 
    data_atualizacao DESC
```

**Parâmetros:**

- `@client_id`: STRING - O ID do cliente.

**Nota:** `[PROJECT_ID]` e `[DATASET_ID]` são placeholders para o ID do projeto GCP e o ID do dataset configurados, respectivamente.
