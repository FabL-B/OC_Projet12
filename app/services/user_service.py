from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.models.user import User
from app.auth.auth import Auth


class UserService:
    """Handles business logic for users."""

    @staticmethod
    def get_by_id(session, user_id):
        """Retrieves a user by ID."""
        return UserRepository.get_user_by_id(session, user_id)

    @staticmethod
    def list_all(session: Session):
        users = UserRepository.get_all_users(session)
        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
            for user in users
        ]

    @staticmethod
    def create(session, name, email, password, role):
        """Creates a user."""
        existing_user = UserRepository.get_user_by_email(session, email)
        if existing_user:
            raise ValueError("A user with this email already exists.")

        user = User(name=name, email=email, role=role)
        user.set_password(password)

        return UserRepository.create_user(session, user)

    @staticmethod
    def update(session, user_id, data):
        """Update an existing user."""
        user = UserRepository.get_user_by_id(session, user_id)
        if not user:
            raise ValueError("User not found.")
        return UserRepository.update_user(session, user_id, data)

    @staticmethod
    def delete(session, user_id):
        """Delete a user."""
        user = UserRepository.get_user_by_id(session, user_id)
        if not user:
            raise ValueError("User not found.")

        return UserRepository.delete_user(session, user_id)

    @staticmethod
    def get_user_by_email(session, user_email):
        """Retrieves a user by email."""
        return UserRepository.get_user_by_email(session, user_email)

    @staticmethod
    def login_user(session, email, password):
        """Allows a user to log in."""
        tokens = Auth.authenticate_user(session, email, password)
        if tokens:
            Auth.save_token(tokens["access_token"], tokens["refresh_token"])
            return tokens
        return None
