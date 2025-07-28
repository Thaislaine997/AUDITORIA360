"""
AI, Chatbot and Intelligent Bots Models for AUDITORIA360
Módulo 7: IA, Chatbot e Bots Inteligentes
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class ConversationStatus(enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    TRANSFERRED = "transferred"
    ARCHIVED = "archived"

class MessageType(enum.Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"
    ESCALATION = "escalation"

class BotType(enum.Enum):
    CHATBOT = "chatbot"
    DESKTOP_ANALYZER = "desktop_analyzer"
    COMPLIANCE_BOT = "compliance_bot"
    PAYROLL_ASSISTANT = "payroll_assistant"

class IntentCategory(enum.Enum):
    CCT_QUESTION = "cct_question"
    PAYROLL_CALCULATION = "payroll_calculation"
    COMPLIANCE_CHECK = "compliance_check"
    DOCUMENT_SEARCH = "document_search"
    GENERAL_HELP = "general_help"
    ESCALATION = "escalation"
    OTHER = "other"

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    
    # Source information
    source_type = Column(String(50))  # cct, legislation, faq, manual
    source_id = Column(String(100))   # ID of the source document/entity
    source_url = Column(String(500))
    
    # Content metadata
    keywords = Column(JSON)  # Array of keywords for search
    tags = Column(JSON)      # Array of tags for categorization
    language = Column(String(5), default="pt-BR")
    
    # Embeddings and AI processing
    embedding_vector = Column(JSON)  # Vector embedding for semantic search
    confidence_score = Column(Float, default=1.0)
    
    # Usage statistics
    view_count = Column(Integer, default=0)
    helpful_votes = Column(Integer, default=0)
    unhelpful_votes = Column(Integer, default=0)
    last_accessed = Column(DateTime(timezone=True))
    
    # Status and versioning
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    verified_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User", foreign_keys=[created_by_id])
    verified_by = relationship("User", foreign_keys=[verified_by_id])
    
    def __repr__(self):
        return f"<KnowledgeBase {self.title} ({self.category})>"

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String(100), nullable=False, index=True)
    
    # Conversation metadata
    title = Column(String(255))
    bot_type = Column(Enum(BotType), nullable=False)
    status = Column(Enum(ConversationStatus), nullable=False, default=ConversationStatus.ACTIVE)
    
    # Context information
    initial_intent = Column(Enum(IntentCategory))
    context_data = Column(JSON)  # Conversation context and variables
    
    # Quality metrics
    satisfaction_rating = Column(Integer)  # 1-5 rating
    was_helpful = Column(Boolean)
    feedback = Column(Text)
    resolution_achieved = Column(Boolean, default=False)
    
    # Escalation handling
    escalated_to_human = Column(Boolean, default=False)
    escalated_at = Column(DateTime(timezone=True))
    escalated_to_user_id = Column(Integer, ForeignKey("users.id"))
    escalation_reason = Column(Text)
    
    # Conversation timing
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True))
    
    # AI metrics
    ai_confidence_avg = Column(Float)
    ai_accuracy_score = Column(Float)
    human_intervention_needed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    escalated_to = relationship("User", foreign_keys=[escalated_to_user_id])
    messages = relationship("Message", back_populates="conversation")
    
    def __repr__(self):
        return f"<Conversation {self.session_id} ({self.bot_type.value})>"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Message content
    content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    
    # AI processing
    intent_detected = Column(Enum(IntentCategory))
    confidence_score = Column(Float)
    entities_extracted = Column(JSON)  # Named entities extracted from message
    
    # Response generation
    response_generated = Column(Text)
    response_source = Column(String(100))  # knowledge_base, api, escalation
    knowledge_base_ids = Column(JSON)  # IDs of KB articles used
    
    # Processing metadata
    processing_time_ms = Column(Integer)
    ai_model_used = Column(String(50))
    api_calls_made = Column(JSON)  # External API calls made
    
    # User interaction
    was_helpful = Column(Boolean)
    user_feedback = Column(Text)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.message_type.value}: {self.content[:50]}...>"

class BotConfiguration(Base):
    __tablename__ = "bot_configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    bot_type = Column(Enum(BotType), nullable=False)
    description = Column(Text)
    
    # AI Model Configuration
    ai_model = Column(String(50), default="gpt-3.5-turbo")
    system_prompt = Column(Text, nullable=False)
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=500)
    
    # Behavior settings
    greeting_message = Column(Text)
    fallback_responses = Column(JSON)  # Array of fallback responses
    escalation_triggers = Column(JSON)  # Conditions for escalation
    
    # Knowledge base configuration
    knowledge_base_categories = Column(JSON)  # Categories to search in
    semantic_search_enabled = Column(Boolean, default=True)
    confidence_threshold = Column(Float, default=0.7)
    
    # Integration settings
    external_apis = Column(JSON)  # Configuration for external API integrations
    webhooks = Column(JSON)       # Webhook configurations
    
    # Status and versioning
    is_active = Column(Boolean, default=True)
    version = Column(String(10), default="1.0")
    
    # Usage statistics
    total_conversations = Column(Integer, default=0)
    successful_resolutions = Column(Integer, default=0)
    escalation_rate = Column(Float, default=0.0)
    average_satisfaction = Column(Float, default=0.0)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User")
    
    def __repr__(self):
        return f"<BotConfiguration {self.name} ({self.bot_type.value})>"

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Recommendation content
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Context and reasoning
    context_data = Column(JSON)  # Data used to generate recommendation
    reasoning = Column(Text)     # AI explanation of the recommendation
    confidence_score = Column(Float, nullable=False)
    
    # Implementation details
    action_items = Column(JSON)  # Specific actions to take
    expected_impact = Column(Text)
    implementation_complexity = Column(String(20))  # low, medium, high
    estimated_time_hours = Column(Float)
    
    # Related entities
    related_entity_type = Column(String(50))  # payroll, employee, cct, etc.
    related_entity_id = Column(String(100))
    
    # User interaction
    is_viewed = Column(Boolean, default=False)
    is_accepted = Column(Boolean)
    is_dismissed = Column(Boolean, default=False)
    user_feedback = Column(Text)
    
    # Implementation tracking
    is_implemented = Column(Boolean, default=False)
    implemented_at = Column(DateTime(timezone=True))
    implementation_notes = Column(Text)
    actual_impact = Column(Text)
    
    # AI model information
    ai_model_used = Column(String(50))
    model_version = Column(String(20))
    training_data_version = Column(String(20))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<AIRecommendation {self.title} for {self.user.username}>"

class LearningLog(Base):
    __tablename__ = "learning_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Learning event information
    event_type = Column(String(50), nullable=False)  # user_interaction, feedback, correction
    bot_type = Column(Enum(BotType), nullable=False)
    
    # Input/Output data
    input_data = Column(JSON, nullable=False)
    expected_output = Column(JSON)
    actual_output = Column(JSON)
    feedback_provided = Column(JSON)
    
    # Learning metrics
    accuracy_before = Column(Float)
    accuracy_after = Column(Float)
    improvement_score = Column(Float)
    
    # Context
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Processing information
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    processing_notes = Column(Text)
    
    # Timestamp
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation")
    user = relationship("User")
    
    def __repr__(self):
        return f"<LearningLog {self.event_type} for {self.bot_type.value}>"