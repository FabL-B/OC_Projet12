import pytest
from unittest.mock import MagicMock

from unittest.mock import patch
from app.controllers.user_controller import UserController
from app.repository.user_repository import UserRepository





def test_list_all_users(user_controller, mock_session):
    """Vérifie que list_all_users appelle bien UserService.list_all()."""
    with patch("app.services.user_service.UserService.list_all") as mock_list_all:
        user_controller.list_all_users({}, mock_session)
        mock_list_all.assert_called_once_with(mock_session)


def test_create_user(user_controller, mock_session):
    """Vérifie que create_user appelle UserService.create avec les bons paramètres."""
    user_data = {"name": "John", "email": "john@example.com", "password": "1234", "role": "Sales"}

    with patch("app.views.user_view.UserView.get_user_creation_data", return_value=user_data), \
         patch("app.services.user_service.UserService.create") as mock_create:

        user_controller.create_user({}, mock_session)
        mock_create.assert_called_once_with(mock_session, **user_data)