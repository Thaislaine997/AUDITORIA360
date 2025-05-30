# test_import.py
try:
    # O caminho correto para o módulo controle_folha_controller.py
    # que está dentro da PASTA src/controllers/
    from src.controllers import controle_folha_controller
    print("Importação de controle_folha_controller bem-sucedida!")
    print(dir(controle_folha_controller)) # Lista o que foi importado
except ImportError as e:
    print(f"Erro na importação: {e}")
except Exception as e:
    print(f"Outro erro: {e}")