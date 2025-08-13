# config

Arquivos e scripts de configuração do sistema AUDITORIA360.

## Descrição dos arquivos principais

<!-- auditoria_gcp.py removido: integração com Google Cloud Platform não utilizada -->
- **config_common.yaml**: Configurações comuns a múltiplos módulos do sistema.
- **config_docai.yaml**: Configuração específica para integração com Document AI.
- **config_ml.yaml**: Configuração de módulos de machine learning.
- **decrypt_configs.py / encrypt_configs.py**: Scripts para criptografar e descriptografar arquivos de configuração sensíveis.
- **demo_config.py**: Exemplo de configuração (remova se não for mais utilizado).
- **logging_config.json**: Configuração de logging do sistema.
- **settings.py**: Configurações gerais do sistema.
<!-- streamlit_config.toml removido: não utilizado -->
- **mcp/**: Subpasta com configurações específicas do módulo MCP.

> Edite estes arquivos com cautela. Recomenda-se versionar apenas exemplos e nunca arquivos com segredos reais.
