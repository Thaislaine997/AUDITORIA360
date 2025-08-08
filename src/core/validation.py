"""
Input Validation and Sanitization Layer for AUDITORIA360
Prevents SQL injection, XSS, and other injection attacks
"""

import logging
import re
from functools import wraps
from typing import Any, Dict, List

import bleach

logger = logging.getLogger(__name__)


class InputValidator:
    """Comprehensive input validation and sanitization"""

    # Patterns for validation
    SQL_INJECTION_PATTERNS = [
        r"(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)",
        r"(\b(or|and)\s+\d+\s*=\s*\d+)",
        r"(\b(or|and)\s+['\"][\w\s]*['\"](\s*=\s*|\s+like\s+)['\"][\w\s]*['\"])",
        r"(--|\/\*|\*\/|;)",
        r"(\bcast\s*\(|\bconvert\s*\()",
        r"(\bexec\s*\(|\bsp_)",
        r"(\bxp_|\bcmd\s*shell)",
    ]

    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
        r"<link[^>]*>",
        r"<meta[^>]*>",
    ]

    SAFE_SQL_IDENTIFIER_PATTERN = r"^[a-zA-Z0-9_-]+$"
    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    @classmethod
    def validate_sql_identifier(cls, identifier: str, max_length: int = 100) -> bool:
        """
        Validate SQL identifier (table names, column names, etc.)

        Args:
            identifier: String to validate
            max_length: Maximum allowed length

        Returns:
            bool: True if identifier is safe to use
        """
        if not identifier or not isinstance(identifier, str):
            return False

        if len(identifier) > max_length:
            return False

        return bool(re.match(cls.SAFE_SQL_IDENTIFIER_PATTERN, identifier))

    @classmethod
    def sanitize_sql_input(cls, value: str) -> str:
        """
        Sanitize input to prevent SQL injection

        Args:
            value: Input string to sanitize

        Returns:
            str: Sanitized string

        Raises:
            ValueError: If input contains SQL injection patterns
        """
        if not isinstance(value, str):
            return str(value)

        # Check for SQL injection patterns
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"Potential SQL injection attempt blocked: {pattern}")
                raise ValueError("Input contains potentially dangerous SQL patterns")

        # Escape single quotes
        return value.replace("'", "''")

    @classmethod
    def sanitize_html_input(cls, value: str, allowed_tags: List[str] = None) -> str:
        """
        Sanitize HTML input to prevent XSS attacks

        Args:
            value: Input string to sanitize
            allowed_tags: List of allowed HTML tags

        Returns:
            str: Sanitized HTML string
        """
        if not isinstance(value, str):
            return str(value)

        # Default allowed tags (very restrictive)
        if allowed_tags is None:
            allowed_tags = ["b", "i", "u", "em", "strong", "p", "br"]

        # Check for XSS patterns
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"Potential XSS attempt blocked: {pattern}")
                # Remove the dangerous content
                value = re.sub(pattern, "", value, flags=re.IGNORECASE)

        # Use bleach to clean HTML
        clean_value = bleach.clean(value, tags=allowed_tags, attributes={}, strip=True)

        return clean_value

    @classmethod
    def validate_email(cls, email: str) -> bool:
        """
        Validate email address format

        Args:
            email: Email address to validate

        Returns:
            bool: True if email format is valid
        """
        if not isinstance(email, str):
            return False

        return bool(re.match(cls.EMAIL_PATTERN, email))

    @classmethod
    def sanitize_user_input(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize user input dictionary

        Args:
            data: Dictionary of user input

        Returns:
            Dict: Sanitized data dictionary
        """
        sanitized = {}

        for key, value in data.items():
            # Validate key name
            if not cls.validate_sql_identifier(key):
                logger.warning(f"Invalid key name: {key}")
                continue

            if isinstance(value, str):
                # Sanitize string values
                try:
                    sanitized_value = cls.sanitize_sql_input(value)
                    sanitized_value = cls.sanitize_html_input(sanitized_value)
                    sanitized[key] = sanitized_value
                except ValueError as e:
                    logger.warning(f"Input validation failed for {key}: {e}")
                    # Skip dangerous inputs
                    continue
            elif isinstance(value, (int, float, bool)):
                # Numeric and boolean values are safe
                sanitized[key] = value
            elif isinstance(value, dict):
                # Recursively sanitize nested dictionaries
                sanitized[key] = cls.sanitize_user_input(value)
            elif isinstance(value, list):
                # Sanitize list items
                sanitized_list = []
                for item in value:
                    if isinstance(item, str):
                        try:
                            sanitized_item = cls.sanitize_sql_input(item)
                            sanitized_item = cls.sanitize_html_input(sanitized_item)
                            sanitized_list.append(sanitized_item)
                        except ValueError:
                            # Skip dangerous items
                            continue
                    else:
                        sanitized_list.append(item)
                sanitized[key] = sanitized_list
            else:
                # Convert other types to string and sanitize
                try:
                    str_value = str(value)
                    sanitized_value = cls.sanitize_sql_input(str_value)
                    sanitized_value = cls.sanitize_html_input(sanitized_value)
                    sanitized[key] = sanitized_value
                except ValueError:
                    # Skip dangerous inputs
                    continue

        return sanitized


def validate_input(validator_func=None):
    """
    Decorator for automatic input validation

    Args:
        validator_func: Custom validation function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validate keyword arguments
            if kwargs:
                try:
                    kwargs = InputValidator.sanitize_user_input(kwargs)
                except Exception as e:
                    logger.error(f"Input validation failed: {e}")
                    raise ValueError("Input validation failed")

            # Apply custom validator if provided
            if validator_func:
                if not validator_func(*args, **kwargs):
                    raise ValueError("Custom validation failed")

            return func(*args, **kwargs)

        return wrapper

    return decorator


# Global validator instance
input_validator = InputValidator()
