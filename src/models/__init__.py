"""
Main models module - imports all model classes and sets up the database
"""

from .ai_models import (
    AIRecommendation,
    BotConfiguration,
    BotType,
    Conversation,
    ConversationStatus,
    IntentCategory,
    KnowledgeBase,
    LearningLog,
    Message,
    MessageType,
)
from .audit_models import (
    AuditExecution,
    AuditFinding,
    AuditStatus,
    AuditType,
    ComplianceReport,
    ComplianceRule,
    ComplianceStatus,
    RiskAssessment,
    RuleSeverity,
    ViolationType,
)

# Import all models to ensure they're registered with SQLAlchemy
from .auth_models import AccessLog, Permission, User, UserRole, UserStatus
from .cct_models import (
    CCT,
    CCTClause,
    CCTComparison,
    CCTStatus,
    CCTType,
    CCTUpdateLog,
    ClauseType,
    Union,
)

# Import database configuration
from .database import Base, SessionLocal, engine, get_db, init_db
from .document_models import (
    AccessLevel,
    Document,
    DocumentAccess,
    DocumentCategory,
    DocumentShare,
    DocumentStatus,
    DocumentTemplate,
    DocumentType,
    DocumentVersion,
)
from .notification_models import (
    Event,
    EventType,
    Notification,
    NotificationPreference,
    NotificationPriority,
    NotificationRule,
    NotificationStatus,
    NotificationTemplate,
    NotificationType,
)
from .payroll_models import (
    Employee,
    PayrollCompetency,
    PayrollImport,
    PayrollItem,
    PayrollStatus,
    PayrollType,
)
from .report_models import (
    BlockType,
    GeneratedReport,
    ReportBlock,
    ReportDataSource,
    ReportTemplate,
    ReportType,
)

# Export all models for easy importing
__all__ = [
    # Database
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    # Auth models
    "User",
    "Permission",
    "AccessLog",
    "UserRole",
    "UserStatus",
    # Payroll models
    "Employee",
    "PayrollCompetency",
    "PayrollItem",
    "PayrollImport",
    "PayrollStatus",
    "PayrollType",
    # Document models
    "Document",
    "DocumentVersion",
    "DocumentAccess",
    "DocumentShare",
    "DocumentTemplate",
    "DocumentType",
    "DocumentCategory",
    "DocumentStatus",
    "AccessLevel",
    # CCT models
    "Union",
    "CCT",
    "CCTClause",
    "CCTComparison",
    "CCTUpdateLog",
    "CCTStatus",
    "CCTType",
    "ClauseType",
    # Notification models
    "Notification",
    "NotificationTemplate",
    "Event",
    "NotificationRule",
    "NotificationPreference",
    "NotificationType",
    "NotificationPriority",
    "NotificationStatus",
    "EventType",
    # Audit models
    "AuditExecution",
    "ComplianceRule",
    "AuditFinding",
    "ComplianceReport",
    "RiskAssessment",
    "AuditType",
    "AuditStatus",
    "ComplianceStatus",
    "ViolationType",
    "RuleSeverity",
    # AI models
    "KnowledgeBase",
    "Conversation",
    "Message",
    "BotConfiguration",
    "AIRecommendation",
    "LearningLog",
    "ConversationStatus",
    "MessageType",
    "BotType",
    "IntentCategory",
    # Report models
    "ReportTemplate",
    "ReportBlock",
    "GeneratedReport",
    "ReportDataSource",
    "ReportType",
    "BlockType",
]


def create_all_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
