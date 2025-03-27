from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class EventView:
    """View for event management."""

    @staticmethod
    def display_events_and_get_choice(events):
        """Displays the list of events and allows viewing details."""
        if not events:
            console.print("[bold red]\nNo events found.[/bold red]")
            return None

        table = Table(title="Event List", show_lines=True)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Start Date", style="green")
        table.add_column("End Date", style="green")
        table.add_column("Location", style="yellow")

        for event in events:
            table.add_row(
                str(event['id']),
                event['start_date'].strftime('%Y-%m-%d'),
                event['end_date'].strftime('%Y-%m-%d'),
                event['location']
            )

        console.print(table)
        console.print(
            "[bold]Enter an event ID to view details [/bold]"
            "[bold]or press Enter to return.[/bold]"
        )
        event_id = Prompt.ask("Event ID", default="")
        return int(event_id) if event_id.isdigit() else None

    @staticmethod
    def display_event_details_and_get_choice(event):
        """Displays event details in a table and provides action options."""
        table = Table(title="Event Details", show_lines=True)

        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Start Date", style="magenta", justify="center")
        table.add_column("End Date", style="magenta", justify="center")
        table.add_column("Location", style="yellow", justify="center")
        table.add_column("Attendees", style="green", justify="center")
        table.add_column("Notes", style="blue", justify="center")
        table.add_column("Support Contact", style="red", justify="center")
        table.add_column("Contract ID", style="cyan", justify="center")
        table.add_column("Client", style="magenta", justify="center")

        support_contact = (
            f"Name: {event.support_contact.name}"
            if event.support_contact
            else "N/A"
        )

        client_info = (
            f"Comapany name: {event.contract.customer.company_name}"
        )

        table.add_row(
            str(event.id),
            event.start_date.strftime("%Y-%m-%d"),
            event.end_date.strftime("%Y-%m-%d"),
            event.location,
            str(event.attendees),
            event.notes if event.notes else "N/A",
            support_contact,
            str(event.contract.id),
            client_info,
        )

        console.print(table)

        console.print("\n[bold]Actions:[/bold]")
        console.print("[green]1 - Edit event[/green]")
        console.print("[red]2 - Delete event[/red]")
        console.print("[yellow]3 - Return to event list[/yellow]")

        return Prompt.ask("Make your choice")

    @staticmethod
    def get_event_creation_data():
        """Retrieves data to create an event."""
        console.print("\n[bold cyan]Create a new event[/bold cyan]")
        support_contact_id = input("Support Contact ID: ").strip()
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        location = input("Location: ").strip()
        attendees = input("Number of Attendees: ").strip()
        notes = input("Notes (optional): ").strip()

        return {
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

    @staticmethod
    def display_not_found():
        print("\nEvent not found.")

    @staticmethod
    def display_invalid_choice():
        print("\nInvalid choice, please try again.")
