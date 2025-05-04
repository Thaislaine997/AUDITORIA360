# main.py

import os

def iniciar():
    if not os.path.exists("session.txt"):
        os.system("python login.py")
    os.system("python painel.py")

if __name__ == "__main__":
    iniciar()
