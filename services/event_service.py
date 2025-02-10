from sqlalchemy.orm import Session
from repository.event_repository import EventRepository


class EventService:
    """Handles business logic for events."""

    @staticmethod
    def list_all(session: Session):
        """Get all event as dictionnaries."""
        events = EventRepository.get_all_events(session)
        return [{"id": event.id,
                 "start_date": event.start_date,
                 "location": event.location}
                for event in events]

    @staticmethod
    def get_by_id(session: Session, event_id: int):
        """Get an event with its ID."""
        event = EventRepository.get_event_by_id(session, event_id)
        if not event:
            raise ValueError("Event not found.")
        return {
            "id": event.id,
            "start_date": event.start_date,
            "end_date": event.end_date,
            "location": event.location
        }
