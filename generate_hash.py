# generate_hash.py
import streamlit_authenticator as stauth
import inspect

# Senha que você quer hashear
plain_password = '41283407'
passwords_to_hash = [plain_password]

print(f"Tentando hashear a senha: {plain_password}")

try:
    # Tenta obter a versão da biblioteca
    try:
        print(f"Versão do streamlit-authenticator: {stauth.__version__}")
    except AttributeError:
        print("Não foi possível determinar a versão do streamlit-authenticator.")

    # Tenta obter a assinatura do construtor Hasher
    try:
        print(f"Assinatura de stauth.Hasher.__init__: {inspect.signature(stauth.Hasher.__init__)}")
    except Exception as sig_e:
        print(f"Não foi possível obter a assinatura de Hasher.__init__: {sig_e}")

    # Tenta obter a assinatura do método Hasher.generate
    try:
        # Precisamos de uma instância para inspecionar um método de instância,
        # mas se __init__ falhar, isso não funcionará diretamente.
        # Vamos tentar inspecionar a partir da classe se possível, ou criar uma instância se __init__ for simples.
        if hasattr(stauth.Hasher, 'generate'):
             print(f"Assinatura de stauth.Hasher.generate: {inspect.signature(stauth.Hasher.generate)}")
        else:
            print("Método 'generate' não encontrado diretamente na classe Hasher.")
            # Tentar com uma instância se __init__ não der erro sem args
            try:
                temp_hasher = stauth.Hasher()
                print(f"Assinatura de temp_hasher.generate: {inspect.signature(temp_hasher.generate)}")
            except Exception as inst_e:
                print(f"Não foi possível instanciar Hasher para checar .generate: {inst_e}")

    except Exception as sig_e:
        print(f"Não foi possível obter a assinatura de Hasher.generate: {sig_e}")

    print("\nTentativa 1: Hasher(passwords_to_hash).generate()")
    try:
        hashed_passwords_attempt1 = stauth.Hasher(passwords_to_hash).generate()
        if hashed_passwords_attempt1:
            print(f"  Sucesso: {hashed_passwords_attempt1[0]}")
        else:
            print("  Erro: Nenhuma senha hasheada foi gerada.")
    except Exception as e1:
        print(f"  Falha na Tentativa 1: {e1}")

    print("\nTentativa 2: Hasher().generate(passwords_to_hash)")
    try:
        hasher_instance = stauth.Hasher()
        # Se generate for um método estático ou de classe que espera senhas, isso pode funcionar.
        # Ou se for um método de instância que espera senhas.
        hashed_passwords_attempt2 = hasher_instance.generate(passwords_to_hash)
        if hashed_passwords_attempt2:
            print(f"  Sucesso: {hashed_passwords_attempt2[0]}")
        else:
            print("  Erro: Nenhuma senha hasheada foi gerada.")
    except Exception as e2:
        print(f"  Falha na Tentativa 2: {e2}")
        
    print("\nTentativa 3: Hasher().hash(plain_password) - comum em algumas libs de hash")
    try:
        hasher_instance = stauth.Hasher()
        if hasattr(hasher_instance, 'hash'):
            print(f"  Assinatura de stauth.Hasher.hash: {inspect.signature(hasher_instance.hash)}")
            hashed_password_attempt3 = hasher_instance.hash(plain_password)
            if hashed_password_attempt3:
                print(f"  Sucesso: {hashed_password_attempt3}")
            else:
                print("  Erro: Nenhuma senha hasheada foi gerada.")
        else:
            print("  Método 'hash' não encontrado em Hasher.")
            
    except Exception as e3:
        print(f"  Falha na Tentativa 3: {e3}")

except Exception as e:
    print(f"Ocorreu um erro inesperado no script: {e}")
