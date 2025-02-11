from sqlalchemy.orm import Session
from models.auth import auth_required
from models.permission import role_required
from services.event_service import EventService


class EventController:
    """Controler to handle events."""
    @staticmethod
    @auth_required
    @role_required("Management")
    def create_event(
        user_payload,
        session: Session,
        contract_id: int,
        support_contact_id: int,
        start_date: str,
        end_date: str,
        location: str,
        attendees: int,
        notes: str = None
    ):
        """Create event."""
        event = EventService.create_event(
            session,
            contract_id,
            support_contact_id,
            start_date,
            end_date,
            location,
            attendees,
            notes
        )
        print(f"Event created successfully.")
        return event

    @staticmethod
    @auth_required
    @role_required("Management")
    def update_event(
        user_payload,
        session: Session,
        event_id: int,
        data: dict
    ):
        """Update an event."""
        event = EventService.update_event(session, event_id, data)
        print(f"Event '{event.id}' updated successfully.")
        return event

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
