import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
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
def session_test():
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
