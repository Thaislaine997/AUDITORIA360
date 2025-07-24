import os
import yaml
from pathlib import Path

class Settings:
    def __init__(self):
        base = Path(__file__).parent
        # Carrega YAMLs principais
        self.common = yaml.safe_load((base / 'config_common.yaml').read_text())
        self.docai = yaml.safe_load((base / 'config_docai.yaml').read_text())
        self.ml = yaml.safe_load((base / 'config_ml.yaml').read_text()) if (base / 'config_ml.yaml').exists() else {}
        # Mescla configs
        self.config = {**self.common, **self.docai, **self.ml}
        # Variáveis de ambiente
        self.config['google_application_credentials'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', self.config.get('google_application_credentials'))
        self.config['environment'] = os.getenv('ENVIRONMENT', self.config.get('environment'))
        self.config['log_level'] = os.getenv('LOG_LEVEL', self.config.get('log_level', 'INFO'))
        # Parâmetros específicos
        self.SECRET_KEY_CONTABILIDADE = os.getenv('SECRET_KEY_CONTABILIDADE', 'sua-chave-secreta')
        self.ACCESS_TOKEN_EXPIRE_MINUTES_CONTABILIDADE = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES_CONTABILIDADE', '60'))
        self.BIGQUERY_PROJECT_ID = self.config.get('project_id', 'auditoria360')
        self.BIGQUERY_DATASET_ID = self.config.get('bq_dataset', 'auditoria_folha_dataset')
        # URL base da API (usado pelo dashboard)
        self.API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')

settings = Settings()
