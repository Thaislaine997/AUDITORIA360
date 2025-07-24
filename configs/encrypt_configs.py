# Este script criptografa todos os arquivos da pasta configs usando uma senha definida pelo usuário.
import os
from cryptography.fernet import Fernet
import getpass
import sys
import base64
import hashlib

CONFIGS_DIR = 'configs'
KEY_FILE = os.path.join(CONFIGS_DIR, 'configs.key')

# Gera uma chave a partir da senha do usuário
def generate_key(password: str) -> bytes:
    # Deriva uma chave de 32 bytes a partir da senha usando PBKDF2
    salt = b'AUDITORIA360_CONFIGS_SALT'  # Pode ser customizado ou salvo em arquivo
    kdf = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.urlsafe_b64encode(kdf)

# Criptografa um arquivo
def encrypt_file(filepath: str, fernet: Fernet):
    with open(filepath, 'rb') as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(filepath + '.enc', 'wb') as file:
        file.write(encrypted)
    os.remove(filepath)

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            password = sys.argv[1]
        else:
            password = input('Digite uma senha forte para criptografar os arquivos da pasta configs: ')
        key = generate_key(password)
        fernet = Fernet(key)
        with open(KEY_FILE, 'wb') as kf:
            kf.write(key)
        for fname in os.listdir(CONFIGS_DIR):
            fpath = os.path.join(CONFIGS_DIR, fname)
            if os.path.isfile(fpath) and not fname.endswith('.key') and not fname.endswith('.enc'):
                try:
                    encrypt_file(fpath, fernet)
                except Exception as e:
                    print(f'Erro ao criptografar {fname}: {e}')
        print('Arquivos criptografados com sucesso! Guarde a senha e o arquivo configs.key para descriptografar.')
    except Exception as e:
        print(f'Erro geral: {e}')
