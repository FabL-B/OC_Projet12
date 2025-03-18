import pytest
from unittest.mock import MagicMock, patch
from app.services.user_service import UserService
from app.models.user import User




def test_create_user(mock_session, mock_user_repository):
    """Vérifie qu'on ne peut pas créer un utilisateur avec un email déjà existant."""
    mock_user_repository.get_user_by_email.return_value = User(id=1, email="test@example.com")

    with pytest.raises(ValueError, match="A user with this email already exists."):
        UserService.create(mock_session, "John", "test@example.com", "securepassword", "Sales")



def test_get_user_by_id(mock_session):
    """Vérifie que get_by_id récupère bien l'utilisateur correct."""
    mock_user = User(id=1, name="Test User", email="test@example.com", role="Sales")

    with patch("app.repository.user_repository.UserRepository.get_user_by_id", return_value=mock_user):
        result = UserService.get_by_id(mock_session, 1)

    assert result == mock_user