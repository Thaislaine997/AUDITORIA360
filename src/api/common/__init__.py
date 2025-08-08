"""
Common API utilities, middleware, and response handlers for AUDITORIA360.

This module provides standardized components for:
- Error handling and responses
- Request/response middleware
- Data validation
- Performance monitoring
"""

from .middleware import (
    PerformanceMonitoringMiddleware,
    RequestLoggingMiddleware,
    StandardizedErrorMiddleware,
)
from .responses import (
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    PaginatedResponse,
    StandardResponse,
    SuccessResponse,
    conflict_error,
    create_error_response,
    create_paginated_response,
    create_success_response,
    forbidden_error,
    internal_server_error,
    not_found_error,
    service_unavailable_error,
    unauthorized_error,
    validation_error,
)
from .validators import (
    BaseValidationModel,
    CNPJValidator,
    CPFValidator,
    DateRangeParams,
    PaginationParams,
    SortParams,
    StandardListParams,
    validate_cnpj,
    validate_cpf,
    validate_email,
    validate_field_lengths,
    validate_money_amount,
    validate_phone,
    validate_postal_code,
    validate_required_fields,
)

__all__ = [
    # Middleware
    "PerformanceMonitoringMiddleware",
    "RequestLoggingMiddleware",
    "StandardizedErrorMiddleware",
    # Response models and functions
    "ErrorCode",
    "ErrorDetail",
    "ErrorResponse",
    "PaginatedResponse",
    "StandardResponse",
    "SuccessResponse",
    "create_error_response",
    "create_paginated_response",
    "create_success_response",
    "validation_error",
    "not_found_error",
    "unauthorized_error",
    "forbidden_error",
    "conflict_error",
    "internal_server_error",
    "service_unavailable_error",
    # Validation models and functions
    "BaseValidationModel",
    "PaginationParams",
    "DateRangeParams",
    "SortParams",
    "StandardListParams",
    "CPFValidator",
    "CNPJValidator",
    "validate_cpf",
    "validate_cnpj",
    "validate_email",
    "validate_phone",
    "validate_postal_code",
    "validate_money_amount",
    "validate_required_fields",
    "validate_field_lengths",
]
