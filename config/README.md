
# Configuração Unificada - AUDITORIA360

Esta pasta reúne **todos os arquivos de configuração, scripts utilitários, exemplos de deploy e dependências** do sistema AUDITORIA360. A estrutura foi unificada para facilitar manutenção, automação e documentação.

## Estrutura dos Arquivos

- **config_docai.yaml**: Configuração para integração com Document AI.
- **config_ml.yaml**: Configuração de módulos de machine learning.
- **logging_config.json**: Configuração de logging do sistema.
- **settings.py**: Configurações globais e carregamento dinâmico de variáveis/envs.
- **decrypt_configs.py / encrypt_configs.py**: Scripts para criptografar/descriptografar configs sensíveis.
- **demo_config.py**: Exemplo de configuração (remover se não utilizado).
- **requirements.txt**: Dependências principais do projeto Python.
- **requirements-dev.txt**: Dependências para ambiente de desenvolvimento.
- **requirements-ml.txt**: Dependências para módulos de machine learning.
- **requirements-monitoring.txt**: Dependências para monitoramento do sistema.
- **nginx.conf.example**: Exemplo de configuração para servidores Nginx.
- **.htaccess**: Configuração para servidores Apache.
- **oracle_singularity_validation.json**: Integração/validação com Oracle/Singularity.
- **mcp/**: Subpasta com configs do módulo MCP.

> Edite estes arquivos com cautela. Recomenda-se versionar apenas exemplos e nunca arquivos com segredos reais. Alterações incorretas podem afetar o funcionamento do sistema ou dos ambientes de deploy.

## Recomendações

- **Nunca** armazene segredos reais (senhas, chaves) em arquivos versionados.
- Use os scripts de criptografia para proteger configs sensíveis.
- Consulte sempre este README antes de alterar ou adicionar arquivos nesta pasta.

## Como usar

1. Edite os arquivos de configuração conforme sua necessidade.
2. Instale as dependências com `pip install -r requirements.txt` e demais arquivos conforme o ambiente.
3. Para deploy, utilize os exemplos de configuração de servidor conforme seu stack (Nginx, Apache, etc).
4. Para integração com módulos MCP, utilize a subpasta `mcp/`.

---

**Manutenção:**
- Sempre que adicionar um novo arquivo de configuração, documente-o aqui.
- Remova arquivos obsoletos para evitar confusão.

---

**AUDITORIA360** - Plataforma de Auditoria Inteligente
