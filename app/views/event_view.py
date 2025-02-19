class EventView:
    """View for event management."""

    @staticmethod
    def show_event_menu():
        """Displays the Event panel menu."""
        print("\nEvent Panel")
        print("1 - Show all events")
        print("2 - Show my events only")
        print("3 - Create an event")
        print("4 - Return to main menu")
        return input("Make your choice: ").strip()

    @staticmethod
    def display_events_and_get_choice(events):
        """
        Displays the list of events and allows viewing details
        or going back.
        """
        if not events:
            print("\nNo events found.")
            return None

        print("\nEvent List:")
        for event in events:
            print(
                f"ID: {event['id']} | Date: {event['start_date']} | "
                f"Location: {event['location']}"
            )

        print("\nActions:")
        print("Enter an event ID to view its details.")
        print("Press Enter to return to the previous menu.")

        event_id = input("Event ID: ").strip()
        return int(event_id) if event_id.isdigit() else None

    @staticmethod
    def display_event_details_and_get_choice(event):
        """Displays event details and provides action options."""
        print("\nEvent Details")
        print(f"ID: {event.id}")
        print(f"Start Date: {event.start_date}")
        print(f"End Date: {event.end_date}")
        print(f"Location: {event.location}")
        print(f"Number of Attendees: {event.attendees}")
        print(f"Notes: {event.notes}")

        print("\nActions:")
        print("1 - Edit event")
        print("2 - Delete event")
        print("3 - Return to event list")

        return input("Make your choice: ").strip()

    @staticmethod
    def get_event_creation_data():
        """Retrieves data to create an event."""
        print("\nCreate a new event")
        contract_id = input("Associated Contract ID: ").strip()
        support_contact_id = input("Support Contact ID: ").strip()
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        location = input("Location: ").strip()
        attendees = input("Number of Attendees: ").strip()
        notes = input("Notes (optional): ").strip()

        return {
            "contract_id": (
                int(contract_id) if contract_id.isdigit() else None
            ),
            "support_contact_id": (
                int(support_contact_id) if support_contact_id.isdigit()
                else None
            ),
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "attendees": (
                int(attendees) if attendees.isdigit() else None
            ),
            "notes": notes if notes else None,
        }

    @staticmethod
    def get_event_update_data():
        """Prompts for new event data."""
        print("\nEdit Event")
        start_date = input(
            "New start date (leave blank to keep unchanged): "
        ).strip()
        end_date = input(
            "New end date (leave blank to keep unchanged): "
        ).strip()
        location = input(
            "New location (leave blank to keep unchanged): "
        ).strip()
        attendees = input(
            "New number of attendees (leave blank to keep unchanged): "
        ).strip()
        notes = input(
            "New notes (leave blank to keep unchanged): "
        ).strip()

        event_data = {}

        if start_date:
            event_data["start_date"] = start_date
        if end_date:
            event_data["end_date"] = end_date
        if location:
            event_data["location"] = location
        if attendees:
            event_data["attendees"] = attendees
        if notes:
            event_data["notes"] = notes

        return event_data
