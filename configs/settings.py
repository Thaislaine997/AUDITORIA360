import os
from pathlib import Path

import yaml


class Settings:
    def __init__(self):
        base = Path(__file__).parent
        # Carrega YAMLs principais
        self.common = yaml.safe_load((base / "config_common.yaml").read_text())
        self.docai = yaml.safe_load((base / "config_docai.yaml").read_text())
        self.ml = (
            yaml.safe_load((base / "config_ml.yaml").read_text())
            if (base / "config_ml.yaml").exists()
            else {}
        )
        # Mescla configs
        self.config = {**self.common, **self.docai, **self.ml}
        # Carrega variáveis do .env.cloudsql se existir
        env_path = base.parent / ".env.cloudsql"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.strip() and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()
        # Variáveis de ambiente
        self.config["google_application_credentials"] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS",
            self.config.get("google_application_credentials"),
        )
        self.config["environment"] = os.getenv(
            "ENVIRONMENT", self.config.get("environment")
        )
        self.config["log_level"] = os.getenv(
            "LOG_LEVEL", self.config.get("log_level", "INFO")
        )
        # Database configuration is centralized in src/models/database.py
        self.config["cloud_sql_instance"] = os.getenv("CLOUD_SQL_INSTANCE")
        self.config["cloud_sql_internal_ip"] = os.getenv("CLOUD_SQL_INTERNAL_IP")
        self.config["cloud_sql_external_ip"] = os.getenv("CLOUD_SQL_EXTERNAL_IP")
        self.config["cloud_sql_db_name"] = os.getenv("CLOUD_SQL_DB_NAME")
        self.config["cloud_sql_db_user"] = os.getenv("CLOUD_SQL_DB_USER")
        self.config["cloud_sql_db_password"] = os.getenv("CLOUD_SQL_DB_PASSWORD")
        self.config["cloud_sql_db_port"] = os.getenv("CLOUD_SQL_DB_PORT")
        self.config["service_account"] = os.getenv("SERVICE_ACCOUNT")
        # Parâmetros específicos
        self.SECRET_KEY_CONTABILIDADE = os.getenv(
            "SECRET_KEY_CONTABILIDADE", "sua-chave-secreta"
        )
        self.ACCESS_TOKEN_EXPIRE_MINUTES_CONTABILIDADE = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES_CONTABILIDADE", "60")
        )
        self.BIGQUERY_PROJECT_ID = self.config.get("project_id", "auditoria360")
        self.BIGQUERY_DATASET_ID = self.config.get(
            "bq_dataset", "auditoria_folha_dataset"
        )
        # URL base da API (usado pelo dashboard)
        self.API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")


settings = Settings()
