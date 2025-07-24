# Script para descriptografar arquivos da pasta configs
import os
from cryptography.fernet import Fernet
import getpass
import base64
import hashlib

CONFIGS_DIR = 'configs'
KEY_FILE = os.path.join(CONFIGS_DIR, 'configs.key')

def decrypt_file(filepath: str, fernet: Fernet):
    with open(filepath, 'rb') as file:
        encrypted = file.read()
    decrypted = fernet.decrypt(encrypted)
    original_path = filepath[:-4]  # remove .enc
    with open(original_path, 'wb') as file:
        file.write(decrypted)
    os.remove(filepath)

if __name__ == '__main__':
    password = getpass.getpass('Digite a senha para descriptografar os arquivos da pasta configs: ')
    salt = b'AUDITORIA360_CONFIGS_SALT'
    kdf = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    key = base64.urlsafe_b64encode(kdf)
    fernet = Fernet(key)
    for fname in os.listdir(CONFIGS_DIR):
        fpath = os.path.join(CONFIGS_DIR, fname)
        if os.path.isfile(fpath) and fname.endswith('.enc'):
            decrypt_file(fpath, fernet)
    print('Arquivos descriptografados com sucesso!')
