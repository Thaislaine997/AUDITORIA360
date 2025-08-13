"""
Structured logging configuration for AUDITORIA360
Provides JSON logging with tenant context for observability and LGPD compliance
"""

import json
import logging
import os
import sys
import time
from typing import Optional, Dict, Any
from contextlib import contextmanager


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        # Get the original log record
        log_entry = {
            "timestamp": time.time(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add tenant context if available
        if hasattr(record, 'tenant_id'):
            log_entry["tenant_id"] = record.tenant_id
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
            
        # Add performance metrics if available
        if hasattr(record, 'duration_ms'):
            log_entry["duration_ms"] = record.duration_ms
        if hasattr(record, 'response_status'):
            log_entry["response_status"] = record.response_status
            
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        # Add extra fields from the record
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                          'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process', 'message']:
                log_entry[key] = value
                
        return json.dumps(log_entry)


def setup_structured_logging(
    service_name: str = "auditoria360",
    log_level: str = None,
    enable_json: bool = None
) -> logging.Logger:
    """Setup structured logging with JSON format"""
    
    # Get configuration from environment
    log_level = log_level or os.getenv("LOG_LEVEL", "INFO")
    enable_json = enable_json if enable_json is not None else os.getenv("LOG_JSON", "true").lower() == "true"
    
    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplication
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    if enable_json:
        # Use JSON formatter for production/structured logging
        console_handler.setFormatter(StructuredFormatter())
    else:
        # Use simple formatter for development
        console_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
    
    logger.addHandler(console_handler)
    
    return logger


@contextmanager
def audit_context(tenant_id: str = None, user_id: str = None, request_id: str = None):
    """Context manager to add tenant/user context to logs"""
    logger = logging.getLogger("auditoria360")
    
    # Store original factory
    old_factory = logging.getLogRecordFactory()
    
    def add_context_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        if tenant_id:
            record.tenant_id = tenant_id
        if user_id:
            record.user_id = user_id
        if request_id:
            record.request_id = request_id
        return record
    
    try:
        logging.setLogRecordFactory(add_context_factory)
        yield logger
    finally:
        logging.setLogRecordFactory(old_factory)


def log_api_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    tenant_id: Optional[str] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None
):
    """Log API request with structured format"""
    logger = logging.getLogger("auditoria360.api")
    
    extra = {
        "event_type": "api_request",
        "method": method,
        "path": path,
        "response_status": status_code,
        "duration_ms": duration_ms,
    }
    
    if tenant_id:
        extra["tenant_id"] = tenant_id
    if user_id:
        extra["user_id"] = user_id
    if request_id:
        extra["request_id"] = request_id
    
    level = logging.WARNING if status_code >= 400 else logging.INFO
    logger.log(level, f"{method} {path} - {status_code} ({duration_ms:.2f}ms)", extra=extra)


def log_security_event(
    event_type: str,
    description: str,
    tenant_id: Optional[str] = None,
    user_id: Optional[str] = None,
    severity: str = "INFO",
    metadata: Optional[Dict[str, Any]] = None
):
    """Log security-related events for audit trail"""
    logger = logging.getLogger("auditoria360.security")
    
    extra = {
        "event_type": "security_event",
        "security_event_type": event_type,
        "severity": severity,
    }
    
    if tenant_id:
        extra["tenant_id"] = tenant_id
    if user_id:
        extra["user_id"] = user_id
    if metadata:
        extra.update(metadata)
    
    level = getattr(logging, severity, logging.INFO)
    logger.log(level, f"Security Event: {event_type} - {description}", extra=extra)


def log_data_access(
    table_name: str,
    operation: str,
    tenant_id: str,
    user_id: str,
    record_count: int = 1,
    request_id: Optional[str] = None
):
    """Log data access for LGPD compliance"""
    logger = logging.getLogger("auditoria360.data_access")
    
    extra = {
        "event_type": "data_access",
        "table_name": table_name,
        "operation": operation,
        "tenant_id": tenant_id,
        "user_id": user_id,
        "record_count": record_count,
    }
    
    if request_id:
        extra["request_id"] = request_id
    
    logger.info(f"Data Access: {operation} on {table_name} ({record_count} records)", extra=extra)


# Initialize structured logging on import
_logger = setup_structured_logging()

# Export commonly used functions
__all__ = [
    "setup_structured_logging",
    "audit_context", 
    "log_api_request",
    "log_security_event",
    "log_data_access",
    "StructuredFormatter"
]