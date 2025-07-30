"""
Core constants for AUDITORIA360
Centralized location for all constants used throughout the application.
"""


class ProfileNames:
    """Profile names used across the application for role-based access control"""

    SUPER_ADMIN = "Super Administrador"
    CONTABILIDADE = "Contabilidade"
    CLIENTE_FINAL = "Cliente Final"
    GESTOR_A = "Gestor A"
    GESTOR_B = "Gestor B"
    AUDITOR = "Auditor"
    USUARIO_COMUM = "Usuário Comum"


class UserTypes:
    """User types for multi-level access control"""

    SUPER_ADMIN = "super_admin"
    CONTABILIDADE = "contabilidade"
    CLIENTE_FINAL = "cliente_final"


class CompanyTypes:
    """Types of companies in the system"""

    CONTABILIDADE = "contabilidade"
    CLIENTE = "cliente"


class DefaultCompanies:
    """Default company identifiers"""

    CONTAB_A_ID = "CONTAB_A"
    CONTAB_B_ID = "CONTAB_B"
    CLIENT_X_ID = "CLIENT_X"
    CLIENT_Y_ID = "CLIENT_Y"


class DefaultUsernames:
    """Default usernames for system initialization"""

    ADMIN = "admin"
    GESTOR_A = "gestor_a"
    GESTOR_B = "gestor_b"
    CLIENT_X = "cliente_x"
    CLIENT_Y = "cliente_y"


class DatabaseTableNames:
    """Database table names"""

    USERS = "users"
    USERS_ENHANCED = "users_enhanced"
    COMPANIES = "companies"
    PERMISSIONS = "permissions"
    USER_PERMISSIONS = "user_permissions"
    ACCESS_LOGS = "access_logs"
    AUDIT_LOGS = "audit_logs"
    DOCUMENTS = "documents"
    TICKETS = "tickets"
    NOTIFICATION_TEMPLATES = "notification_templates"


class SystemDefaults:
    """System default values"""

    DEFAULT_PASSWORD_MIN_LENGTH = 8
    DEFAULT_TOKEN_EXPIRE_MINUTES = 60
    DEFAULT_DATABASE_TIMEOUT = 30
    DEFAULT_MAX_LOGIN_ATTEMPTS = 5


class NotificationTypes:
    """Types of notifications in the system"""

    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class NotificationTemplates:
    """Default notification template names"""

    WELCOME_USER = "welcome_user"
    DOCUMENT_PROCESSED = "document_processed"
    AUDIT_ALERT = "audit_alert"
    PASSWORD_RESET = "password_reset"
    LOGIN_ALERT = "login_alert"


class SecurityConstants:
    """Security-related constants"""

    BCRYPT_ROUNDS = 12
    JWT_ALGORITHM = "HS256"
    SESSION_COOKIE_NAME = "auditoria360_session"
    CSRF_TOKEN_LENGTH = 32


class EnvironmentVariables:
    """Environment variable names for configuration"""

    SECRET_KEY = "SECRET_KEY"
    DATABASE_URL = "DATABASE_URL"
    DEFAULT_ADMIN_PASSWORD = "DEFAULT_ADMIN_PASSWORD"
    DEFAULT_GESTOR_A_PASSWORD = "DEFAULT_GESTOR_A_PASSWORD"
    DEFAULT_GESTOR_B_PASSWORD = "DEFAULT_GESTOR_B_PASSWORD"
    DEFAULT_CLIENT_X_PASSWORD = "DEFAULT_CLIENT_X_PASSWORD"
    OPENAI_API_KEY = "OPENAI_API_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES = "ACCESS_TOKEN_EXPIRE_MINUTES"
    ENVIRONMENT = "ENVIRONMENT"
    DEBUG = "DEBUG"
    LOG_LEVEL = "LOG_LEVEL"


class AuditActions:
    """Actions logged in audit trails"""

    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    PASSWORD_CHANGED = "password_changed"
    DOCUMENT_UPLOADED = "document_uploaded"
    DOCUMENT_PROCESSED = "document_processed"
    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_REVOKED = "permission_revoked"


class StatusConstants:
    """General status constants"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
