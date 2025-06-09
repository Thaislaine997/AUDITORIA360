import os
import json
import getpass

TEMPLATE_CONFIG = {
    "RECAPTCHA_SITE_KEY": "COLE_AQUI_O_SITE_KEY",
    "client_display_name": "NOME DO CLIENTE",
    "branding_logo_url": "https://url-do-logo.png",
    "gcp_project_id": "SEU_PROJECT_ID",
    "bq_dataset_id": "SEU_DATASET_BQ",
    "bq_table_id": "SUA_TABELA_BQ",
    "client_id": "ID_UNICO_CLIENTE"
}

CONFIG_DIR = "src/client_configs/"
LOGIN_YAML = "auth/login.yaml"

def criar_config_cliente():
    nome = input("Nome do cliente (ex: cliente_x): ").strip()
    client_id = input("ID único do cliente (ex: cliente_x): ").strip()
    site_key = input("reCAPTCHA SITE KEY: ").strip()
    display_name = input("Nome de exibição: ").strip()
    logo_url = input("URL do logo: ").strip()
    config = TEMPLATE_CONFIG.copy()
    config["RECAPTCHA_SITE_KEY"] = site_key
    config["client_display_name"] = display_name
    config["branding_logo_url"] = logo_url
    config["client_id"] = client_id
    config_path = os.path.join(CONFIG_DIR, f"{client_id}.json")
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"Arquivo de configuração criado: {config_path}")
    return client_id

def adicionar_usuario_login_yaml(client_id):
    usuario = input(f"Usuário para o cliente {client_id}: ").strip()
    senha = getpass.getpass(f"Senha para {usuario}: ")
    # Adiciona ao login.yaml (simples, sem parser yaml avançado)
    with open(LOGIN_YAML, "a", encoding="utf-8") as f:
        f.write(f"  {usuario}: \"{senha}\"\n")
    print(f"Usuário {usuario} adicionado ao {LOGIN_YAML}")

def main():
    print("--- Onboarding de Novo Cliente White-Label ---")
    client_id = criar_config_cliente()
    adicionar_usuario_login_yaml(client_id)
    print("Onboarding concluído! Valide o branding, login e isolamento de dados.")

if __name__ == "__main__":
    main()
