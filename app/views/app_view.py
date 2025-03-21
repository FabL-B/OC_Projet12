from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class AppView:
    """View for the main user interface (menu and authentication)."""

    @staticmethod
    def get_login_credentials():
        """Prompts for login credentials."""
        console.print("[bold cyan]Enter your login credentials[/bold cyan]")
        email = Prompt.ask("[green]Email[/green]")
        password = Prompt.ask("[green]Password[/green]", password=True)
        return email, password

    @staticmethod
    def show_main_menu(menu_actions):
        """Dynamically displays the main menu and gets the user's choice."""
        console.print("[bold cyan]\nMain Menu[/bold cyan]")
        table = Table(show_lines=True)
        table.add_column("Option", justify="center", style="cyan")
        table.add_column("Description", style="bold cyan")

        for key, (description, _) in menu_actions.items():
            table.add_row(str(key), description)

        console.print(table)
        return Prompt.ask("Make your choice")

    @staticmethod
    def show_user_menu():
        """Displays the User panel menu and gets the user's choice."""
        console.print("[bold cyan]\nUser Panel[/bold cyan]")
        console.print("[green]1 - Show all users[/green]")
        console.print("[green]2 - Create a user[/green]")
        console.print("[yellow]3 - Return to main menu[/yellow]")
        return Prompt.ask("Make your choice")

    @staticmethod
    def show_customer_menu():
        """Displays the Customer panel menu and gets the user's choice."""
        console.print("[bold cyan]\nCustomer Panel[/bold cyan]")
        console.print("[green]1 - Show all customers[/green]")
        console.print("[green]2 - Show my customers only[/green]")
        console.print("[green]3 - Show customers without sales[/green]")
        console.print("[green]4 - Create a customer[/green]")
        console.print("[yellow]5 - Return to main menu[/yellow]")
        return Prompt.ask("Make your choice")

    @staticmethod
    def show_contract_menu():
        """Displays the Contract panel menu."""
        console.print("[bold cyan]\nContract Panel[/bold cyan]")
        console.print("[green]1 - Show all contracts[/green]")
        console.print("[green]2 - Filter unsigned contracts[/green]")
        console.print("[green]3 - Filter unpaid contracts[/green]")
        console.print("[green]4 - Create a contract[/green]")
        console.print("[yellow]5 - Return to main menu[/yellow]")
        return Prompt.ask("Make your choice")

    @staticmethod
    def show_event_menu():
        """Displays the Event panel menu."""
        console.print("[bold cyan]\nEvent Panel[/bold cyan]")
        console.print("[green]1 - Show all events[/green]")
        console.print("[green]2 - Show my events only[/green]")
        console.print("[green]3 - Show events without support[/green]")
        console.print("[green]4 - Create an event[/green]")
        console.print("[yellow]5 - Return to main menu[/yellow]")
        return Prompt.ask("Make your choice")

    @staticmethod
    def display_logout_message():
        print("\nLogging out...")

    @staticmethod
    def display_invalid_choice():
        print("\nInvalid choice, please try again.")
