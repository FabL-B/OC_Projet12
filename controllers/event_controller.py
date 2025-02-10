from sqlalchemy.orm import Session
from models.auth import auth_required
from services.event_service import EventService


class EventController:
    """Controler to handle events."""

    @staticmethod
    @auth_required
    def list_events(user_payload, session: Session):
        """List all events."""
        events = EventService.list_all_events(session)
        return events

    @staticmethod
    @auth_required
    def get_event(user_payload, session: Session, event_id: int):
        """Get event with its ID."""
        try:
            return EventService.get_by_id(session, event_id)
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None
