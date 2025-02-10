import pytest
from models.user import User
from services.user_service import UserService
from repository.user_repository import UserRepository


def test_create_user_success(mock_session, mocker):
    """Test valid user cration."""
    mocker.patch.object(UserRepository, "get_user_by_email", return_value=None)

    fake_user = User(id=1, name="Bob", email="bob@example.com", role="Sales")
    mocker.patch.object(UserRepository, "save", return_value=fake_user)

    user = UserService.create_user(
        mock_session,
        "Bob",
        "bob@example.com",
        "securepassword",
        "Sales"
    )

    assert user.name == "Bob"
    assert user.email == "bob@example.com"
    assert user.role == "Sales"


def test_create_user_existing_email(mock_session, mocker):
    """Test user creation fail (existing email)."""
    existing_user = User(
        id=1,
        name="Bob",
        email="bob@example.com",
        role="Sales"
    )
    mocker.patch.object(
        UserRepository,
        "get_user_by_email",
        return_value=existing_user
    )

    with pytest.raises(ValueError,
                       match="User with this email already exists."):
        UserService.create_user(
            mock_session,
            "Bob",
            "bob@example.com",
            "securepassword",
            "Sales"
        )
