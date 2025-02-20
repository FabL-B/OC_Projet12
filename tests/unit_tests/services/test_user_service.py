import pytest
from app.models.user import User
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository


def test_create_user_success(mock_session, mocker):
    """Test successful user creation."""
    mocker.patch.object(
        UserRepository,
        "get_user_by_email",
        return_value=None,
    )

    fake_user = User(
        id=1, name="Bob", email="bob@example.com", role="Sales"
    )
    mocker.patch.object(
        UserRepository,
        "create_user",
        return_value=fake_user,
    )

    user = UserService.create(
        mock_session,
        name="Bob",
        email="bob@example.com",
        password="securepassword",
        role="Sales",
    )

    assert user.name == "Bob"
    assert user.email == "bob@example.com"
    assert user.role == "Sales"


def test_create_user_existing_email(mock_session, mocker):
    """Test user creation failure (email already exists)."""
    existing_user = User(
        id=1, name="Bob", email="bob@example.com", role="Sales"
    )
    mocker.patch.object(
        UserRepository,
        "get_user_by_email",
        return_value=existing_user,
    )

    with pytest.raises(
        ValueError,
        match="A user with this email already exists.",
    ):
        UserService.create(
            mock_session,
            name="Bob",
            email="bob@example.com",
            password="securepassword",
            role="Sales",
        )


def test_delete_user_success(mock_session, mocker):
    """Test successful user deletion."""
    fake_user = User(
        id=1, name="Alice", email="alice@example.com", role="Sales"
    )

    mocker.patch.object(
        UserRepository,
        "get_user_by_id",
        return_value=fake_user,
    )
    mocker.patch.object(
        UserRepository,
        "delete_user",
        return_value=fake_user,
    )

    deleted_user = UserService.delete(mock_session, 1)

    assert deleted_user == fake_user
