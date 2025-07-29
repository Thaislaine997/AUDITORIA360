"""
Common validation functions and Pydantic models for AUDITORIA360 API
Provides consistent validation across all endpoints
"""

import re
from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, validator

from .responses import ErrorDetail, validation_error


class BaseValidationModel(BaseModel):
    """Base model with common validation configuration"""
    
    class Config:
        # Pydantic v2 compatible configuration
        extra = "forbid"
        # Use enum values instead of names
        use_enum_values = True
        # Validate assignment
        validate_assignment = True
        # Allow population by field name or alias (Pydantic v2)
        validate_by_name = True


class PaginationParams(BaseValidationModel):
    """Standard pagination parameters"""
    
    page: int = Field(1, ge=1, le=1000, description="Page number (1-based)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    @validator('page')
    def validate_page(cls, v):
        if v < 1:
            raise validation_error("Page must be greater than 0", field="page", value=v)
        return v
    
    @validator('page_size')
    def validate_page_size(cls, v):
        if v > 100:
            raise validation_error("Page size cannot exceed 100", field="page_size", value=v)
        return v


class DateRangeParams(BaseValidationModel):
    """Standard date range parameters"""
    
    start_date: Optional[datetime] = Field(None, description="Start date (ISO format)")
    end_date: Optional[datetime] = Field(None, description="End date (ISO format)")
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise validation_error(
                    "End date must be after start date",
                    field="end_date",
                    value=v
                )
        return v


class SortParams(BaseValidationModel):
    """Standard sorting parameters"""
    
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: Optional[str] = Field("asc", pattern="^(asc|desc)$", description="Sort order")
    
    @validator('sort_order')
    def validate_sort_order(cls, v):
        if v not in ['asc', 'desc']:
            raise validation_error(
                "Sort order must be 'asc' or 'desc'",
                field="sort_order",
                value=v
            )
        return v


class StandardListParams(PaginationParams, DateRangeParams, SortParams):
    """Combined standard parameters for list endpoints"""
    
    search: Optional[str] = Field(None, max_length=100, description="Search term")
    active_only: Optional[bool] = Field(None, description="Filter only active records")
    
    @validator('search')
    def validate_search(cls, v):
        if v is not None and len(v.strip()) < 2:
            raise validation_error(
                "Search term must be at least 2 characters",
                field="search",
                value=v
            )
        return v.strip() if v else v


def validate_cpf(cpf: str) -> bool:
    """
    Validate Brazilian CPF number
    
    Args:
        cpf: CPF string to validate
    
    Returns:
        bool: True if valid CPF
    """
    # Remove non-digit characters
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Check length
    if len(cpf) != 11:
        return False
    
    # Check for known invalid CPFs (all same digits)
    if cpf in ['00000000000', '11111111111', '22222222222', '33333333333',
               '44444444444', '55555555555', '66666666666', '77777777777',
               '88888888888', '99999999999']:
        return False
    
    # Calculate first check digit
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder1 = sum1 % 11
    digit1 = 0 if remainder1 < 2 else 11 - remainder1
    
    # Calculate second check digit
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder2 = sum2 % 11
    digit2 = 0 if remainder2 < 2 else 11 - remainder2
    
    # Verify check digits
    return int(cpf[9]) == digit1 and int(cpf[10]) == digit2


def validate_cnpj(cnpj: str) -> bool:
    """
    Validate Brazilian CNPJ number
    
    Args:
        cnpj: CNPJ string to validate
    
    Returns:
        bool: True if valid CNPJ
    """
    # Remove non-digit characters
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    # Check length
    if len(cnpj) != 14:
        return False
    
    # Check for known invalid CNPJs
    if cnpj in ['00000000000000', '11111111111111', '22222222222222']:
        return False
    
    # Calculate first check digit
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
    remainder1 = sum1 % 11
    digit1 = 0 if remainder1 < 2 else 11 - remainder1
    
    # Calculate second check digit
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
    remainder2 = sum2 % 11
    digit2 = 0 if remainder2 < 2 else 11 - remainder2
    
    # Verify check digits
    return int(cnpj[12]) == digit1 and int(cnpj[13]) == digit2


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        bool: True if valid email format
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate Brazilian phone number
    
    Args:
        phone: Phone string to validate
    
    Returns:
        bool: True if valid phone format
    """
    # Remove non-digit characters
    phone = re.sub(r'[^0-9]', '', phone)
    
    # Check if it's a valid Brazilian phone number (10 or 11 digits)
    return len(phone) in [10, 11] and phone[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def validate_postal_code(postal_code: str) -> bool:
    """
    Validate Brazilian postal code (CEP)
    
    Args:
        postal_code: CEP string to validate
    
    Returns:
        bool: True if valid CEP format
    """
    # Remove non-digit characters
    postal_code = re.sub(r'[^0-9]', '', postal_code)
    
    # Check if it's 8 digits
    return len(postal_code) == 8


def validate_money_amount(amount: Union[int, float, str]) -> bool:
    """
    Validate monetary amount
    
    Args:
        amount: Amount to validate
    
    Returns:
        bool: True if valid monetary amount
    """
    try:
        value = float(amount)
        return value >= 0 and value <= 999999999.99  # Max 999 million
    except (ValueError, TypeError):
        return False


class CPFValidator:
    """Pydantic validator for CPF fields"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise validation_error("CPF must be a string", value=value)
        
        if not validate_cpf(value):
            raise validation_error("Invalid CPF format", field="cpf", value=value)
        
        return value


class CNPJValidator:
    """Pydantic validator for CNPJ fields"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise validation_error("CNPJ must be a string", value=value)
        
        if not validate_cnpj(value):
            raise validation_error("Invalid CNPJ format", field="cnpj", value=value)
        
        return value


def validate_required_fields(data: dict, required_fields: List[str]) -> List[ErrorDetail]:
    """
    Validate that required fields are present and not empty
    
    Args:
        data: Data dictionary to validate
        required_fields: List of required field names
    
    Returns:
        List[ErrorDetail]: List of validation errors
    """
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(ErrorDetail(
                field=field,
                message=f"Field '{field}' is required",
                code="MISSING_FIELD"
            ))
        elif data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
            errors.append(ErrorDetail(
                field=field,
                message=f"Field '{field}' cannot be empty",
                code="EMPTY_FIELD",
                value=data[field]
            ))
    
    return errors


def validate_field_lengths(data: dict, field_limits: dict) -> List[ErrorDetail]:
    """
    Validate field length limits
    
    Args:
        data: Data dictionary to validate
        field_limits: Dictionary mapping field names to max lengths
    
    Returns:
        List[ErrorDetail]: List of validation errors
    """
    errors = []
    
    for field, max_length in field_limits.items():
        if field in data and isinstance(data[field], str):
            if len(data[field]) > max_length:
                errors.append(ErrorDetail(
                    field=field,
                    message=f"Field '{field}' exceeds maximum length of {max_length}",
                    code="FIELD_TOO_LONG",
                    value=len(data[field])
                ))
    
    return errors