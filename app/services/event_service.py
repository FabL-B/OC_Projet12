from sqlalchemy.orm import Session
from app.repository.event_repository import EventRepository
from app.models.event import Event


class EventService:
    """Handles business logic for events."""

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
            "location": event.location,
            "attendees": event.attendees,
            "notes": event.notes,
        }

    @staticmethod
    def list_all(session: Session):
        """Get all event as dictionnaries."""
        events = EventRepository.get_all_events(session)
        return [{"id": event.id,
                 "start_date": event.start_date,
                 "end_date": event.end_date,
                 "location": event.location}
                for event in events]

    @staticmethod
    def list_by_support_contact(session: Session, support_contact_id: int):
        """Returns events managed by a specific support contact."""
        events = EventRepository.get_events_by_support_contact(
            session, support_contact_id
        )
        return [{"id": event.id,
                 "start_date": event.start_date,
                 "end_date": event.end_date,
                 "location": event.location,}
                for event in events]

    @staticmethod
    def create(
        session: Session,
        contract_id: int,
        support_contact_id: int,
        start_date: str,
        end_date: str,
        location: str,
        attendees: int,
        notes: str = None
    ):
        """Create a new event."""
        event = Event(
            contract_id=contract_id,
            support_contact_id=support_contact_id,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
            notes=notes
        )
        return EventRepository.create_event(session, event)

    @staticmethod
    def update(session: Session, event_id: int, data: dict):
        """Update an existing event."""
        event = EventRepository.get_event_by_id(session, event_id)
        if not event:
            raise ValueError("Event not found.")
        return EventRepository.update_event(session, event_id, data)

    @staticmethod
    def delete(session: Session, event_id: int):
        """Delete an event."""
        event = EventRepository.get_event_by_id(session, event_id)
        if not event:
            raise ValueError("Event not found.")

        return EventRepository.delete_event(session, event_id)
