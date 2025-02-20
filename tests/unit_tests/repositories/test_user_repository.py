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

    created_user = UserRepository.create_user(mock_session, user)

    mock_session.add.assert_called_once_with(user)
    mock_session.commit.assert_called_once()
    assert created_user == user


def test_get_user_by_id():
    mock_session = MagicMock()
    mock_session.get.return_value = User(
        id=2,
        name="User2",
        email="user2@example.com",
        role="Sales"
    )

    retrieved_user = UserRepository.get_user_by_id(mock_session, 2)

    mock_session.get.assert_called_once_with(User, 2)
    assert retrieved_user.email == "user2@example.com"
