#!/usr/bin/env python3
"""
Script seguro para criar ou resetar o usuário admin no arquivo /config/gestor_contas.json.
- Gera hash bcrypt seguro para a senha.
- Sobrescreve ou cria o usuário admin.
- Uso: python3 reset_admin.py --username admin --password NOVA_SENHA [--client-id ADMIN001]
"""
import argparse
import json
import os
import sys
from getpass import getpass

try:
    import bcrypt
except ImportError:
    print("[ERRO] O módulo 'bcrypt' não está instalado. Instale com: pip install bcrypt")
    sys.exit(1)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "config", "gestor_contas.json"))


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def load_users(path: str) -> dict:
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(path: str, users: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Cria ou reseta o usuário admin no gestor_contas.json")
    parser.add_argument("--username", default="admin", help="Nome de usuário do admin (padrão: admin)")
    parser.add_argument("--password", help="Senha do admin (se não informado, será solicitado)")
    parser.add_argument("--client-id", default="ADMIN001", help="Client ID do admin (padrão: ADMIN001)")
    args = parser.parse_args()

    username = args.username
    password = args.password or getpass(f"Digite a nova senha para '{username}': ")
    client_id = args.client_id

    if not password or len(password) < 8:
        print("[ERRO] A senha deve ter pelo menos 8 caracteres.")
        sys.exit(1)

    users = load_users(CONFIG_PATH)
    hashed = hash_password(password)
    users[username] = {
        "username": username,
        "hashed_password": hashed,
        "client_id": client_id,
        "disabled": False,
        "is_admin": True
    }
    save_users(CONFIG_PATH, users)
    print(f"[OK] Usuário admin '{username}' criado/resetado com sucesso em {CONFIG_PATH}.")

if __name__ == "__main__":
    main()
