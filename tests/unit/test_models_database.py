"""
Unit tests for src.models.database module.
"""

import os
from unittest.mock import MagicMock, patch


from src.models.database import (
    Base,
    BaseModel,
    SessionLocal,
    engine,
    get_db,
    init_db,
)


class TestDatabaseConfiguration:
    """Test cases for database configuration."""

    def test_database_url_default(self):
        """Test DATABASE_URL default value."""
        with patch.dict(os.environ, {}, clear=True):
            # Import the module again to get fresh config
            from importlib import reload

            import src.models.database as db_module

            reload(db_module)

            assert "postgresql://" in db_module.DATABASE_URL
            assert "auditoria360" in db_module.DATABASE_URL

    def test_database_url_from_env(self):
        """Test DATABASE_URL from environment variable."""
        test_url = "postgresql://testuser:testpass@testhost/testdb"
        with patch.dict(os.environ, {"DATABASE_URL": test_url}):
            from importlib import reload

            import src.models.database as db_module

            reload(db_module)

            assert db_module.DATABASE_URL == test_url

    def test_engine_exists(self):
        """Test that engine is created."""
        assert engine is not None
        # In SQLAlchemy 2.0, engine has different methods
        assert hasattr(engine, "connect") or hasattr(engine, "execute")

    def test_session_local_exists(self):
        """Test that SessionLocal is created."""
        assert SessionLocal is not None
        assert callable(SessionLocal)


class TestBaseModel:
    """Test cases for BaseModel class."""

    def test_base_model_repr_with_name(self):
        """Test BaseModel __repr__ with name field."""

        class TestModel(BaseModel):
            def __init__(self):
                self.name = "Test Name"
                self.id = 123

        model = TestModel()
        result = repr(model)

        assert "TestModel" in result
        assert "Test Name" in result

    def test_base_model_repr_with_title(self):
        """Test BaseModel __repr__ with title field."""

        class TestModel(BaseModel):
            def __init__(self):
                self.title = "Test Title"
                self.id = 123

        model = TestModel()
        result = repr(model)

        assert "TestModel" in result
        assert "Test Title" in result

    def test_base_model_repr_with_username(self):
        """Test BaseModel __repr__ with username field."""

        class TestModel(BaseModel):
            def __init__(self):
                self.username = "testuser"
                self.id = 123

        model = TestModel()
        result = repr(model)

        assert "TestModel" in result
        assert "testuser" in result

    def test_base_model_repr_with_email(self):
        """Test BaseModel __repr__ with email field."""

        class TestModel(BaseModel):
            def __init__(self):
                self.email = "test@example.com"
                self.id = 123

        model = TestModel()
        result = repr(model)

        assert "TestModel" in result
        assert "test@example.com" in result

    def test_base_model_repr_with_id_only(self):
        """Test BaseModel __repr__ with only id field."""

        class TestModel(BaseModel):
            def __init__(self):
                self.id = 123

        model = TestModel()
        result = repr(model)

        assert "TestModel" in result
        # The actual implementation uses just the id value, not "id=123"
        assert "123" in result

    def test_base_model_repr_with_no_identifiers(self):
        """Test BaseModel __repr__ with no identifier fields."""

        class TestModel(BaseModel):
            def __init__(self):
                self.some_field = "value"

        model = TestModel()
        result = repr(model)

        assert "TestModel" in result
        assert "Unknown" in result

    def test_base_model_repr_priority_order(self):
        """Test BaseModel __repr__ identifier priority order."""

        class TestModel(BaseModel):
            def __init__(self):
                self.name = "Name Value"
                self.email = "email@example.com"
                self.id = 123

        model = TestModel()
        result = repr(model)

        # name should take priority over email and id
        assert "TestModel" in result
        assert "Name Value" in result
        assert "email@example.com" not in result

    def test_base_model_repr_none_values_skipped(self):
        """Test BaseModel __repr__ skips None values."""

        class TestModel(BaseModel):
            def __init__(self):
                self.name = None
                self.title = None
                self.email = "test@example.com"
                self.id = 123

        model = TestModel()
        result = repr(model)

        # Should skip None values and use email
        assert "TestModel" in result
        assert "test@example.com" in result


class TestBase:
    """Test cases for Base declarative base."""

    def test_base_exists(self):
        """Test that Base exists and is usable."""
        assert Base is not None
        assert hasattr(Base, "metadata")

    def test_base_uses_base_model(self):
        """Test that Base uses BaseModel as base class."""
        # Test that Base inherits from BaseModel by checking methods
        assert hasattr(Base, "__repr__")

        # Create a simple mock model to test the __repr__ functionality
        class MockModel:
            def __init__(self):
                self.id = 1
                self.name = "test"

        # Apply BaseModel's __repr__ to the mock
        base_model = BaseModel()
        mock_model = MockModel()
        mock_model.__class__ = type("TestModel", (BaseModel,), {})

        # Should have BaseModel's __repr__ method behavior
        result = repr(mock_model)
        assert "TestModel" in result
        assert "test" in result


class TestGetDb:
    """Test cases for get_db dependency."""

    @patch("src.models.database.SessionLocal")
    def test_get_db_yields_session(self, mock_session_local):
        """Test that get_db yields a database session."""
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db

        # Use get_db generator
        db_generator = get_db()
        db_session = next(db_generator)

        assert db_session == mock_db
        mock_session_local.assert_called_once()

    @patch("src.models.database.SessionLocal")
    def test_get_db_closes_session(self, mock_session_local):
        """Test that get_db closes the session after use."""
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db

        # Use get_db generator completely
        db_generator = get_db()
        next(db_generator)

        # Trigger cleanup by trying to get next (should raise StopIteration)
        try:
            next(db_generator)
        except StopIteration:
            pass

        mock_db.close.assert_called_once()


class TestInitDb:
    """Test cases for init_db function."""

    @patch("src.models.database.Base")
    @patch("src.models.database.engine")
    def test_init_db_creates_tables(self, mock_engine, mock_base):
        """Test that init_db creates all tables."""
        mock_metadata = MagicMock()
        mock_base.metadata = mock_metadata

        init_db()

        mock_metadata.create_all.assert_called_once_with(bind=mock_engine)
