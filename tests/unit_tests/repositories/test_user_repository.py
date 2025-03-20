from unittest.mock import MagicMock
from app.models import User
from app.repository.user_repository import UserRepository


def test_create_user():
    mock_session = MagicMock()
    user = User(
        id=1,
        name="Test User",
        email="test@example.com",
        role="Sales"
    )
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    created_user = UserRepository.create_user(mock_session, user)

    mock_session.add.assert_called_once_with(user)
    mock_session.commit.assert_called_once()
    assert created_user == user


def test_get_user_by_id():
    mock_session = MagicMock()
    mock_session.get.return_value = User(
        id=1,
        name="Test User",
        email="test@example.com",
        role="Sales"
    )

    retrieved_user = UserRepository.get_user_by_id(mock_session, 1)

    mock_session.get.assert_called_once_with(User, 1)
    assert retrieved_user.email == "test@example.com"


def test_update_user():
    mock_session = MagicMock()
    user = User(
        id=1,
        name="Test User",
        email="test@example.com",
        role="Sales"
    )
    mock_session.get.return_value = user

    updated_data = {"name": "Updated User", "role": "Admin"}
    updated_user = UserRepository.update_user(mock_session, 1, updated_data)

    mock_session.get.assert_called_once_with(User, 1)
    assert updated_user.name == "Updated User"
    assert updated_user.role == "Admin"


def test_delete_user():
    mock_session = MagicMock()
    user = User(
        id=1,
        name="Test User",
        email="test@example.com",
        role="Sales"
    )
    mock_session.get.return_value = user

    deleted_user = UserRepository.delete_user(mock_session, 1)

    mock_session.get.assert_called_once_with(User, 1)
    mock_session.delete.assert_called_once_with(user)
    assert deleted_user == user
