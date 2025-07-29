# Checklist de Validação do Schema BigQuery – Controle de Folhas

Este checklist garante que a tabela do BigQuery está compatível com o ciclo de "Gestão de Controle de Folhas".

## 1. Estrutura da Tabela

- [ ] Dataset correto (ex: `controle_folhas_dataset`)
- [ ] Nome da tabela: `folhas`
- [ ] Coluna `client_id` (STRING, REQUIRED) para isolamento multi-cliente
- [ ] Coluna `id_folha` (STRING, PRIMARY KEY)
- [ ] Coluna `codigo_empresa` (INTEGER ou STRING, conforme sistema)
- [ ] Coluna `cnpj_empresa` (STRING)
- [ ] Coluna `mes_ano` (DATE ou STRING no formato YYYY-MM-DD)
- [ ] Coluna `status` (STRING)
- [ ] Colunas de datas: `data_envio_cliente`, `data_guia_fgts`, `data_darf_inss` (DATE ou TIMESTAMP)
- [ ] Coluna `observacoes` (STRING)
- [ ] Coluna `sindicato_id_aplicavel` (STRING, opcional)

## 2. Tipos e Restrições

- [ ] Tipos compatíveis com os dados enviados pelo backend
- [ ] Campos obrigatórios definidos como REQUIRED
- [ ] Campos opcionais como NULLABLE

## 3. Permissões

- [ ] Conta de serviço do Cloud Run com permissão de Editor no BigQuery
- [ ] Permissão de leitura/escrita apenas no dataset do cliente

## 4. Testes

- [ ] Teste de inserção de registro real via API
- [ ] Teste de consulta filtrada por client_id, empresa, mês, ano
- [ ] Teste de isolamento: dados de um cliente não aparecem para outro

---

**Dica:** Compare o schema real da tabela com o arquivo `docs/bigquery_schema.sql` do projeto.
