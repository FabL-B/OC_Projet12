from app.models.event import Event


class EventRepository:
    """Handles database operations related to the Event entity."""
    @staticmethod
    def create_event(session, event):
        """Create a new event in the database."""
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    @staticmethod
    def delete_event(session, event_id):
        """Delete an event from the database."""
        event = session.get(Event, event_id)
        session.delete(event)
        session.commit()
        return event

    @staticmethod
    def update_event(session, event_id, data):
        """Update an existing event in the database."""
        event = session.get(Event, event_id)
        if event:
            for key, value in data.items():
                setattr(event, key, value)
            session.commit()
        return event

    @staticmethod
    def get_all_events(session):
        """Retrieve all events from the database."""
        return session.query(Event).all()

    @staticmethod
    def get_events_by_support_contact(session, support_contact_id):
        """Retrieves all events managed by a specific support contact."""
        return session.query(Event).filter_by(
            support_contact_id=support_contact_id
        ).all()

    @staticmethod
    def get_event_by_id(session, event_id):
        """Get an event from database with its ID."""
        return session.get(Event, event_id)

    @staticmethod
    def get_events_without_support_contact(session):
        """Get all events that have no support contact assigned."""
        return session.query(Event).filter(
            Event.support_contact_id.is_(None)).all()
