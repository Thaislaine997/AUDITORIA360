"""
Main models module - imports all model classes and sets up the database
"""

# Import database configuration
from .database import Base, engine, SessionLocal, get_db, init_db

# Import all models to ensure they're registered with SQLAlchemy
from .auth_models import User, Permission, AccessLog, UserRole, UserStatus
from .payroll_models import (
    Employee, PayrollCompetency, PayrollItem, PayrollImport,
    PayrollStatus, PayrollType
)
from .document_models import (
    Document, DocumentVersion, DocumentAccess, DocumentShare, DocumentTemplate,
    DocumentType, DocumentCategory, DocumentStatus, AccessLevel
)
from .cct_models import (
    Union, CCT, CCTClause, CCTComparison, CCTUpdateLog,
    CCTStatus, CCTType, ClauseType
)
from .notification_models import (
    Notification, NotificationTemplate, Event, NotificationRule, NotificationPreference,
    NotificationType, NotificationPriority, NotificationStatus, EventType
)
from .audit_models import (
    AuditExecution, ComplianceRule, AuditFinding, ComplianceReport, RiskAssessment,
    AuditType, AuditStatus, ComplianceStatus, ViolationType, RuleSeverity
)
from .ai_models import (
    KnowledgeBase, Conversation, Message, BotConfiguration, AIRecommendation, LearningLog,
    ConversationStatus, MessageType, BotType, IntentCategory
)

# Export all models for easy importing
__all__ = [
    # Database
    "Base", "engine", "SessionLocal", "get_db", "init_db",
    
    # Auth models
    "User", "Permission", "AccessLog", "UserRole", "UserStatus",
    
    # Payroll models
    "Employee", "PayrollCompetency", "PayrollItem", "PayrollImport",
    "PayrollStatus", "PayrollType",
    
    # Document models
    "Document", "DocumentVersion", "DocumentAccess", "DocumentShare", "DocumentTemplate",
    "DocumentType", "DocumentCategory", "DocumentStatus", "AccessLevel",
    
    # CCT models
    "Union", "CCT", "CCTClause", "CCTComparison", "CCTUpdateLog",
    "CCTStatus", "CCTType", "ClauseType",
    
    # Notification models
    "Notification", "NotificationTemplate", "Event", "NotificationRule", "NotificationPreference",
    "NotificationType", "NotificationPriority", "NotificationStatus", "EventType",
    
    # Audit models
    "AuditExecution", "ComplianceRule", "AuditFinding", "ComplianceReport", "RiskAssessment",
    "AuditType", "AuditStatus", "ComplianceStatus", "ViolationType", "RuleSeverity",
    
    # AI models
    "KnowledgeBase", "Conversation", "Message", "BotConfiguration", "AIRecommendation", "LearningLog",
    "ConversationStatus", "MessageType", "BotType", "IntentCategory",
]

def create_all_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)