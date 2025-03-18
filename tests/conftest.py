import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from app.repository.user_repository import UserRepository

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from app.models.user import User
from config.database import Base


load_dotenv()
TEST_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/epicevent_test_db"  # noqa: E501

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture(scope="function")
def session():
    """Fixture that creates a temporary PostgreSQL database for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def mock_session(mocker):
    """Fixture to mock an SQLAlchemy session."""
    return mocker.Mock(spec=Session)

@pytest.fixture
def disable_auth_and_permissions():
    with patch("app.auth.auth.Auth.is_authenticated", return_value={"id": 1, "role": "Admin"}):
        yield

@pytest.fixture
def admin_user():
    """Fixture pour un utilisateur admin avec tous les droits."""
    return User(id=1, name="Admin User", email="admin@example.com", role="Admin", password_hash="fake_hash")


@pytest.fixture
def sales_user():
    """Fixture pour un utilisateur Sales."""
    return User(id=2, name="Sales User", email="sales@example.com", role="Sales", password_hash="fake_hash")


@pytest.fixture
def support_user():
    """Fixture pour un utilisateur Support."""
    return User(id=3, name="Support User", email="support@example.com", role="Support", password_hash="fake_hash")


@pytest.fixture
def management_user():
    """Fixture pour un utilisateur Management."""
    return User(id=4, name="Management User", email="management@example.com", role="Management", password_hash="fake_hash")


@pytest.fixture
def mock_user_repository():
    """Mock de UserRepository."""
    return MagicMock(spec=UserRepository)