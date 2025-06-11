# generate_hash.py
import streamlit_authenticator as stauth

# Senha que você quer hashear
plain_password = '41283407'

print(f"Tentando hashear a senha: {plain_password}")

try:
    hashed_password = stauth.Hasher().hash(plain_password)
    if hashed_password:
        print(f"Senha hasheada: {hashed_password}")
    else:
        print("Erro: Nenhuma senha hasheada foi gerada.")
except Exception as e:
    print(f"Erro ao gerar hash: {e}")
