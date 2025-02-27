from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class UserView:
    """View for user management."""

    @staticmethod
    def show_user_menu():
        """Displays the User panel menu."""
        console.print("[bold cyan]\nUser Panel[/bold cyan]")
        console.print("[green]1 - Show all users[/green]")
        console.print("[green]2 - Create a user[/green]")
        console.print("[red]3 - Return to main menu[/red]")
        return Prompt.ask("Make your choice")

    @staticmethod
    def display_users_and_get_choice(users):
        """Displays the list of users and allows selecting details or going back."""
        if not users:
            console.print("[bold red]\nNo users found.[/bold red]")
            return None

        table = Table(title="User List", show_lines=True)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Role", style="yellow")

        for user in users:
            table.add_row(
                str(user['id']),
                user['name'],
                user['email'],
                user['role']
            )

        console.print(table)
        console.print("[bold]Enter a user ID to view details or press Enter to return.[/bold]")
        user_id = Prompt.ask("User ID", default="")
        return int(user_id) if user_id.isdigit() else None

    @staticmethod
    def display_user_details_and_get_choice(user):
        """Displays a user's details and provides action options."""
        console.print("[bold cyan]\nUser Details[/bold cyan]")
        console.print(f"[magenta]ID:[/magenta] {user.id}")
        console.print(f"[magenta]Name:[/magenta] {user.name}")
        console.print(f"[magenta]Email:[/magenta] {user.email}")
        console.print(f"[magenta]Role:[/magenta] {user.role}")

        console.print("\n[bold]Actions:[/bold]")
        console.print("[green]1 - Edit user[/green]")
        console.print("[green]2 - Delete user[/green]")
        console.print("[red]3 - Return to the user list[/red]")

        return Prompt.ask("Make your choice")

    @staticmethod
    def get_user_update_data():
        """Prompts for new user data."""
        print("\nEdit User")
        name = input("New name (leave blank to keep unchanged): ").strip()
        email = input("New email (leave blank to keep unchanged): ").strip()
        role = input("New role (leave blank to keep unchanged): ").strip()

        user_data = {}

        if name:
            user_data["name"] = name
        if email:
            user_data["email"] = email
        if role:
            user_data["role"] = role

        return user_data

    @staticmethod
    def get_user_creation_data():
        """Prompts for information to create a new user."""
        print("\nCreate a New User")
        name = input("Name: ").strip().title()
        email = input("Email: ").strip().lower()
        password = input("Password: ").strip()
        role = input("Role (Support, Manager, Sales): ").strip()

        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        }
