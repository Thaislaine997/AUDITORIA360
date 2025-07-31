"""
Redirect module to consolidate models in src.models
This module redirects all imports to the centralized models in src.models
to avoid SQLAlchemy table conflicts while maintaining backward compatibility.
"""

# Import everything from the centralized models
from src.models import *

# Ensure backward compatibility
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