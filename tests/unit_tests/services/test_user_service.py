import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.models.user import User
from app.auth.auth import Auth
from app.services.user_service import UserService  # Assuming your class is in user_service.py

class TestUserService(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock(spec=Session)  # Mock the database session
        self.user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",  # In real tests, avoid storing plain passwords
            "role": "user"
        }

    def test_get_by_id(self):
        mock_user = MagicMock(spec=User)
        UserRepository.get_user_by_id = MagicMock(return_value=mock_user)
        user = UserService.get_by_id(self.session_mock, 1)
        self.assertEqual(user, mock_user)
        UserRepository.get_user_by_id.assert_called_once_with(self.session_mock, 1)

    def test_list_all(self):
        mock_users = [
            User(id=1, name="User 1", email="user1@example.com", role="user"),
            User(id=2, name="User 2", email="user2@example.com", role="admin"),
        ]
        UserRepository.get_all_users = MagicMock(return_value=mock_users)
        users = UserService.list_all(self.session_mock)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]["id"], 1)
        UserRepository.get_all_users.assert_called_once_with(self.session_mock)

    @patch("app.services.user_service.UserRepository.get_user_by_email")  # Patch inside the class
    @patch("app.services.user_service.UserRepository.create_user")
    def test_create(self, mock_create_user, mock_get_user_by_email):
        mock_get_user_by_email.return_value = None  # No existing user
        mock_user = MagicMock(spec=User)
        mock_create_user.return_value = mock_user

        user = UserService.create(self.session_mock, self.user_data["name"], self.user_data["email"], self.user_data["password"], self.user_data["role"])

        self.assertEqual(user, mock_user)
        mock_get_user_by_email.assert_called_once_with(self.session_mock, self.user_data["email"])
        mock_create_user.assert_called_once()  # Check if create_user was called

    @patch("app.services.user_service.UserRepository.get_user_by_email")
    def test_create_existing_user(self, mock_get_user_by_email):
        mock_get_user_by_email.return_value = MagicMock(spec=User)  # Simulate existing user
        with self.assertRaises(ValueError) as context:
            UserService.create(self.session_mock, self.user_data["name"], self.user_data["email"], self.user_data["password"], self.user_data["role"])

        self.assertEqual(str(context.exception), "A user with this email already exists.")


    @patch("app.services.user_service.UserRepository.get_user_by_id")
    @patch("app.services.user_service.UserRepository.update_user")
    def test_update(self, mock_update_user, mock_get_user_by_id):
        mock_user = MagicMock(spec=User)
        mock_get_user_by_id.return_value = mock_user
        updated_data = {"name": "Updated Name"}
        updated_user = UserService.update(self.session_mock, 1, updated_data)
        self.assertEqual(updated_user, mock_update_user.return_value) # or mock_user if update returns the user itself
        mock_get_user_by_id.assert_called_once_with(self.session_mock, 1)
        mock_update_user.assert_called_once_with(self.session_mock, 1, updated_data)

    @patch("app.services.user_service.UserRepository.get_user_by_id")
    def test_update_user_not_found(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            UserService.update(self.session_mock, 1, {"name": "Updated Name"})
        self.assertEqual(str(context.exception), "User not found.")

    @patch("app.services.user_service.UserRepository.get_user_by_id")
    @patch("app.services.user_service.UserRepository.delete_user")
    def test_delete(self, mock_delete_user, mock_get_user_by_id):
        mock_user = MagicMock(spec=User)
        mock_get_user_by_id.return_value = mock_user
        deleted = UserService.delete(self.session_mock, 1)
        self.assertEqual(deleted, mock_delete_user.return_value) # or True if delete returns a boolean
        mock_get_user_by_id.assert_called_once_with(self.session_mock, 1)
        mock_delete_user.assert_called_once_with(self.session_mock, 1)

    @patch("app.services.user_service.UserRepository.get_user_by_id")
    def test_delete_user_not_found(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            UserService.delete(self.session_mock, 1)
        self.assertEqual(str(context.exception), "User not found.")

    def test_get_user_by_email(self):
        mock_user = MagicMock(spec=User)
        UserRepository.get_user_by_email = MagicMock(return_value=mock_user)
        user = UserService.get_user_by_email(self.session_mock, "test@example.com")
        self.assertEqual(user, mock_user)
        UserRepository.get_user_by_email.assert_called_once_with(self.session_mock, "test@example.com")

    @patch("app.services.user_service.Auth.authenticate_user")
    @patch("app.services.user_service.Auth.save_token")
    def test_login_user(self, mock_save_token, mock_authenticate_user):
        mock_tokens = {"access_token": "access", "refresh_token": "refresh"}
        mock_authenticate_user.return_value = mock_tokens
        tokens = UserService.login_user(self.session_mock, "test@example.com", "password")
        self.assertEqual(tokens, mock_tokens)
        mock_authenticate_user.assert_called_once_with(self.session_mock, "test@example.com", "password")
        mock_save_token.assert_called_once_with("access", "refresh")

    @patch("app.services.user_service.Auth.authenticate_user")
    def test_login_user_invalid_credentials(self, mock_authenticate_user):
        mock_authenticate_user.return_value = None
        tokens = UserService.login_user(self.session_mock, "test@example.com", "wrong_password")
        self.assertIsNone(tokens)
        mock_authenticate_user.assert_called_once_with(self.session_mock, "test@example.com", "wrong_password")

if __name__ == '__main__':
    unittest.main()