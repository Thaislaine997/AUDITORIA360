import os

# Estrutura esperada do projeto
expected_structure = {
    "src": ["main.py", "docai_utils.py", "chat_utils.py", "email_utils.py"],
    "config": ["config.json", "config_login.yaml"],
    "deploy": ["cloudbuild.yaml"],
    "scripts": ["compilar_instalador_windows.bat"],
    ".": ["requirements.txt", "README.md"]
}

# Caminho base do projeto
base_path = os.getcwd()
errors = []

# Verificar a estrutura do projeto
for folder, files in expected_structure.items():
    folder_path = os.path.join(base_path, folder)
    if not os.path.exists(folder_path):
        errors.append(f"Faltando diretório: {folder}")
        continue
    for file in files:
        file_path = os.path.join(folder_path, file)
        if not os.path.exists(file_path):
            errors.append(f"Faltando arquivo: {file_path}")

# Exibir resultados
if errors:
    print("Problemas encontrados:")
    for error in errors:
        print(f"- {error}")
else:
    print("Estrutura do projeto está de acordo com o esperado.")