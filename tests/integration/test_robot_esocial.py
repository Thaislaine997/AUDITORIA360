"""
Teste de uso do Robô eSocial automático.
"""

import os

from robot_esocial import RoboESocial

# Exemplo de uso (substitua por credenciais válidas e caminho do XML)
USUARIO = os.getenv("ESOCIAL_USUARIO", "seu_usuario")
SENHA = os.getenv("ESOCIAL_SENHA", "sua_senha")
CAMINHO_XML = os.getenv("XML_PATH", "/caminho/para/arquivo.xml")

if __name__ == "__main__":
    robo = RoboESocial(USUARIO, SENHA)
    try:
        robo.iniciar()
        robo.upload_xml(CAMINHO_XML)
        status = robo.fetch_status()
        print(f"Status do envio: {status}")
        robo.emitir_guia()
    finally:
        robo.finalizar()
