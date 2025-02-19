from app.models.user import User
from app.repository.user_repository import UserRepository


def test_create_user(mock_session):
    """Test the creation and saving of a user in the database."""
    user = User(name="Bob", email="bob@example.com", role="Sales")
    user.set_password("securepassword")

    UserRepository.create_user(mock_session, user)

    assert mock_session.add.called
    assert mock_session.commit.called


def test_get_user_by_id(mock_session):
    """Test retrieving a user by ID."""
    user = User(id=1, name="Bob", email="bob@example.com", role="Sales")
    mock_session.get.return_value = user

    result = UserRepository.get_user_by_id(mock_session, 1)

    assert result == user


def test_delete_user(mock_session):
    """Test deleting a user from the database."""
    user = User(id=1, name="Bob", email="bob@example.com", role="Sales")
    mock_session.get.return_value = user

    result = UserRepository.delete_user(mock_session, 1)

    assert mock_session.delete.called
    assert mock_session.commit.called
    assert result == user
