import pytest
from app.models.user import User


@pytest.fixture
def user():
    """Fixture to crerate a fake user."""
    return User(name="Alice", email="alice@example.com", role="Sales")


def test_set_password(user):
    """Test password hashing."""
    password = "securepassword123"
    user.set_password(password)

    assert user.password_hash is not None
    assert isinstance(user.password_hash, str)
    print(password)
    print(user.password_hash, str)
    assert user.password_hash != password


def test_verify_password(user):
    """Test password verification."""
    password = "securepassword123"
    user.set_password(password)

    assert user.verify_password(password) is True
    assert user.verify_password("wrongpassword") is False
