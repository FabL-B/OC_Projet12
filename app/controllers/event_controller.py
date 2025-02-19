from services.event_service import EventService
from app.auth.auth import auth_required
from app.permissions.permission import EventPermission, permission_required
from views.event_view import EventView


class EventController:
    """Controller for managing events."""

    def __init__(self):
        self.service = EventService
        self.permission_class = EventPermission

    @auth_required
    @permission_required("list_all")
    def list_all_events(self, user_payload, session):
        """Displays all events and offers modification/deletion options."""
        while True:
            events = self.service.list_all(session)
            event_id = EventView.display_events_and_get_choice(events)

            if event_id is None:
                break

            self.show_event_details(session, event_id)

    @auth_required
    @permission_required("list_my_events")
    def list_my_events(self, user_payload, session):
        """Displays events linked to the logged-in user."""
        while True:
            events = self.service.list_by_support_contact(
                session, user_payload["sub"]
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
            print("\nEvent not found.")
            return

        while True:
            choice = EventView.display_event_details_and_get_choice(event)

            if choice == "1":
                self.update_event(session, event_id)
            elif choice == "2":
                self.delete_event(session, event_id)
                break
            elif choice == "3":
                break
            else:
                print("\nInvalid choice, please try again.")

    @auth_required
    @permission_required("create")
    def create_event(self, user_payload, session):
        """Creates a new event."""
        event_data = EventView.get_event_creation_data()
        self.service.create(session, **event_data)
        print("Event successfully created.")

    @auth_required
    @permission_required("update")
    def update_event(self, user_payload, session, event_id):
        """Updates an existing event."""
        updated_data = EventView.get_event_update_data()
        if updated_data:
            self.service.update(session, event_id, updated_data)
            print(f"Event {event_id} successfully updated.")

    @auth_required
    @permission_required("delete")
    def delete_event(self, user_payload, session, event_id):
        """Deletes an event after confirmation."""
        confirm = input(
            f"Confirm deletion of event {event_id}? (y/n): "
        ).strip().lower()

        if confirm == "y":
            self.service.delete(session, event_id)
            print(f"Event {event_id} successfully deleted.")
