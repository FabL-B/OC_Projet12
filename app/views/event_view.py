from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class EventView:
    """View for event management."""

    @staticmethod
    def show_event_menu():
        """Displays the Event panel menu."""
        console.print("[bold cyan]\nEvent Panel[/bold cyan]")
        console.print("[green]1 - Show all events[/green]")
        console.print("[green]2 - Show my events only[/green]")
        console.print("[green]3 - Create an event[/green]")
        console.print("[red]4 - Return to main menu[/red]")
        return Prompt.ask("Make your choice")

    @staticmethod
    def display_events_and_get_choice(events):
        """Displays the list of events and allows viewing details."""
        if not events:
            console.print("[bold red]\nNo events found.[/bold red]")
            return None

        table = Table(title="Event List", show_lines=True)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Start Date", style="magenta")
        table.add_column("End Date", style="yellow")
        table.add_column("Location", style="green")

        for event in events:
            table.add_row(
                str(event['id']),
                event['start_date'],
                event['end_date'],
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
        """Displays event details and provides action options."""
        console.print("[bold cyan]\nEvent Details[/bold cyan]")
        console.print(f"[magenta]ID:[/magenta] {event.id}")
        console.print(f"[magenta]Start Date:[/magenta] {event.start_date}")
        console.print(f"[magenta]End Date:[/magenta] {event.end_date}")
        console.print(f"[magenta]Location:[/magenta] {event.location}")
        console.print(f"[magenta]Attendees:[/magenta] {event.attendees}")
        console.print(f"[magenta]Notes:[/magenta] {event.notes}")

        console.print("\n[bold]Actions:[/bold]")
        console.print("[green]1 - Edit event[/green]")
        console.print("[green]2 - Delete event[/green]")
        console.print("[red]3 - Return to event list[/red]")

        return Prompt.ask("Make your choice")

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
