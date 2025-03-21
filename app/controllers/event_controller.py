from app.logger_config import logger
from app.services.event_service import EventService
from app.auth.auth import auth_required
from app.permissions.permission import EventPermission, permission_required
from app.views.event_view import EventView


class EventController:
    """Controller for managing events."""

    def __init__(self):
        self.service = EventService
        self.permission_class = EventPermission

    @auth_required
    @permission_required("list")
    def list_all_events(self, user_payload, session):
        """Displays all events and offers modification/deletion options."""
        while True:
            events = self.service.list_all(session)
            event_id = EventView.display_events_and_get_choice(events)

            if event_id is None:
                break

            self.show_event_details(session, event_id)

    @auth_required
    @permission_required("list")
    def list_my_events(self, user_payload, session):
        """Displays events linked to the logged-in user."""
        while True:
            events = self.service.list_by_support_contact(
                session, user_payload["id"]
            )
            event_id = EventView.display_events_and_get_choice(events)

            if event_id is None:
                break

            self.show_event_details(session, event_id)

    @auth_required
    @permission_required("get")
    def show_event_details(self, user_payload, session, event_id):
        """Displays event details and offers modification/deletion options."""
        event = self.service.get_by_id(session, event_id)
        if not event:
            EventView.display_not_found()
            return

        while True:
            choice = EventView.display_event_details_and_get_choice(event)

            if choice == "1":
                self.update_event(session, obj=event)
            elif choice == "2":
                self.delete_event(session, obj=event)
                break
            elif choice == "3":
                break
            else:
                EventView.display_invalid_choice()

    @auth_required
    @permission_required("create")
    def create_event(self, user_payload, session):
        """Creates a new event."""
        try:
            event_data = EventView.get_event_creation_data()
            self.service.create(session, **event_data)
            logger.info(f"Created event: {event_data.get('location')}")
        except Exception as e:
            logger.error(e)
            raise

    @auth_required
    @permission_required("update", requires_object=True)
    def update_event(self, user_payload, session, **kwargs):
        """Updates an existing event."""
        try:
            event = kwargs.get("obj")
            updated_data = EventView.get_event_update_data()
            if updated_data:
                self.service.update(session, event.id, updated_data)
                logger.info(f"Updated event {event.id}")
        except Exception as e:
            logger.error(e)
            raise

    @auth_required
    @permission_required("delete", requires_object=True)
    def delete_event(self, user_payload, session, **kwargs):
        """Deletes an event after confirmation."""
        try:
            event = kwargs.get("obj")
            confirm = input(
                f"Confirm deletion of event {event.id}? (y/n): "
            ).strip().lower()
            if confirm == "y":
                self.service.delete(session, event.id)
                logger.info(f"Event {event.id} successfully deleted.")
        except Exception as e:
            logger.error(e)
            raise

    @auth_required
    @permission_required("list")
    def list_events_without_support_contact(self, user_payload, session):
        """Displays all events that have no support contact assigned."""
        events = self.service.list_events_without_support_contact(session)
        EventView.display_events_and_get_choice(events)
