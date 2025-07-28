"""
Notification and Events Models for AUDITORIA360
Módulo 4: Notificações e Eventos
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class NotificationType(enum.Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"
    SYSTEM = "system"

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
    priority = Column(Enum(NotificationPriority), nullable=False, default=NotificationPriority.MEDIUM)
    
    # Delivery information
    status = Column(Enum(NotificationStatus), nullable=False, default=NotificationStatus.PENDING)
    delivery_attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    
    # Scheduling
    scheduled_for = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    
    # Content details
    action_url = Column(String(500))  # URL for action button
    action_text = Column(String(100))  # Text for action button
    additional_data = Column(JSON)  # Additional metadata
    
    # Delivery tracking
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    failed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # External service tracking
    external_id = Column(String(255))  # ID from external service (Firebase, SendGrid, etc.)
    provider = Column(String(50))  # firebase, sendgrid, twilio
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.title} to {self.user.username} ({self.type.value})>"

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
    
    def __repr__(self):
        return f"<NotificationTemplate {self.name} ({self.type.value})>"

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(EventType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Event source
    source_module = Column(String(50))  # payroll, cct, document, etc.
    source_id = Column(String(100))     # ID of the source entity
    
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
    
    def __repr__(self):
        return f"<Event {self.type.value}: {self.title}>"

class NotificationRule(Base):
    __tablename__ = "notification_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Rule triggers
    event_type = Column(Enum(EventType), nullable=False)
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
    
    def __repr__(self):
        return f"<NotificationRule {self.name} for {self.event_type.value}>"

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Preference settings
    event_type = Column(Enum(EventType), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    is_enabled = Column(Boolean, default=True)
    
    # Timing preferences
    quiet_hours_start = Column(String(5))  # Format: "22:00"
    quiet_hours_end = Column(String(5))    # Format: "08:00"
    timezone = Column(String(50), default="UTC")
    
    # Frequency control
    max_per_hour = Column(Integer, default=10)
    max_per_day = Column(Integer, default=50)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<NotificationPreference {self.user.username}: {self.event_type.value} via {self.notification_type.value}>"