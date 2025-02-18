from sqlalchemy.orm import Session
from models.event import Event


class EventRepository:
    """Handles database operations related to the Event entity."""
    @staticmethod
    def create_event(session: Session, event: Event):
        """Create a new event in database."""
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    @staticmethod
    def delete_event(session: Session, event_id: int):
        """Delete an event from database."""
        event = session.get(Event, event_id)
        session.delete(event)
        session.commit()
        return event

    def update_event(session: Session, event_id: int, data: dict):
        """Update an existing event in database."""
        event = session.get(Event, event_id)
        if event:
            for key, value in data.items():
                setattr(event, key, value)
            session.commit()
        return event

    @staticmethod
    def get_all_events(session: Session):
        """Get all from database events."""
        return session.query(Event).all()

    @staticmethod
    def get_events_by_support_contact(session, support_contact_id):
        """Retrieves all events managed by a specific support contact."""
        return session.query(Event).filter_by(
            support_contact_id=support_contact_id
        ).all()

    @staticmethod
    def get_event_by_id(session: Session, event_id: int):
        """Get an event from database with its ID."""
        return session.get(Event, event_id)
