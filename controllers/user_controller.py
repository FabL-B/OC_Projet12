from services.user_service import UserService
from models.auth import auth_required
from sqlalchemy.orm import Session
from controllers.base_controller import BaseController
from models.permission import UserPermission

class UserController(BaseController):
    """Controller for handling users."""
    
    service = UserService
    permission_class = UserPermission

    @staticmethod
    @auth_required
    def get_user_by_email(user_payload, session: Session, user_email: str):
        """Get user using email."""
        return UserService.get_user_by_email(session, user_email)

    @staticmethod
    def login_user(session: Session, email: str, password: str):
        """Allow user to connect."""
        return UserService.login_user(session, email, password)
