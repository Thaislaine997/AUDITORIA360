"""
User and Authentication Models for AUDITORIA360
Implements granular permissions system with roles:
- Administrador, RH, Contador, Colaborador, Sindicato
"""

import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class UserRole(enum.Enum):
    ADMINISTRADOR = "administrador"
    GESTOR = "gestor"  # Manager role for the blueprint
    ANALISTA = "analista"  # Analyst role for the blueprint
    RH = "rh"
    CONTADOR = "contador"
    COLABORADOR = "colaborador"
    SINDICATO = "sindicato"
    LIDER_EQUIPE = "lider_equipe"  # Team leader role
    ESTAGIARIO = "estagiario"  # Intern role


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class OnboardingStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class UserProfile(enum.Enum):
    GESTOR = "gestor"
    ANALISTA = "analista"
    CONTADOR = "contador"
    RH = "rh"
    SINDICATO = "sindicato"
    COLABORADOR = "colaborador"


# Association table for many-to-many relationship between users and permissions
user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

# Association table for user achievements
user_achievements = Table(
    "user_achievements",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("achievement_id", Integer, ForeignKey("achievements.id"), primary_key=True),
    Column("earned_at", DateTime(timezone=True), server_default=func.now()),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.COLABORADOR)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)

    # Profile information
    phone = Column(String(20))
    department = Column(String(100))
    position = Column(String(100))
    employee_id = Column(String(50))
    user_profile = Column(
        Enum(UserProfile), nullable=False, default=UserProfile.COLABORADOR
    )

    # Gamification fields
    xp_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    total_missions_completed = Column(Integer, default=0)

    # Onboarding tracking
    onboarding_status = Column(
        Enum(OnboardingStatus), default=OnboardingStatus.NOT_STARTED
    )
    onboarding_completed_at = Column(DateTime(timezone=True))
    current_mission_id = Column(Integer, ForeignKey("onboarding_missions.id"))

    # Dashboard preferences
    dashboard_template = Column(String(100))  # Template by business segment
    preferred_segment = Column(String(100))  # "Startups", "Varejo", "Serviços de Saúde"

    # Accessibility and productivity preferences
    keyboard_navigation_enabled = Column(Boolean, default=True)
    predictive_loading_enabled = Column(Boolean, default=True)

    # Custom role (when role is CUSTOM)
    custom_role_id = Column(Integer, ForeignKey("custom_roles.id"))

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    is_email_verified = Column(Boolean, default=False)

    # LGPD Compliance
    consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime(timezone=True))
    data_retention_date = Column(DateTime(timezone=True))
    explicit_consent_for_communications = Column(Boolean, default=False)
    consent_proof_id = Column(String(255))  # Reference to consent proof record

    # Relationships
    permissions = relationship(
        "Permission", secondary=user_permissions, back_populates="users"
    )
    access_logs = relationship("AccessLog", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    achievements = relationship(
        "Achievement", secondary=user_achievements, back_populates="users"
    )
    xp_history = relationship("XPHistory", back_populates="user")
    skill_progress = relationship("UserSkillProgress", back_populates="user")
    custom_role = relationship(
        "CustomRole", back_populates="users", foreign_keys=[custom_role_id]
    )
    current_mission = relationship("OnboardingMission")

    # Use default __repr__ from BaseModel


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    resource = Column(String(100), nullable=False)  # folha, cct, documentos, etc.
    action = Column(String(50), nullable=False)  # create, read, update, delete, admin

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    users = relationship(
        "User", secondary=user_permissions, back_populates="permissions"
    )

    # Use default __repr__ from BaseModel


class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    success = Column(Boolean, default=True)
    error_message = Column(Text)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="access_logs")

    # Use default __repr__ from BaseModel


class CustomRole(Base):
    """Custom roles builder for enterprise-level permissions"""

    __tablename__ = "custom_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)

    # JSON field for custom permissions configuration
    permissions_config = Column(Text)  # JSON string with custom permissions

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    users = relationship(
        "User", back_populates="custom_role", foreign_keys="User.custom_role_id"
    )
    created_by = relationship("User", foreign_keys=[created_by_user_id])


class Achievement(Base):
    """Achievement system for gamification"""

    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(50))  # Icon identifier
    badge_class = Column(String(50))  # CSS class for styling
    xp_reward = Column(Integer, default=0)

    # Achievement criteria
    criteria_type = Column(String(50))  # "count", "streak", "milestone", etc.
    criteria_target = Column(Integer)
    criteria_resource = Column(String(100))  # What to count/track

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    users = relationship(
        "User", secondary=user_achievements, back_populates="achievements"
    )


class XPHistory(Base):
    """Track XP earning history"""

    __tablename__ = "xp_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    xp_earned = Column(Integer, nullable=False)
    reason = Column(String(255))  # "mission_completed", "achievement_unlocked", etc.
    related_resource = Column(String(100))  # Reference to what earned the XP
    related_resource_id = Column(String(100))

    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="xp_history")


class Skill(Base):
    """Skills in the skill tree system"""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    category = Column(String(50))  # "WhatsApp", "Automation", "Configuration", etc.

    # Unlock requirements
    required_xp = Column(Integer, default=0)
    required_actions = Column(Integer, default=0)
    action_type = Column(String(100))  # What action unlocks this skill

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_progress = relationship("UserSkillProgress", back_populates="skill")


class UserSkillProgress(Base):
    """Track user progress in skills"""

    __tablename__ = "user_skill_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    current_progress = Column(Integer, default=0)
    is_unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="skill_progress")
    skill = relationship("Skill", back_populates="user_progress")


class OnboardingMission(Base):
    """Onboarding missions for the gamified journey"""

    __tablename__ = "onboarding_missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    instructions = Column(Text)

    # Mission configuration
    order_sequence = Column(Integer, nullable=False)
    profile_target = Column(String(50))  # "gestor", "analista", "all"
    xp_reward = Column(Integer, default=100)
    badge_reward = Column(String(100))  # Badge name to award

    # Mission completion criteria
    completion_criteria = Column(Text)  # JSON with criteria
    is_optional = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)


class NotificationPreference(Base):
    """Granular notification preferences for users"""

    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Email preferences
    email_enabled = Column(Boolean, default=True)
    email_critical_only = Column(Boolean, default=False)
    email_digest_frequency = Column(
        String(50), default="daily"
    )  # "instant", "daily", "weekly", "never"

    # In-app preferences
    inapp_enabled = Column(Boolean, default=True)
    show_success_notifications = Column(Boolean, default=False)
    show_failure_notifications = Column(Boolean, default=True)

    # Specific notification types
    notify_client_issues = Column(Boolean, default=True)
    notify_config_changes = Column(Boolean, default=True)
    notify_system_updates = Column(Boolean, default=False)
    notify_achievements = Column(Boolean, default=True)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")
