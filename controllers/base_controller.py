from sqlalchemy.orm import Session
from models.auth import auth_required

class BaseController:
    """Base Controller to manage CRUD operations."""

    service = None
    permission_class = None

    @staticmethod
    @auth_required
    def list_all(user_payload, session: Session):
        """Retrieve all entities."""
        return BaseController.service.list_all(session)

    @staticmethod
    @auth_required
    def get(user_payload, session: Session, entity_id: int):
        """Retrieve a specific entity by ID."""
        return BaseController.service.get_by_id(session, entity_id)

    @staticmethod
    @auth_required
    def create(user_payload, session: Session, **kwargs):
        """Create a new entity."""
        return BaseController.service.create(session, **kwargs)

    @staticmethod
    @auth_required
    def update(user_payload, session: Session, entity_id: int, data: dict):
        """Update an existing entity."""
        return BaseController.service.update(session, entity_id, data)

    @staticmethod
    @auth_required
    def delete(user_payload, session: Session, entity_id: int):
        """Delete an entity."""
        return BaseController.service.delete(session, entity_id)
