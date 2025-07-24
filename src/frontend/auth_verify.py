# Módulo de verificação de autenticação

def verificar_autenticacao(token):
    return bool(token) and len(token) > 10
