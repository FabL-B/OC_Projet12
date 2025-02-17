from services.event_service import EventService
from models.auth import auth_required
from sqlalchemy.orm import Session
from models.permission import EventPermission, permission_required


class EventController:
    """Controller for handling events."""

    def __init__(self):
        self.service = EventService
        self.permission_class = EventPermission

    @auth_required
    @permission_required("list_all")
    def list_all(self, user_payload, session: Session):
        """Retrieve all events."""
        return self.service.list_all(session)

    @auth_required
    @permission_required("get")
    def get(self, user_payload, session: Session, entity_id: int):
        """Retrieve a specific event by ID."""
        return self.service.get_by_id(session, entity_id)

    @auth_required
    @permission_required("create")
    def create(self, user_payload, session: Session, **kwargs):
        """Create a new event."""
        return self.service.create(session, **kwargs)

    @auth_required
    @permission_required("update")
    def update(self, user_payload, session: Session, entity_id, data):
        """Update an existing event."""
        return self.service.update(session, entity_id, data)

    @auth_required
    @permission_required("delete")
    def delete(self, user_payload, session: Session, entity_id):
        """Delete an event."""
        return self.service.delete(session, entity_id)
