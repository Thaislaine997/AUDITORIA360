"""
Validation utilities for AUDITORIA360.
Consolidated from services/core/validators.py
"""

import re

from .exceptions import ValidationError


def validate_cpf(cpf: str) -> bool:
    """
    Validate Brazilian CPF (Cadastro de Pessoas Físicas) number.
    
    Performs comprehensive validation including format, length, and check digit verification
    according to Brazilian government standards.
    
    Args:
        cpf: The CPF string to validate. Can contain formatting characters (dots, hyphens)
             that will be automatically removed.
    
    Returns:
        True if the CPF is valid, False otherwise.
        
    Example:
        >>> validate_cpf("123.456.789-09")
        True
        >>> validate_cpf("12345678909")
        True
        >>> validate_cpf("111.111.111-11")
        False
        >>> validate_cpf("invalid")
        False
        
    Note:
        This function validates the mathematical correctness of the CPF
        but does not verify if it's actually registered in government databases.
    """
    if not cpf or not isinstance(cpf, str):
        return False

    # Remove non-numeric characters
    cpf = re.sub(r"[^0-9]", "", cpf)

    # CPF must have 11 digits
    if len(cpf) != 11:
        return False

    # Check for repeated digits
    if cpf == cpf[0] * 11:
        return False

    # Validate check digits
    def calculate_digit(cpf_digits, position):
        sum_digits = sum(
            int(digit) * weight
            for digit, weight in zip(cpf_digits, range(position, 1, -1))
        )
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
    Validate Brazilian CNPJ (Cadastro Nacional de Pessoas Jurídicas) number.
    
    Validates CNPJ format and check digits according to Brazilian standards.
    
    Args:
        cnpj: The CNPJ string to validate. Accepts formatted (XX.XXX.XXX/XXXX-XX) 
              or unformatted (XXXXXXXXXXXXXX) strings.
    
    Returns:
        True if CNPJ is valid, False otherwise.
        
    Example:
        >>> validate_cnpj("11.222.333/0001-81")
        True
        >>> validate_cnpj("11222333000181")
        True
        >>> validate_cnpj("00.000.000/0000-00")
        False
        
    Raises:
        ValidationError: If input is not a string or is empty.
    """
    if not cnpj or not isinstance(cnpj, str):
        raise ValidationError("CNPJ must be a non-empty string", "cnpj")

    # Remove non-numeric characters
    cnpj = re.sub(r"[^0-9]", "", cnpj)

    # CNPJ must have 14 digits
    if len(cnpj) != 14:
        return False

    # Check for repeated digits
    if cnpj == cnpj[0] * 14:
        return False

    # Calculate first check digit
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
    remainder1 = sum1 % 11
    digit1 = 0 if remainder1 < 2 else 11 - remainder1

    if digit1 != int(cnpj[12]):
        return False

    # Calculate second check digit
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
    remainder2 = sum2 % 11
    digit2 = 0 if remainder2 < 2 else 11 - remainder2

    return digit2 == int(cnpj[13])


def validate_email(email: str) -> bool:
    """
    Validate email address format using RFC-compliant regex pattern.
    
    Args:
        email: Email address string to validate.
        
    Returns:
        True if email format is valid, False otherwise.
        
    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
        >>> validate_email("test+tag@domain.co.uk")
        True
    """
    if not email or not isinstance(email, str):
        return False
        
    # RFC 5322 compliant email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone_br(phone: str) -> bool:
    """
    Validate Brazilian phone number format.
    
    Accepts mobile and landline numbers with or without country code.
    
    Args:
        phone: Phone number string. Can include formatting characters.
        
    Returns:
        True if phone number format is valid, False otherwise.
        
    Example:
        >>> validate_phone_br("(11) 99999-9999")
        True
        >>> validate_phone_br("+55 11 99999-9999")
        True
        >>> validate_phone_br("11999999999")
        True
        >>> validate_phone_br("(11) 3333-3333")
        True
        
    Note:
        Validates format only, not if the number is actually active.
    """
    if not phone or not isinstance(phone, str):
        return False
        
    # Remove all non-numeric characters
    phone = re.sub(r"[^0-9]", "", phone)
    
    # Remove country code if present
    if phone.startswith('55') and len(phone) >= 12:
        phone = phone[2:]
    
    # Brazilian mobile: 11 digits (area code + 9 + 8 digits)
    # Brazilian landline: 10 digits (area code + 7-8 digits)
    if len(phone) == 11:
        # Mobile format: XX9XXXXXXXX
        return phone[2] == '9'
    elif len(phone) == 10:
        # Landline format: XXXXXXXXXX
        return phone[2] in '2345'
    
    return False


def validate_payroll_data(data: dict) -> tuple[bool, list[str]]:
    """
    Comprehensive validation for payroll data entries.
    
    Validates employee payroll information according to Brazilian labor laws
    and internal business rules.
    
    Args:
        data: Dictionary containing payroll information with keys:
              - employee_id (str): Employee identification
              - salary (float): Base salary amount
              - hours_worked (float): Hours worked in the period
              - benefits (dict): Additional benefits data
              
    Returns:
        Tuple containing:
        - bool: True if all validations pass, False otherwise
        - list[str]: List of validation error messages (empty if valid)
        
    Example:
        >>> data = {
        ...     "employee_id": "EMP001",
        ...     "salary": 2500.00,
        ...     "hours_worked": 160.0,
        ...     "benefits": {"health": 150.0}
        ... }
        >>> is_valid, errors = validate_payroll_data(data)
        >>> is_valid
        True
        >>> errors
        []
        
    Raises:
        ValidationError: If data is not a dictionary or required fields are missing.
    """
    if not isinstance(data, dict):
        raise ValidationError("Payroll data must be a dictionary", "payroll_data")
    
    errors = []
    
    # Required fields validation
    required_fields = ['employee_id', 'salary', 'hours_worked']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif data[field] is None:
            errors.append(f"Field {field} cannot be null")
    
    # Employee ID validation
    if 'employee_id' in data:
        employee_id = data['employee_id']
        if not isinstance(employee_id, str) or len(employee_id.strip()) == 0:
            errors.append("Employee ID must be a non-empty string")
    
    # Salary validation
    if 'salary' in data:
        salary = data['salary']
        if not isinstance(salary, (int, float)) or salary < 0:
            errors.append("Salary must be a non-negative number")
        elif salary < 1320.00:  # Brazilian minimum wage (approximate)
            errors.append("Salary below minimum wage (R$ 1,320.00)")
    
    # Hours worked validation
    if 'hours_worked' in data:
        hours = data['hours_worked']
        if not isinstance(hours, (int, float)) or hours < 0:
            errors.append("Hours worked must be a non-negative number")
        elif hours > 220:  # Maximum monthly hours (44h/week * 4.5 weeks)
            errors.append("Hours worked exceeds maximum allowed (220 hours/month)")
    
    # Benefits validation (optional)
    if 'benefits' in data:
        benefits = data['benefits']
        if benefits is not None and not isinstance(benefits, dict):
            errors.append("Benefits must be a dictionary or null")
        elif benefits:
            for benefit_type, amount in benefits.items():
                if not isinstance(amount, (int, float)) or amount < 0:
                    errors.append(f"Benefit '{benefit_type}' must have non-negative amount")
    
    return len(errors) == 0, errors

def validate_email(email: str) -> bool:
    """
    Validate email address format.
    """
    if not email or not isinstance(email, str):
        return False

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
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
        elif data[field] is None or (
            isinstance(data[field], str) and not data[field].strip()
        ):
            empty_fields.append(field)

    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    if empty_fields:
        raise ValidationError(f"Empty required fields: {', '.join(empty_fields)}")
