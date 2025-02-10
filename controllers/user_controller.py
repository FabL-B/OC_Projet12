from sqlalchemy.orm import Session
from models.user import User
from repository.user_repository import UserManager
from models.auth import auth_required, Auth
from models.permission import role_required


class UserController:
    @staticmethod
    @auth_required
    @role_required("Management")
    def create_user(user_payload,
                    session: Session,
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
    @auth_required
    def get_user(user_payload, session: Session, user_id: int):
        """Get user with its ID."""
        user = UserManager.get_user_by_id(session, user_id)
        if user:
            print(f"User found : {user.name}")
        else:
            print(f"No user found with ID {user_id}")

    @staticmethod
    @auth_required
    def get_user_by_email(user_payload, session: Session, user_email: int):
        """Get user with its ID."""
        user = UserManager.get_user_by_email(session, user_email)
        if user:
            print(f"User found : {user.name}")
        else:
            print(f"No user found with ID {user_email}")

    @staticmethod
    def login_user(session: Session, email: str, password: str):
        """Allow a user to connect."""
        tokens = Auth.authenticate_user(session, email, password)
        if tokens:
            Auth.save_token(tokens["access_token"], tokens["refresh_token"])
            print(f"Connected! Welcome, {tokens['user'].name}.")
            return tokens
        else:
            print("Incorrect email or password.")
            return None
