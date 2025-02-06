from sqlalchemy.orm import Session
from models.user import User
from models.user_manager import UserManager


class UserController:
    @staticmethod
    def create_user(session: Session,
                    name: str,
                    email: str,
                    password: str,
                    role: str):
        """Create a new user."""
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        UserManager.save(session, user)
        print(f"User created successfully. ID: {user.id}")

    @staticmethod
    def get_user(session: Session, user_id: int):
        """Get user with its ID."""
        user = UserManager.get_user_by_id(session, user_id)
        if user:
            print(f"User found : {user.name}")
        else:
            print(f"No user found with ID {user_id}")

    @staticmethod
    def get_user_by_email(session: Session, user_email: int):
        """Get user with its ID."""
        user = UserManager.get_by_email(session, user_email)
        if user:
            print(f"User found : {user.name}")
        else:
            print(f"No user found with ID {user_email}")

    @staticmethod
    def login_user(session: Session, email: str, password: str):
        """Allow a user to connect."""
        user = UserManager.authenticate_user(session, email, password)
        if user:
            print(f"Connected ! Welcome, {user.name} ({user.role}).")
            return user
        else:
            print("Incorrect email or password.")
            return None
