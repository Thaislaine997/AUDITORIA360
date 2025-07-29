import re
from datetime import datetime
from typing import Any, Dict, List, Optional

def is_valid_cpf(cpf: str) -> bool:
    """Validate Brazilian CPF number."""
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
        check = ((value * 10) % 11) % 10
        if check != int(cpf[i]):
            return False
    return True

def validate_cpf(cpf: str) -> bool:
    """Alias for is_valid_cpf for consistency."""
    return is_valid_cpf(cpf)

def validate_cnpj(cnpj: str) -> bool:
    """Validate Brazilian CNPJ number."""
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14:
        return False
    
    # Calculate first check digit
    weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_products = sum(int(cnpj[i]) * weights[i] for i in range(12))
    check_digit_1 = (sum_products % 11)
    check_digit_1 = 0 if check_digit_1 < 2 else 11 - check_digit_1
    
    # Calculate second check digit
    weights = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_products = sum(int(cnpj[i]) * weights[i] for i in range(13))
    check_digit_2 = (sum_products % 11)
    check_digit_2 = 0 if check_digit_2 < 2 else 11 - check_digit_2
    
    return int(cnpj[12]) == check_digit_1 and int(cnpj[13]) == check_digit_2

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate Brazilian phone number format."""
    phone = re.sub(r'\D', '', phone)
    return len(phone) in [10, 11] and phone[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def is_iso_date(date_str: str) -> bool:
    """Validate ISO date format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

class DataValidator:
    """Data validation utility class."""
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        return validate_cpf(cpf)
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        return validate_cnpj(cnpj)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        return validate_email(email)
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        return validate_phone(phone)
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        return is_iso_date(date_str)
