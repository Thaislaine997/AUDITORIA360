"""
Custom exceptions for AUDITORIA360 backend.
"""


class AuditoriaException(Exception):
    """Base exception for AUDITORIA360 application."""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "AUDITORIA_ERROR"
        super().__init__(self.message)


class ValidationError(AuditoriaException):
    """Exception raised for data validation errors."""

    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")


class AuthenticationError(AuditoriaException):
    """Exception raised for authentication errors."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR")


class AuthorizationError(AuditoriaException):
    """Exception raised for authorization errors."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, "AUTHZ_ERROR")


class ProcessingError(AuditoriaException):
    """Exception raised for document/data processing errors."""

    def __init__(self, message: str, processing_type: str = None):
        self.processing_type = processing_type
        super().__init__(message, "PROCESSING_ERROR")
