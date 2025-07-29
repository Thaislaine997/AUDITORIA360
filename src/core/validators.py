"""
Validation utilities for AUDITORIA360.
Consolidated from services/core/validators.py
"""

import re
from typing import Any

from .exceptions import ValidationError


def validate_cpf(cpf: str) -> bool:
    """
    Validate Brazilian CPF number.
    """
    if not cpf or not isinstance(cpf, str):
        return False
    
    # Remove non-numeric characters
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # CPF must have 11 digits
    if len(cpf) != 11:
        return False
    
    # Check for repeated digits
    if cpf == cpf[0] * 11:
        return False
    
    # Validate check digits
    def calculate_digit(cpf_digits, position):
        sum_digits = sum(int(digit) * weight for digit, weight in zip(cpf_digits, range(position, 1, -1)))
        remainder = sum_digits % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Check first digit
    first_digit = calculate_digit(cpf[:9], 10)
    if first_digit != int(cpf[9]):
        return False
    
    # Check second digit
    second_digit = calculate_digit(cpf[:10], 11)
    if second_digit != int(cpf[10]):
        return False
    
    return True


def validate_cnpj(cnpj: str) -> bool:
    """
    Validate Brazilian CNPJ number.
    """
    if not cnpj or not isinstance(cnpj, str):
        return False
    
    # Remove non-numeric characters
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    # CNPJ must have 14 digits
    if len(cnpj) != 14:
        return False
    
    # Check for repeated digits
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validate check digits
    def calculate_digit(cnpj_digits, weights):
        sum_digits = sum(int(digit) * weight for digit, weight in zip(cnpj_digits, weights))
        remainder = sum_digits % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Check first digit
    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    first_digit = calculate_digit(cnpj[:12], weights_1)
    if first_digit != int(cnpj[12]):
        return False
    
    # Check second digit
    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_digit = calculate_digit(cnpj[:13], weights_2)
    if second_digit != int(cnpj[13]):
        return False
    
    return True


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    """
    if not email or not isinstance(email, str):
        return False
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_required_fields(data: dict, required_fields: list) -> None:
    """
    Validate that all required fields are present and not empty.
    """
    missing_fields = []
    empty_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            empty_fields.append(field)
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    if empty_fields:
        raise ValidationError(f"Empty required fields: {', '.join(empty_fields)}")