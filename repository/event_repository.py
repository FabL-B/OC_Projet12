from sqlalchemy.orm import Session
from models.event import Event


class EventRepository:
    """Handles database operations related to the Event entity."""

    @staticmethod
    def get_all_events(session: Session):
        """Get all events."""
        return session.query(Event).all()

    @staticmethod
    def get_event_by_id(session: Session, event_id: int):
        """Get an event with its ID."""
        return session.get(Event, event_id)
