import os
import yaml
from pathlib import Path

def load_config():
    # Define path para configs
    base = Path(__file__).parent.parent / 'configs'

    # Carrega arquivos YAML
    common_cfg = yaml.safe_load((base / 'config_common.yaml').read_text())
    docai_cfg = yaml.safe_load((base / 'config_docai.yaml').read_text())

    # Mescla configurações
    cfg = {**common_cfg, **docai_cfg}

    # Carrega variáveis de ambiente para sobrepor
    cfg['google_application_credentials'] = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS',
        cfg.get('google_application_credentials')
    )
    cfg['environment'] = os.getenv(
        'ENVIRONMENT',
        cfg.get('environment')
    )
    cfg['log_level'] = os.getenv(
        'LOG_LEVEL',
        cfg.get('log_level', 'INFO')
    )

    return cfg
