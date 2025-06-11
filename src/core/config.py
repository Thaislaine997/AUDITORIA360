import os
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis de ambiente do arquivo .env

class Settings:
    # Configurações do BigQuery
    BIGQUERY_PROJECT_ID: str = os.getenv("BIGQUERY_PROJECT_ID", "auditoria-folha")
    BIGQUERY_DATASET_ID: str = os.getenv("BIGQUERY_DATASET_ID", "dataset_auditoria")
    BIGQUERY_DATASET_LEGAL_ID: str = os.getenv("BIGQUERY_DATASET_LEGAL_ID", "Tabelas_legais_dataseet") # Novo dataset para tabelas legais

    # Configurações de Autenticação para API (usadas no JWT)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua-chave-secreta-supersegura")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Configurações de Autenticação para Contabilidades (mantidas para compatibilidade)
    SECRET_KEY_CONTABILIDADE: str = os.getenv("SECRET_KEY_CONTABILIDADE", "your_super_secret_key_for_contabilidades_32_chars")
    ACCESS_TOKEN_EXPIRE_MINUTES_CONTABILIDADE: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES_CONTABILIDADE", 30))

    # Configurações de Fontes Oficiais (exemplo, pode vir de um JSON ou DB)
    # Esta parte é mais para o param_legais_controller, mas centralizar aqui pode ser útil
    FONTES_OFICIAIS_CONFIG_FILE: str = "src/config.json"

    # URL base da API para comunicação frontend-backend
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

    # Outras configurações globais
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
