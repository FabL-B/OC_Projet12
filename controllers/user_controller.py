from services.user_service import UserService
from models.auth import auth_required
from sqlalchemy.orm import Session
from models.permission import UserPermission, permission_required
from models.auth import Auth


class UserController:
    """Controller for handling users."""

    def __init__(self):
        self.service = UserService
        self.permission_class = UserPermission

    @auth_required
    @permission_required("list_all")
    def list_all(self, user_payload, session: Session):
        """Retrieve all entities."""
        return self.service.list_all(session)

    @auth_required
    @permission_required("get")
    def get(self, user_payload, session: Session, entity_id: int):
        """Retrieve a specific entity by ID."""
        return self.service.get_by_id(session, entity_id)

    @auth_required
    @permission_required("create")
    def create(self, user_payload, session: Session, **kwargs):
        """Create a new entity."""
        print(f"🔍 DEBUG user_payload: {user_payload}")
        return self.service.create(session, **kwargs)

    @auth_required
    @permission_required("update")
    def update(self, user_payload, session: Session, entity_id, data):
        """Update an existing entity."""
        return self.service.update(session, entity_id, data)

    @auth_required
    @permission_required("delete")
    def delete(self, user_payload, session: Session, entity_id):
        """Delete an entity."""
        return self.service.delete(session, entity_id)

    def login_user(self, session: Session, email: str, password: str):
        """Allow a user to connect."""
        tokens = Auth.authenticate_user(session, email, password)
        if tokens:
            Auth.save_token(tokens["access_token"], tokens["refresh_token"])
            print(f"Connected! Welcome, {tokens['user'].name}.")
            return tokens
        else:
            print("Incorrect email or password.")
            return None
