import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import wraps
from sqlalchemy.orm import Session

from app.repository.user_repository import UserRepository

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


class Auth:
    """Handles authentication using JWT."""

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str):
        """Authenticate a user with email and password."""
        user = UserRepository.get_user_by_email(session, email)
        if user and user.verify_password(password):
            return {
                "user": user,
                "access_token": Auth.create_access_token(user.id, user.role),
                "refresh_token": Auth.create_refresh_token(user.id)
            }
        return None

    @staticmethod
    def create_access_token(user_id: int, role: str):
        """Create a JWT access token."""
        expire = datetime.datetime.now(
            ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload_data = {
            "id": str(user_id),
            "role": role,
            "exp": expire
        }
        return jwt.encode(
            payload=payload_data,
            key=JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

    @staticmethod
    def create_refresh_token(user_id: int):
        """Create a JWT refresh token."""
        expire = datetime.datetime.now(
            ) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        payload_data = {"id": str(user_id), "exp": expire}
        return jwt.encode(
            payload=payload_data,
            key=JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

    @staticmethod
    def load_token():
        """Load tokens from .auth_token."""
        try:
            with open(".auth_token", "r") as f:
                access_token = f.readline().strip()
                refresh_token = f.readline().strip()
            return access_token, refresh_token
        except FileNotFoundError:
            return None, None

    @staticmethod
    def save_token(access_token: str, refresh_token: str):
        """Save tokens in .auth_token."""
        with open(".auth_token", "w") as f:
            f.write(access_token + "\n")
            f.write(refresh_token)
        os.chmod(".auth_token", 0o600)

    @staticmethod
    def verify_token(token: str):
        """Check JWT token and return payload if valid."""
        try:
            payload_data = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )
            return payload_data
        except jwt.ExpiredSignatureError:
            print("Erreur : Token expiré.")
            return "expired"
        except jwt.InvalidTokenError:
            print("Erreur : Token invalide.")
            return "invalid"

    @staticmethod
    def refresh_access_token(refresh_token: str):
        payload_data = Auth.verify_token(refresh_token)
        if payload_data:
            new_access_token = Auth.create_access_token(
                payload_data["id"],
                payload_data.get("role", "User")
            )
            Auth.save_token(new_access_token, refresh_token)
            return Auth.verify_token(new_access_token)
        return None

    @staticmethod
    def is_authenticated():
        """Check if user is authenticated with a valid token."""
        access_token, refresh_token = Auth.load_token()
        if not access_token:
            return None

        payload_data = Auth.verify_token(access_token)
        if payload_data == "invalid":
            return None

        if payload_data == "expired":
            payload_data = Auth.refresh_access_token(refresh_token)
            return payload_data

        return payload_data


def auth_required(func):
    """Wrapper to ckeck a user is authenticated before executing functions."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        user_payload = Auth.is_authenticated()
        if not user_payload:
            raise PermissionError(
                "Access denied: Authentication required"
            )
        return func(self, user_payload, *args, **kwargs)
    return wrapper
