from services.core.validators import is_valid_cpf, is_iso_date

if __name__ == "__main__":
    print("CPF válido:", is_valid_cpf("123.456.789-09"))
    print("Data ISO válida:", is_iso_date("2025-07-22"))
