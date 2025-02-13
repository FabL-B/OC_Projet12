from sqlalchemy.orm import Session
from models.auth import auth_required

# Modèle ne fonctionne pas pour le moment,
# problème de gestion des arguments passés


class BaseController:
    """Base Controller to manage CRUD operations."""

    def __init__(self, service, permission_class):
        self.service = service
        self.permission_class = permission_class
        self.user_payload = None
        self.session = None

    @auth_required
    def list_all(self, user_payload, session: Session):
        """Retrieve all entities."""
        self.user_payload = user_payload
        self.session = session
        return self.service.list_all(session)

    @auth_required
    def get(self, user_payload, session: Session, entity_id: int):
        """Retrieve a specific entity by ID."""
        self.user_payload = user_payload
        self.session = session
        return self.service.get_by_id(session, entity_id)

    @auth_required
    def create(self, session: Session, **kwargs):
        """Create a new entity."""
        return self.service.create(session, **kwargs)

    @auth_required
    def update(self, user_payload, session: Session, entity_id, data):
        """Update an existing entity."""
        self.user_payload = user_payload
        self.session = session
        return self.service.update(session, entity_id, data)

    @auth_required
    def delete(self, user_payload, session: Session, entity_id):
        """Delete an entity."""
        self.user_payload = user_payload
        self.session = session
        return self.service.delete(session, entity_id)
