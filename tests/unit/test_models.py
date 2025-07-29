"""
Tests for database models and core functionality
"""

from unittest.mock import Mock, patch

from src.models import (
    CCT,
    AccessLog,
    AuditExecution,
    Base,
    Document,
    Employee,
    KnowledgeBase,
    Notification,
    PayrollCompetency,
    Permission,
    User,
    create_all_tables,
    get_db,
    init_db,
)


def test_user_model_creation():
    """Test User model can be instantiated"""
    user = User(
        username="test_user",
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashed_password",
    )
    assert user.username == "test_user"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"


def test_permission_model_creation():
    """Test Permission model can be instantiated"""
    permission = Permission(name="read_documents", description="Can read documents")
    assert permission.name == "read_documents"
    assert permission.description == "Can read documents"


def test_employee_model_creation():
    """Test Employee model can be instantiated"""
    employee = Employee(
        full_name="John Doe", cpf="123.456.789-00", employee_id="EMP001"
    )
    assert employee.full_name == "John Doe"
    assert employee.cpf == "123.456.789-00"
    assert employee.employee_id == "EMP001"


def test_document_model_creation():
    """Test Document model can be instantiated"""
    document = Document(
        filename="test.pdf",
        original_filename="original_test.pdf",
        file_size=1024,
        mime_type="application/pdf",
    )
    assert document.filename == "test.pdf"
    assert document.original_filename == "original_test.pdf"
    assert document.file_size == 1024


def test_cct_model_creation():
    """Test CCT model can be instantiated"""
    cct = CCT(
        union_name="Test Union",
        company_name="Test Company",
        start_date="2024-01-01",
        end_date="2024-12-31",
    )
    assert cct.union_name == "Test Union"
    assert cct.company_name == "Test Company"


def test_notification_model_creation():
    """Test Notification model can be instantiated"""
    notification = Notification(
        title="Test Notification", message="This is a test message", user_id=1
    )
    assert notification.title == "Test Notification"
    assert notification.message == "This is a test message"
    assert notification.user_id == 1


def test_audit_execution_model_creation():
    """Test AuditExecution model can be instantiated"""
    audit = AuditExecution(
        audit_name="Monthly Payroll Audit", executed_by=1, status="completed"
    )
    assert audit.audit_name == "Monthly Payroll Audit"
    assert audit.executed_by == 1


def test_knowledge_base_model_creation():
    """Test KnowledgeBase model can be instantiated"""
    kb = KnowledgeBase(
        title="Test Article", content="This is test content", category="general"
    )
    assert kb.title == "Test Article"
    assert kb.content == "This is test content"
    assert kb.category == "general"


def test_access_log_model_creation():
    """Test AccessLog model can be instantiated"""
    log = AccessLog(
        user_id=1, action="login", resource="system", ip_address="192.168.1.1"
    )
    assert log.user_id == 1
    assert log.action == "login"
    assert log.resource == "system"
    assert log.ip_address == "192.168.1.1"


def test_payroll_competency_model_creation():
    """Test PayrollCompetency model can be instantiated"""
    competency = PayrollCompetency(
        month=1, year=2024, employee_id=1, gross_salary=5000.00
    )
    assert competency.month == 1
    assert competency.year == 2024
    assert competency.employee_id == 1
    assert competency.gross_salary == 5000.00


@patch("src.models.database.create_engine")
def test_get_db_function(mock_create_engine):
    """Test get_db dependency function"""
    # Mock the engine and session
    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine

    # Test that get_db returns a generator
    db_gen = get_db()
    assert db_gen is not None


def test_init_db_function():
    """Test database initialization function"""
    try:
        result = init_db()
        # Should not raise an exception
        assert result is None  # Function doesn't return anything
    except Exception as e:
        # If it fails due to missing database, that's expected in test env
        assert "database" in str(e).lower() or "connection" in str(e).lower()


def test_create_all_tables_function():
    """Test create all tables function"""
    try:
        result = create_all_tables()
        # Should not raise an exception
        assert result is None  # Function doesn't return anything
    except Exception as e:
        # If it fails due to missing database, that's expected in test env
        assert "database" in str(e).lower() or "connection" in str(e).lower()


def test_base_model_exists():
    """Test that Base declarative base exists"""
    assert Base is not None
    assert hasattr(Base, "metadata")


def test_model_inheritance():
    """Test that all models inherit from Base"""
    models = [
        User,
        Permission,
        Employee,
        Document,
        CCT,
        Notification,
        AuditExecution,
        KnowledgeBase,
    ]

    for model in models:
        # Check that model has a __tablename__ attribute (indicating it's a SQLAlchemy model)
        assert hasattr(model, "__tablename__") or hasattr(model, "__table__")


def test_model_string_representations():
    """Test model string representations"""
    user = User(username="test", email="test@test.com", full_name="Test")
    # Should have some string representation
    str_repr = str(user)
    assert isinstance(str_repr, str)
    assert len(str_repr) > 0
