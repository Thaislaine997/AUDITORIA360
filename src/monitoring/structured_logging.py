"""
Structured logging configuration for AUDITORIA360
Implements JSON-formatted logging for centralized log analysis (ELK Stack, Loki, etc.)
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class StructuredFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def __init__(self, service_name: str = "auditoria360"):
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "service": self.service_name,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra fields from record
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in [
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "message",
                "exc_info",
                "exc_text",
                "stack_info",
            ]:
                extra_fields[key] = value

        if extra_fields:
            log_entry["extra"] = extra_fields

        return json.dumps(log_entry)


class BusinessLogger:
    """Specialized logger for business events and metrics"""

    def __init__(self):
        self.logger = logging.getLogger("auditoria360.business")

    def log_audit_start(self, audit_id: str, audit_type: str, user_id: str):
        """Log audit process start"""
        self.logger.info(
            "Audit process started",
            extra={
                "event_type": "audit_start",
                "audit_id": audit_id,
                "audit_type": audit_type,
                "user_id": user_id,
                "business_event": True,
            },
        )

    def log_audit_complete(
        self,
        audit_id: str,
        audit_type: str,
        duration: float,
        findings_count: int,
        status: str,
    ):
        """Log audit process completion"""
        self.logger.info(
            "Audit process completed",
            extra={
                "event_type": "audit_complete",
                "audit_id": audit_id,
                "audit_type": audit_type,
                "duration_seconds": duration,
                "findings_count": findings_count,
                "status": status,
                "business_event": True,
            },
        )

    def log_user_login(self, user_id: str, user_type: str, success: bool):
        """Log user login attempt"""
        self.logger.info(
            "User login attempt",
            extra={
                "event_type": "user_login",
                "user_id": user_id,
                "user_type": user_type,
                "success": success,
                "security_event": True,
            },
        )

    def log_report_generation(
        self, report_type: str, user_id: str, generation_time: float, records_count: int
    ):
        """Log report generation"""
        self.logger.info(
            "Report generated",
            extra={
                "event_type": "report_generation",
                "report_type": report_type,
                "user_id": user_id,
                "generation_time_seconds": generation_time,
                "records_count": records_count,
                "business_event": True,
            },
        )

    def log_compliance_check(
        self, check_type: str, entity_id: str, result: str, issues_found: int
    ):
        """Log compliance check result"""
        self.logger.info(
            "Compliance check performed",
            extra={
                "event_type": "compliance_check",
                "check_type": check_type,
                "entity_id": entity_id,
                "result": result,
                "issues_found": issues_found,
                "compliance_event": True,
            },
        )

    def log_document_upload(
        self, document_id: str, document_type: str, user_id: str, file_size: int
    ):
        """Log document upload"""
        self.logger.info(
            "Document uploaded",
            extra={
                "event_type": "document_upload",
                "document_id": document_id,
                "document_type": document_type,
                "user_id": user_id,
                "file_size_bytes": file_size,
                "business_event": True,
            },
        )


class SecurityLogger:
    """Specialized logger for security events"""

    def __init__(self):
        self.logger = logging.getLogger("auditoria360.security")

    def log_access_denied(self, user_id: str, resource: str, action: str):
        """Log access denied event"""
        self.logger.warning(
            "Access denied",
            extra={
                "event_type": "access_denied",
                "user_id": user_id,
                "resource": resource,
                "action": action,
                "security_event": True,
                "severity": "medium",
            },
        )

    def log_suspicious_activity(
        self, user_id: str, activity: str, details: Dict[str, Any]
    ):
        """Log suspicious activity"""
        self.logger.warning(
            "Suspicious activity detected",
            extra={
                "event_type": "suspicious_activity",
                "user_id": user_id,
                "activity": activity,
                "details": details,
                "security_event": True,
                "severity": "high",
            },
        )

    def log_security_breach(
        self, breach_type: str, affected_resources: list, details: Dict[str, Any]
    ):
        """Log security breach"""
        self.logger.error(
            "Security breach detected",
            extra={
                "event_type": "security_breach",
                "breach_type": breach_type,
                "affected_resources": affected_resources,
                "details": details,
                "security_event": True,
                "severity": "critical",
            },
        )


class PerformanceLogger:
    """Specialized logger for performance events"""

    def __init__(self):
        self.logger = logging.getLogger("auditoria360.performance")

    def log_slow_query(self, query: str, duration: float, table: str):
        """Log slow database query"""
        self.logger.warning(
            "Slow database query detected",
            extra={
                "event_type": "slow_query",
                "query": query[:200] + "..." if len(query) > 200 else query,
                "duration_seconds": duration,
                "table": table,
                "performance_event": True,
            },
        )

    def log_api_performance(
        self,
        endpoint: str,
        method: str,
        duration: float,
        status_code: int,
        user_id: Optional[str] = None,
    ):
        """Log API performance"""
        self.logger.info(
            "API request processed",
            extra={
                "event_type": "api_request",
                "endpoint": endpoint,
                "method": method,
                "duration_seconds": duration,
                "status_code": status_code,
                "user_id": user_id,
                "performance_event": True,
            },
        )


def setup_structured_logging(
    level: str = "INFO", service_name: str = "auditoria360"
) -> None:
    """Setup structured logging for the application"""

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler with structured formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(StructuredFormatter(service_name))
    root_logger.addHandler(console_handler)

    # Configure specific loggers
    loggers_config = {
        "auditoria360": level,
        "auditoria360.business": level,
        "auditoria360.security": level,
        "auditoria360.performance": level,
        "uvicorn": "WARNING",  # Reduce uvicorn log noise
        "fastapi": "WARNING",  # Reduce fastapi log noise
    }

    for logger_name, logger_level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, logger_level.upper()))
        logger.propagate = True


# Global logger instances
business_logger = BusinessLogger()
security_logger = SecurityLogger()
performance_logger = PerformanceLogger()


def get_business_logger() -> BusinessLogger:
    """Get business events logger"""
    return business_logger


def get_security_logger() -> SecurityLogger:
    """Get security events logger"""
    return security_logger


def get_performance_logger() -> PerformanceLogger:
    """Get performance events logger"""
    return performance_logger
