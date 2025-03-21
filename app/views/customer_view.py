from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class CustomerView:
    """View for customer management."""

    @staticmethod
    def display_customers_and_get_choice(customers):
        """Displays the list of customers and allows viewing details"""
        if not customers:
            console.print("[bold red]\nNo customers found.[/bold red]")
            return None

        table = Table(title="Customer List", show_lines=True)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Company Name", style="yellow")
        table.add_column("Email", style="green")
        table.add_column("Phone", style="blue")

        for customer in customers:
            table.add_row(
                str(customer['id']),
                customer['name'],
                customer['company_name'],
                customer['email'],
                customer['phone']
            )

        console.print(table)
        console.print(
            "[bold]Enter a customer ID to view details [/bold]"
            "[bold]or press Enter to return.[/bold]"
        )
        customer_id = Prompt.ask("Customer ID", default="")
        return int(customer_id) if customer_id.isdigit() else None

    @staticmethod
    def display_customer_details_and_get_choice(customer):
        """Displays customer details and provides action options."""
        console.print("[bold cyan]\nCustomer Details[/bold cyan]")
        console.print(f"[magenta]ID:[/magenta] {customer.id}")
        console.print(f"[magenta]Name:[/magenta] {customer.name}")
        console.print(
            f"[magenta]Company name:[/magenta] {customer.company_name}"
        )
        console.print(f"[magenta]Email:[/magenta] {customer.email}")
        console.print(f"[magenta]Phone:[/magenta] {customer.phone}")
        console.print(
            "[magenta]Created at:[/magenta] "
            f"[green]{customer.created_at.strftime('%Y-%m-%d %H:%M')}[/green]"
        )
        console.print(
            "[magenta]Updated at:[/magenta] "
            f"[green]{customer.updated_at.strftime('%Y-%m-%d %H:%M')}[/green]"
        )

        console.print("\n[bold]Actions:[/bold]")
        console.print("[green]1 - Edit customer[/green]")
        console.print("[green]2 - Delete customer[/green]")
        console.print("[red]3 - Return to the customer list[/red]")

        return Prompt.ask("Make your choice")

    @staticmethod
    def get_customer_creation_data():
        """Retrieves and sanitizes customer data."""
        print("\nCreate a new customer")
        name = input("Name: ").strip().title()
        company_name = input("Company name: ").strip().title()
        email = input("Email: ").strip().lower()
        phone = input("Phone: ").strip()

        return {
            "name": name,
            "company_name": company_name,
            "email": email,
            "phone": phone,
        }

    @staticmethod
    def get_customer_update_data():
        """Prompts for updated customer data."""
        print("\nEdit Customer")
        name = input(
            "Updated name (leave blank to keep unchanged): "
        ).strip().title()
        company_name = input(
            "Updated company name (leave blank to keep unchanged): "
        ).strip().title()
        email = input(
            "Updated email (leave blank to keep unchanged): "
        ).strip().lower()
        phone = input(
            "Updated phone (leave blank to keep unchanged): "
        ).strip()

        customer_data = {}

        if name:
            customer_data["name"] = name
        if company_name:
            customer_data["company_name"] = company_name
        if email:
            customer_data["email"] = email
        if phone:
            customer_data["phone"] = phone

        return customer_data

    @staticmethod
    def display_not_found():
        print("\nCustomer not found.")

    @staticmethod
    def display_invalid_choice():
        print("\nInvalid choice, please try again.")
