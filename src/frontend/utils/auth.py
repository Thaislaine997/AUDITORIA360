# Utilitário de autenticação para uso em dashboards/pages

def validar_token(token):
    # Exemplo simples de validação
    return bool(token) and len(token) > 10
