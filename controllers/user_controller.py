from services.user_service import UserService
from models.auth import auth_required
from sqlalchemy.orm import Session
from models.permission import UserPermission


class UserController:
    """Controller for handling users."""

    def __init__(self):
        self.service = UserService
        self.permission_class = UserPermission

    @auth_required
    def list_all(self, user_payload, session: Session):
        """Retrieve all entities."""
        if not self.permission_class().has_permission(
            user_payload, "list_all"):
            raise PermissionError()
        return self.service.list_all(session)

    @auth_required
    def get(self, user_payload, session: Session, entity_id: int):
        """Retrieve a specific entity by ID."""
        if not self.permission_class().has_permission(
            user_payload, "get"):
            raise PermissionError()
        return self.service.get_by_id(session, entity_id)

    @auth_required
    def create(self, user_payload, session: Session, **kwargs):
        """Create a new entity."""
        if not self.permission_class().has_permission(
            user_payload, "create"):
            raise PermissionError()
        return self.service.create(session, **kwargs)

    @auth_required
    def update(self, user_payload, session: Session, entity_id, data):
        """Update an existing entity."""
        if not self.permission_class().has_permission(
            user_payload, "update"):
            raise PermissionError()
        return self.service.update(session, entity_id, data)

    @auth_required
    def delete(self, user_payload, session: Session, entity_id):
        """Delete an entity."""
        if not self.permission_class().has_permission(
            user_payload, "delete"):
            raise PermissionError()
        return self.service.delete(session, entity_id)
