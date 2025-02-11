from sqlalchemy.orm import Session
from models.auth import auth_required
from models.permission import role_required
from services.user_service import UserService


class UserController:
    """Controler to handle users."""

    @staticmethod
    @auth_required
    @role_required("Management")
    def create_user(user_payload, session: Session, name: str,
                    email: str, password: str, role: str):
        """Create user."""
        user = UserService.create_user(session, name, email, password, role)
        print(f"User '{user.name}' created successfully.")
        return user

    @staticmethod
    @auth_required
    @role_required("Management")
    def update_user(user_payload, session: Session, user_id: int, data: dict):
        """Update an user."""
        user = UserService.update_user(session, user_id, data)
        print(f"✅ User '{user.name}' updated successfully.")
        return user

    @staticmethod
    @auth_required
    @role_required("Management")
    def delete_user(user_payload, session: Session, user_id: int):
        """Delete a user."""
        user = UserService.delete_user(session, user_id)
        print(f"User '{user.name}' deleted successfully.")
        return user

    @staticmethod
    @auth_required
    def get_user(user_payload, session: Session, user_id: int):
        """Get user using ID."""
        user = UserService.get_user_by_id(session, user_id)
        if user:
            print(f"User found: {user.name}")
        else:
            print(f"No user found with ID {user_id}")

    @staticmethod
    @auth_required
    def get_user_by_email(user_payload, session: Session, user_email: str):
        """Get user using email."""
        user = UserService.get_user_by_email(session, user_email)
        if user:
            print(f"User found: {user.name}")
        else:
            print(f"No user found with email {user_email}")

    @staticmethod
    def login_user(session: Session, email: str, password: str):
        """Allow user to connect."""
        tokens = UserService.login_user(session, email, password)
        if tokens:
            print(f"Connected! Welcome, {tokens['user'].name}.")
            return tokens
        else:
            print("Incorrect email or password.")
            return None
