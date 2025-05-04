# painel.py

import os

def verificar_sessao():
    if not os.path.exists("session.txt"):
        print("Você precisa fazer login primeiro.")
        exit()

    with open("session.txt", "r") as f:
        return f.read().strip()

def painel(usuario):
    print(f"\nBem-vindo ao Painel, {usuario}!")
    print("1. Adicionar Cliente")
    print("2. Cadastrar Financeiro")
    print("3. Visualizar Relatórios")
    print("4. Sair")

    escolha = input("Escolha uma opção: ")
    if escolha == "4":
        os.remove("session.txt")
        print("Logout efetuado.")
    else:
        print(f"Você escolheu a opção {escolha}. (em desenvolvimento)")

if __name__ == "__main__":
    usuario_logado = verificar_sessao()
    painel(usuario_logado)
