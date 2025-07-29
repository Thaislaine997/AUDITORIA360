# Utilitário para verificação de admin


def verificar_admin(token):
    # Exemplo: considera admin se token contém 'admin'
    return token and "admin" in token
