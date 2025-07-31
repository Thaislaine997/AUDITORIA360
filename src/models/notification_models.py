"""
Notification and Events Models for AUDITORIA360
Módulo 4: Notificações e Eventos
"""

import enum

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class NotificationType(enum.Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"
    SYSTEM = "system"
    WHATSAPP = "whatsapp"
    SLACK = "slack"


class NotificationPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationStatus(enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"
    DISMISSED = "dismissed"


class NotificationCategory(enum.Enum):
    SYSTEM = "system"
    CLIENT_ACTIVITY = "client_activity"
    CONFIGURATION = "configuration"
    COMPLIANCE = "compliance"
    ACHIEVEMENT = "achievement"
    CHURN_ALERT = "churn_alert"
    ANOMALY = "anomaly"


class DigestFrequency(enum.Enum):
    INSTANT = "instant"
    HOURLY = "hourly" 
    DAILY = "daily"
    WEEKLY = "weekly"
    NEVER = "never"


class EventType(enum.Enum):
    PAYROLL_CALCULATED = "payroll_calculated"
    PAYROLL_APPROVED = "payroll_approved"
    DOCUMENT_UPLOADED = "document_uploaded"
    CCT_UPDATED = "cct_updated"
    CCT_EXPIRING = "cct_expiring"
    COMPLIANCE_VIOLATION = "compliance_violation"
    AUDIT_COMPLETED = "audit_completed"
    USER_LOGIN = "user_login"
    DATA_EXPORT = "data_export"
    SYSTEM_ERROR = "system_error"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Notification content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    category = Column(Enum(NotificationCategory), nullable=False, default=NotificationCategory.SYSTEM)
    priority = Column(
        Enum(NotificationPriority), nullable=False, default=NotificationPriority.MEDIUM
    )

    # Delivery information
    status = Column(
        Enum(NotificationStatus), nullable=False, default=NotificationStatus.PENDING
    )
    delivery_attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)

    # Grouping for digest notifications
    digest_group = Column(String(100))  # Group similar notifications
    can_be_digested = Column(Boolean, default=True)

    # Scheduling
    scheduled_for = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))

    # Content details
    action_url = Column(String(500))  # URL for action button
    action_text = Column(String(100))  # Text for action button
    additional_data = Column(JSON)  # Additional metadata
    
    # Rich content support
    icon = Column(String(50))  # Icon identifier
    image_url = Column(String(500))  # Optional image
    sound = Column(String(100))  # Sound identifier for push notifications

    # Delivery tracking
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    dismissed_at = Column(DateTime(timezone=True))
    failed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)

    # External service tracking
    external_id = Column(
        String(255)
    )  # ID from external service (Firebase, SendGrid, etc.)
    provider = Column(String(50))  # firebase, sendgrid, twilio

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")

    # Use default __repr__ from BaseModel


class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    # Template content
    title_template = Column(String(255), nullable=False)
    message_template = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    priority = Column(Enum(NotificationPriority), nullable=False)

    # Template variables
    variables = Column(JSON)  # List of variables used in template

    # Email specific templates
    email_subject_template = Column(String(255))
    email_html_template = Column(Text)

    # SMS specific
    sms_template = Column(String(160))  # SMS character limit

    # Configuration
    is_active = Column(Boolean, default=True)
    auto_send = Column(Boolean, default=False)

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    created_by = relationship("User")

    # Use default __repr__ from BaseModel


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(EventType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)

    # Event source
    source_module = Column(String(50))  # payroll, cct, document, etc.
    source_id = Column(String(100))  # ID of the source entity

    # Event data
    event_data = Column(JSON)  # Structured event data
    severity = Column(String(20), default="info")  # info, warning, error, critical

    # User and context
    triggered_by_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(45))
    user_agent = Column(Text)

    # Processing
    is_processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    processing_result = Column(JSON)

    # Audit fields
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    triggered_by = relationship("User")
    rules = relationship("NotificationRule", back_populates="event")

    # Use default __repr__ from BaseModel


class NotificationRule(Base):
    __tablename__ = "notification_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Rule triggers
    event_type = Column(Enum(EventType), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)  # Fixed: Add missing foreign key
    conditions = Column(JSON)  # Conditions for triggering notification

    # Notification configuration
    template_id = Column(Integer, ForeignKey("notification_templates.id"))
    notification_type = Column(Enum(NotificationType), nullable=False)
    priority = Column(Enum(NotificationPriority), nullable=False)

    # Target configuration
    target_roles = Column(JSON)  # Array of roles to notify
    target_users = Column(JSON)  # Array of specific user IDs
    include_event_user = Column(Boolean, default=False)

    # Timing and frequency
    delay_minutes = Column(Integer, default=0)
    max_frequency_hours = Column(Integer)  # Prevent spam

    # Status
    is_active = Column(Boolean, default=True)

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    template = relationship("NotificationTemplate")
    event = relationship("Event", back_populates="rules")
    created_by = relationship("User")

    # Use default __repr__ from BaseModel


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Preference settings
    event_type = Column(Enum(EventType), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    is_enabled = Column(Boolean, default=True)

    # Timing preferences
    quiet_hours_start = Column(String(5))  # Format: "22:00"
    quiet_hours_end = Column(String(5))  # Format: "08:00"
    timezone = Column(String(50), default="UTC")

    # Frequency control
    max_per_hour = Column(Integer, default=10)
    max_per_day = Column(Integer, default=50)

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")

    # Use default __repr__ from BaseModel


class EnhancedNotificationPreference(Base):
    """Granular notification preferences for the Blueprint requirements"""
    __tablename__ = "enhanced_notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # General email preferences
    email_enabled = Column(Boolean, default=True)
    email_critical_failures_only = Column(Boolean, default=False)
    email_digest_frequency = Column(Enum(DigestFrequency), default=DigestFrequency.DAILY)
    
    # Specific notification categories
    notify_success_sends = Column(Boolean, default=False)  # "Don't notify about success"
    notify_failure_sends = Column(Boolean, default=True)
    notify_client_activity = Column(Boolean, default=True)
    notify_configuration_changes = Column(Boolean, default=True)
    notify_compliance_alerts = Column(Boolean, default=True)
    notify_churn_risks = Column(Boolean, default=True)
    notify_anomaly_detection = Column(Boolean, default=True)
    notify_achievements = Column(Boolean, default=True)
    notify_system_updates = Column(Boolean, default=False)
    
    # Advanced preferences
    group_similar_notifications = Column(Boolean, default=True)
    max_notifications_per_digest = Column(Integer, default=10)
    auto_dismiss_read_notifications = Column(Boolean, default=False)
    
    # Sound and visual preferences
    enable_sound_notifications = Column(Boolean, default=True)
    enable_desktop_notifications = Column(Boolean, default=True)
    preferred_sound = Column(String(50), default="default")
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")


class NotificationDigest(Base):
    """Grouped notifications for digest delivery"""
    __tablename__ = "notification_digests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Digest details
    digest_type = Column(Enum(DigestFrequency), nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    
    # Contained notifications
    notification_ids = Column(JSON)  # Array of notification IDs in this digest
    notification_count = Column(Integer, default=0)
    
    # Categories summary
    categories_summary = Column(JSON)  # Count by category
    priority_summary = Column(JSON)  # Count by priority
    
    # Delivery
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True))
    
    # Period covered
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
