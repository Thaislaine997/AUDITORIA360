# c:\Users\55479\Documents\AUDITORIA360\e2e_config.py
import dataclasses

@dataclasses.dataclass
class E2EContext:
    username: str = "test_user_playwright"
    password: str = "password123"
    login_attempts: int = 0
    login_success: bool = False
    # Campos para simular a entrada do usuário, se necessário diretamente no contexto
    # current_username_input: str = "" 
    # current_password_input: str = ""

e2e_context_instance = E2EContext()
