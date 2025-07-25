# generate_hash.py
import streamlit_authenticator as stauth

# Senha que você quer hashear
plain_password = '41283407'

<<<<<<< HEAD
print("Tentando hashear a senha.")
=======
print("Tentando hashear uma senha.")
>>>>>>> 5f80f61 (Correções de segurança: senhas agora são hasheadas e não registradas em texto simples)

try:
    hashed_password = stauth.Hasher().hash(plain_password)
    if hashed_password:
        print(f"Senha hasheada: {hashed_password}")
    else:
        print("Erro: Nenhuma senha hasheada foi gerada.")
except Exception as e:
    print(f"Erro ao gerar hash: {e}")
