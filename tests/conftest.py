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
def admin_user():
    """Fixture pour simuler un utilisateur Admin connecté."""
    return {"id": 1, "role": "Admin"}


@pytest.fixture
def sales_user():
    """Fixture pour simuler un utilisateur Sales connecté."""
    return {"id": 2, "role": "Sales"}


@pytest.fixture
def management_user():
    """Fixture pour simuler un utilisateur Management connecté."""
    return {"id": 3, "role": "Management"}


@pytest.fixture
def support_user():
    """Fixture pour simuler un utilisateur Support connecté."""
    return {"id": 4, "role": "Support"}


@pytest.fixture(autouse=True)
def disable_auth():
    """Mock global pour désactiver l'authentification et les permissions dans les tests d'intégration"""
    with patch("app.auth.auth.auth_required", lambda x: x), \
         patch("app.permissions.permission.permission_required", lambda *args, **kwargs: lambda x: x):
        yield
