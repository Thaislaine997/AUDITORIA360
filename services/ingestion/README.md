# services/ingestion/

Pipeline de ingestão de dados:
- `config_loader.py`: carrega configs YAML/env
- `main.py`: entrypoint (Cloud Function/Run)
- `docai_utils.py`: integração Document AI
- `generate_data_hash.py`: hash SHA256 de arquivos
- `bq_loader.py`: inserção otimizada no BigQuery
