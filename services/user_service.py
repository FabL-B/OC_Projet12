from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from models.user import User
from models.auth import Auth


class UserService:
    """Handles business logic for users."""
    @staticmethod
    def create_user(
        session: Session,
        name: str,
        email: str,
        password: str,
        role: str
    ):
        """Creates a user while applying business rules."""
        existing_user = UserRepository.get_user_by_email(session, email)
        if existing_user:
            raise ValueError("A user with this email already exists.")

        user = User(name=name, email=email, role=role)
        user.set_password(password)

        return UserRepository.create_user(session, user)

    @staticmethod
    def update_user(session: Session, user_id: int, data: dict):
        """Update an existing user."""
        user = UserRepository.get_user_by_id(session, user_id)
        if not user:
            raise ValueError("User not found.")
        return UserRepository.update_user(session, user_id, data)

    @staticmethod
    def list_users(session: Session):
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
    def get_user_by_id(session: Session, user_id: int):
        """Retrieves a user by ID."""
        return UserRepository.get_user_by_id(session, user_id)

    @staticmethod
    def get_user_by_email(session: Session, user_email: str):
        """Retrieves a user by email."""
        return UserRepository.get_user_by_email(session, user_email)

    @staticmethod
    def login_user(session: Session, email: str, password: str):
        """Allows a user to log in."""
        tokens = Auth.authenticate_user(session, email, password)
        if tokens:
            Auth.save_token(tokens["access_token"], tokens["refresh_token"])
            return tokens
        return None
