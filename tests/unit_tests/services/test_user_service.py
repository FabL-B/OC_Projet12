from unittest.mock import MagicMock, patch
from app.services.user_service import UserService
from app.models.user import User


def test_get_user_by_id():
    """Test retrieving a user by their ID."""
    mock_session = MagicMock()
    mock_user = User(id=1, name="Test User", email="test@example.com")

    with patch(
        "app.repository.user_repository.UserRepository.get_user_by_id",
        return_value=mock_user
    ):
        user = UserService.get_by_id(mock_session, 1)

    assert user.id == 1
    assert user.email == "test@example.com"


def test_create_user():
    """Test creating a new user."""
    mock_session = MagicMock()
    mock_user = User(
        id=2,
        name="User2",
        email="user2@example.com",
        role="Sales"
    )

    with patch(
        "app.repository.user_repository.UserRepository.get_user_by_email",
        return_value=None
    ):
        with patch(
            "app.repository.user_repository.UserRepository.create_user",
            return_value=mock_user
        ):
            created_user = UserService.create(
                mock_session,
                "User2",
                "user2@example.com",
                "password123",
                "Sales"
            )

    assert created_user.email == "user2@example.com"


def test_update_user():
    """Test updating an existing user's details."""
    mock_session = MagicMock()
    mock_user = User(id=3, name="User3", email="user3@example.com")
    updated_user = User(id=3, name="User3", email="updated3@example.com")

    with patch(
        "app.repository.user_repository.UserRepository.get_user_by_id",
        return_value=mock_user
    ):
        with patch(
            "app.repository.user_repository.UserRepository.update_user",
            return_value=updated_user
        ):
            result = UserService.update(
                mock_session,
                3,
                {"email": "updated3@example.com"}
            )

    assert result.email == "updated3@example.com"


def test_delete_user():
    """Test deleting a user."""
    mock_session = MagicMock()

    with patch(
        "app.repository.user_repository.UserRepository.delete_user",
        return_value=True
    ):
        result = UserService.delete(mock_session, 4)

    assert result is True
