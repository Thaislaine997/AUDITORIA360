# Auditoria de Folha com Document AI e BigQuery

Este projeto automatiza o processamento de documentos de folha de pagamento em formato PDF. Ele utiliza o Google Cloud Document AI para extrair informações relevantes dos PDFs e armazena os dados estruturados no Google Cloud BigQuery para análises e auditorias futuras.

## Arquitetura e Fluxo de Dados

O fluxo de processamento é projetado da seguinte forma:

1. **Upload de PDF:** Um arquivo PDF de folha de pagamento é carregado no bucket do Google Cloud Storage (GCS) `auditoria-folha-input-pdfs`.
2. **Acionamento do Cloud Run:** A criação de um novo objeto (arquivo PDF) no bucket GCS aciona o serviço Google Cloud Run. Este acionamento é tipicamente configurado via Eventarc, que monitora o bucket e invoca o endpoint do Cloud Run.
3. **Processamento com Document AI:** O serviço Cloud Run, ao ser acionado, recebe o nome do arquivo PDF. Ele então lê o arquivo do GCS e o envia para um processador específico do Google Cloud Document AI. Este processador é treinado ou configurado para extrair entidades relevantes das folhas de pagamento.
4. **Armazenamento no BigQuery:** Os dados extraídos e estruturados pelo Document AI são então formatados e carregados pelo serviço Cloud Run em uma tabela no Google Cloud BigQuery, especificamente no dataset `auditoria_folha_dataset` e tabela `docai_extracted_data`.

## Configuração

### Variáveis de Ambiente (Cloud Run)

As seguintes variáveis de ambiente são cruciais e devem ser configuradas no serviço Cloud Run:

* `GCP_PROJECT_ID`: O ID do seu projeto Google Cloud.
* `GCP_LOCATION`: A região onde seu processador Document AI está localizado (ex: `us`, `eu`). Esta é a localização do *endpoint* do Document AI.
* `DOCAI_PROCESSOR_ID`: O ID do seu processador Document AI específico para folhas de pagamento.
* `GCS_INPUT_BUCKET`: O nome do bucket GCS onde os PDFs de entrada são carregados. Atualmente configurado como `auditoria-folha-input-pdfs`.
* `BQ_DATASET_ID`: O ID do dataset no BigQuery. Atualmente configurado como `auditoria_folha_dataset`.
* `BQ_TABLE_ID`: O ID da tabela no BigQuery. Atualmente configurado como `docai_extracted_data`.

### Conta de Serviço (Cloud Run)

O serviço Cloud Run `processador-pdf-folha` executa utilizando a Conta de Serviço Padrão do Compute Engine (`333253866645-compute@developer.gserviceaccount.com` neste projeto). Esta conta de serviço deve possuir, no mínimo, os seguintes papéis para o correto funcionamento:

* `Leitor de objetos do Storage` (para ler PDFs do GCS).
* `Usuário da API Document AI` (ou um papel mais específico como `Analisador do Document AI`).
* `Editor de dados BigQuery` (para inserir dados na tabela do BigQuery).
* `Gravador de registros` (para escrever logs no Cloud Logging).

### Desenvolvimento Local

Para desenvolvimento e testes locais, um arquivo `src/config.json` pode ser utilizado para fornecer as configurações acima. O formato esperado é:

```json
// filepath: src/config.json
{
  "gcp_project_id": "SEU_PROJECT_ID",
  "gcp_location": "SUA_REGIAO_DOCAI",
  "docai_processor_id": "SEU_PROCESSOR_ID_DOCAI",
  "gcs_input_bucket": "SEU_BUCKET_GCS_INPUT",
  "bq_dataset_id": "SEU_DATASET_BQ",
  "bq_table_id": "SUA_TABELA_BQ"
}
```

**Nota:** Ao rodar localmente, garanta que seu ambiente está autenticado com o Google Cloud, seja via `gcloud auth application-default login` ou configurando a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` para apontar para um arquivo de chave de conta de serviço com as permissões necessárias.

## Como Executar Localmente (Exemplo)

1. **Clone o repositório:**

   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```

2. **Crie e ative um ambiente virtual (recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

   Para recursos de IA Gemini, instale também:

   ```bash
   pip install google-generativeai
   ```

4. **Autentique-se no Google Cloud:**

   ```bash
   gcloud auth application-default login
   ```

   Ou configure a variável `GOOGLE_APPLICATION_CREDENTIALS`.

5. **Crie e configure o arquivo `src/config.json`** com suas configurações de desenvolvimento.

6. **Execute a aplicação principal** (o ponto de entrada pode variar dependendo de como seu `main.py` está estruturado):

   ```bash
   # Exemplo, ajuste conforme sua implementação (ex: se for um servidor Flask/FastAPI ou um script direto)
   # python main.py
   ```

## Deploy

O deploy para o Google Cloud Run é automatizado via Google Cloud Build. Qualquer push para o branch `main` acionará o pipeline definido no arquivo `cloudbuild.yaml`. Este pipeline constrói a imagem do contêiner da aplicação e a implanta no serviço Cloud Run `processador-pdf-folha`. O Cloud Build utiliza a conta de serviço `auditoria-folha@appspot.gserviceaccount.com` para suas operações, conforme configurado no gatilho.

## Segurança

* **Endpoint do Cloud Run:** O serviço Cloud Run `processador-pdf-folha` está configurado para **exigir autenticação**. Isso significa que apenas chamadas autenticadas com uma identidade IAM que possua o papel de `Invocador do Cloud Run` (roles/run.invoker) podem acionar o serviço.
* **Entrada (Ingress):** Recomenda-se configurar a entrada do serviço Cloud Run para **"Permitir tráfego interno apenas"** se o acionamento vier exclusivamente de fontes internas do GCP (como Eventarc), para maior segurança.
* **Princípio do Menor Privilégio:** Embora atualmente utilize a conta de serviço padrão do Compute Engine, para ambientes de produção mais robustos, é recomendado criar uma conta de serviço dedicada para o Cloud Run com apenas os papéis estritamente necessários.

## Informações do BigQuery

Os dados extraídos são armazenados na seguinte tabela:

* **Projeto:** (Definido por `GCP_PROJECT_ID`)
* **Dataset:** `auditoria_folha_dataset` (ou o valor de `BQ_DATASET_ID`)
* **Tabela:** `docai_extracted_data` (ou o valor de `BQ_TABLE_ID`)

### Schema da Tabela `docai_extracted_data`

| Nome do campo       | Tipo      | Modo     | Descrição (Exemplo)                     |
| :------------------ | :-------- | :------- | :-------------------------------------- |
| id_extracao         | STRING    | NULLABLE | Identificador único da extração do arquivo |
| id_item             | STRING    | REQUIRED | Identificador único do item/entidade extraída |
| nome_arquivo_origem | STRING    | NULLABLE | Nome do arquivo PDF original processado |
| pagina              | INTEGER   | NULLABLE | Número da página onde a entidade foi encontrada no PDF |
| tipo_campo          | STRING    | NULLABLE | Tipo da entidade extraída (ex: `nome_funcionario`, `salario_base`) |
| texto_extraido      | STRING    | NULLABLE | O texto exato como extraído pelo Document AI |
| valor_limpo         | STRING    | NULLABLE | Valor após limpeza ou formatação (se aplicável) |
| valor_numerico      | FLOAT     | NULLABLE | Valor convertido para formato numérico (se aplicável) |
| confianca           | FLOAT     | NULLABLE | Pontuação de confiança da extração fornecida pelo Document AI |
| timestamp_carga     | TIMESTAMP | REQUIRED | Data e hora (UTC) em que o registro foi carregado no BigQuery |

Nota: Ajuste a coluna "Descrição (Exemplo)" conforme os dados e a lógica de extração do seu projeto.

## Estrutura do Projeto (Principais Arquivos)

* `main.py`: Ponto de entrada da aplicação Cloud Run. Responsável por receber o evento de trigger (ex: do GCS via Eventarc), orquestrar o processamento do PDF com `docai_utils` e o carregamento dos dados com `bq_loader`.
* `src/docai_utils.py`: Módulo contendo a lógica para interagir com a API do Google Cloud Document AI. Responsável por enviar o documento para processamento e extrair as entidades relevantes.
* `src/bq_loader.py`: Módulo contendo a lógica para carregar os dados extraídos e estruturados na tabela apropriada do BigQuery.
* `requirements.txt`: Lista todas as dependências Python necessárias para o projeto.
* `cloudbuild.yaml`: Arquivo de configuração do Google Cloud Build. Define os passos para construir a imagem do contêiner e realizar o deploy no Cloud Run.
* `Dockerfile`: Contém as instruções para construir a imagem do contêiner Docker da aplicação, especificando o ambiente de execução e as dependências.

## Testes Automatizados e Padronização

Todos os testes utilizam mocks globais para dependências externas, garantindo que o projeto pode ser testado localmente ou em CI sem credenciais reais do Google Cloud. Os testes estão em `tests/` e o arquivo `conftest.py` centraliza os mocks para BigQuery, Storage, Document AI e autenticação.

Para rodar os testes:

```bash
pytest --maxfail=3 --disable-warnings -v
```

## Relatório de Lacunas

O arquivo `relatorio_lacunas_atualizado.csv` traz o status dos arquivos, cobertura de testes, comentários e recomendações. Use-o para acompanhar o progresso da padronização e identificar pontos de melhoria.

## Contribuição

Contribuições são bem-vindas! Siga as diretrizes:
- Crie branches a partir de `main`.
- Faça PRs pequenos e bem documentados.
- Sempre rode os testes antes de submeter PR.
- Consulte o roadmap e o relatório de lacunas para priorizar melhorias.

## Roadmap

- [x] Unificação dos schemas em `src/schemas/`
- [x] Remoção de código legado
- [x] Mocks globais para testes
- [x] Cobertura total dos testes CCT
- [ ] Finalizar padronização global
- [ ] Enriquecer documentação técnica
- [ ] Garantir 100% dos testes passando
- [ ] Automatizar deploy e CI/CD

## Documentação Técnica

Consulte a pasta `docs/` para guias detalhados de integração, autenticação, checklist de auditoria, onboarding e uso dos principais módulos. Recomenda-se gerar a documentação técnica com Sphinx ou ReadTheDocs para facilitar o acesso e manutenção.

## Diagrama de Arquitetura

![Diagrama de Arquitetura](assets/logo.png)

> **Fluxo Resumido:**
> [Usuário] -> [Upload PDF] -> [GCS Bucket] -> [Eventarc] -> [Cloud Run] -> [Document AI] -> [BigQuery]

---
