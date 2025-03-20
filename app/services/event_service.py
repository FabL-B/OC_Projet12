from app.repository.event_repository import EventRepository
from app.models.event import Event
from app.utils.transaction import transactional_session


class EventService:
    """Handles business logic for events."""

    @staticmethod
    def get_by_id(session, event_id):
        """Get an event with its ID."""
        event = EventRepository.get_event_by_id(session, event_id)
        if not event:
            raise ValueError("Event not found.")
        return event

    @staticmethod
    def list_all(session):
        """Get all event as dictionnaries."""
        events = EventRepository.get_all_events(session)
        return [{"id": event.id,
                 "start_date": event.start_date,
                 "end_date": event.end_date,
                 "location": event.location}
                for event in events]

    @staticmethod
    def list_by_support_contact(session, support_contact_id):
        """Returns events managed by a specific support contact."""
        events = EventRepository.get_events_by_support_contact(
            session, support_contact_id
        )
        return [{"id": event.id,
                 "start_date": event.start_date,
                 "end_date": event.end_date,
                 "location": event.location}
                for event in events]

    @staticmethod
    def create(session, contract_id, support_contact_id,
               start_date, end_date, location, attendees, notes):
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
    def update(session, event_id, data):
        """Update an existing event."""
        with transactional_session(session) as s:
            event = EventRepository.get_event_by_id(s, event_id)
            if not event:
                raise ValueError("Event not found.")
            return EventRepository.update_event(s, event_id, data)

    @staticmethod
    def delete(session, event_id):
        """Delete an event."""
        with transactional_session(session) as s:
            event = EventRepository.get_event_by_id(s, event_id)
            if not event:
                raise ValueError("Event not found.")
            return EventRepository.delete_event(s, event_id)

    @staticmethod
    def list_events_without_support_contact(session):
        """Returns all events without an assigned support contact."""
        return EventRepository.get_events_without_support_contact(session)
