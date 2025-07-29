"""
Standardized error handling and response models for AUDITORIA360 API
Provides consistent error formats and HTTP status codes across all endpoints
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


class ErrorCode(str, Enum):
    """Standardized error codes for AUDITORIA360 API"""
    
    # Authentication and Authorization
    AUTHENTICATION_FAILED = "AUTH_001"
    AUTHORIZATION_FAILED = "AUTH_002"
    TOKEN_EXPIRED = "AUTH_003"
    INVALID_CREDENTIALS = "AUTH_004"
    
    # Validation Errors
    INVALID_INPUT = "VAL_001"
    MISSING_REQUIRED_FIELD = "VAL_002"
    INVALID_FORMAT = "VAL_003"
    INVALID_RANGE = "VAL_004"
    
    # Business Logic Errors
    RESOURCE_NOT_FOUND = "BIZ_001"
    RESOURCE_CONFLICT = "BIZ_002"
    OPERATION_NOT_ALLOWED = "BIZ_003"
    BUSINESS_RULE_VIOLATION = "BIZ_004"
    
    # System Errors
    INTERNAL_SERVER_ERROR = "SYS_001"
    SERVICE_UNAVAILABLE = "SYS_002"
    DATABASE_ERROR = "SYS_003"
    EXTERNAL_SERVICE_ERROR = "SYS_004"
    
    # Processing Errors
    FILE_PROCESSING_ERROR = "PROC_001"
    OCR_PROCESSING_ERROR = "PROC_002"
    CALCULATION_ERROR = "PROC_003"
    EXPORT_ERROR = "PROC_004"


class ErrorDetail(BaseModel):
    """Detailed error information"""
    
    field: Optional[str] = Field(None, description="Field that caused the error")
    message: str = Field(..., description="Human-readable error message")
    code: Optional[str] = Field(None, description="Specific error code")
    value: Optional[Any] = Field(None, description="Invalid value that caused the error")


class StandardResponse(BaseModel):
    """Standard API response format"""
    
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Human-readable message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Unique request identifier for tracking")


class SuccessResponse(StandardResponse):
    """Standard success response format"""
    
    success: bool = Field(True, description="Always true for success responses")
    data: Optional[Any] = Field(None, description="Response data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ErrorResponse(StandardResponse):
    """Standard error response format"""
    
    success: bool = Field(False, description="Always false for error responses")
    error_code: ErrorCode = Field(..., description="Standardized error code")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information")
    trace_id: Optional[str] = Field(None, description="Error trace identifier for debugging")


class PaginationMetadata(BaseModel):
    """Pagination metadata for list responses"""
    
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_items: int = Field(..., ge=0, description="Total number of items")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class PaginatedResponse(SuccessResponse):
    """Paginated response format for list endpoints"""
    
    data: List[Any] = Field(..., description="List of items")
    pagination: PaginationMetadata = Field(..., description="Pagination information")


def create_success_response(
    data: Any = None,
    message: str = "Operation completed successfully",
    metadata: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> SuccessResponse:
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        metadata: Additional metadata
        request_id: Request tracking ID
    
    Returns:
        SuccessResponse: Standardized success response
    """
    return SuccessResponse(
        message=message,
        data=data,
        metadata=metadata,
        request_id=request_id
    )


def create_paginated_response(
    items: List[Any],
    page: int,
    page_size: int,
    total_items: int,
    message: str = "Items retrieved successfully",
    request_id: Optional[str] = None
) -> PaginatedResponse:
    """
    Create a standardized paginated response
    
    Args:
        items: List of items for current page
        page: Current page number
        page_size: Items per page
        total_items: Total number of items
        message: Success message
        request_id: Request tracking ID
    
    Returns:
        PaginatedResponse: Standardized paginated response
    """
    total_pages = (total_items + page_size - 1) // page_size
    
    pagination = PaginationMetadata(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return PaginatedResponse(
        message=message,
        data=items,
        pagination=pagination,
        request_id=request_id
    )


def create_error_response(
    error_code: ErrorCode,
    message: str,
    details: Optional[List[ErrorDetail]] = None,
    trace_id: Optional[str] = None,
    request_id: Optional[str] = None
) -> ErrorResponse:
    """
    Create a standardized error response
    
    Args:
        error_code: Standardized error code
        message: Error message
        details: Detailed error information
        trace_id: Error trace identifier
        request_id: Request tracking ID
    
    Returns:
        ErrorResponse: Standardized error response
    """
    return ErrorResponse(
        message=message,
        error_code=error_code,
        details=details or [],
        trace_id=trace_id,
        request_id=request_id
    )


class APIException(HTTPException):
    """
    Custom API exception with standardized error response
    """
    
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[List[ErrorDetail]] = None,
        trace_id: Optional[str] = None
    ):
        self.error_code = error_code
        self.error_message = message
        self.details = details or []
        self.trace_id = trace_id
        
        # Create standardized error response
        error_response = create_error_response(
            error_code=error_code,
            message=message,
            details=details,
            trace_id=trace_id
        )
        
        super().__init__(
            status_code=status_code,
            detail=error_response.dict()
        )


# Convenience functions for common error types
def validation_error(
    message: str,
    field: Optional[str] = None,
    value: Optional[Any] = None,
    details: Optional[List[ErrorDetail]] = None
) -> APIException:
    """Create a validation error"""
    error_details = details or []
    if field:
        error_details.append(ErrorDetail(
            field=field,
            message=message,
            code=ErrorCode.INVALID_INPUT,
            value=value
        ))
    
    return APIException(
        error_code=ErrorCode.INVALID_INPUT,
        message=message,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=error_details
    )


def not_found_error(resource: str, identifier: str) -> APIException:
    """Create a resource not found error"""
    return APIException(
        error_code=ErrorCode.RESOURCE_NOT_FOUND,
        message=f"{resource} not found: {identifier}",
        status_code=status.HTTP_404_NOT_FOUND
    )


def unauthorized_error(message: str = "Authentication required") -> APIException:
    """Create an unauthorized error"""
    return APIException(
        error_code=ErrorCode.AUTHENTICATION_FAILED,
        message=message,
        status_code=status.HTTP_401_UNAUTHORIZED
    )


def forbidden_error(message: str = "Insufficient permissions") -> APIException:
    """Create a forbidden error"""
    return APIException(
        error_code=ErrorCode.AUTHORIZATION_FAILED,
        message=message,
        status_code=status.HTTP_403_FORBIDDEN
    )


def conflict_error(message: str) -> APIException:
    """Create a conflict error"""
    return APIException(
        error_code=ErrorCode.RESOURCE_CONFLICT,
        message=message,
        status_code=status.HTTP_409_CONFLICT
    )


def internal_server_error(message: str = "Internal server error") -> APIException:
    """Create an internal server error"""
    return APIException(
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def service_unavailable_error(service: str) -> APIException:
    """Create a service unavailable error"""
    return APIException(
        error_code=ErrorCode.SERVICE_UNAVAILABLE,
        message=f"Service temporarily unavailable: {service}",
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE
    )