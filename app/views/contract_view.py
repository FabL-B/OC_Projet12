from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class ContractView:
    """View for contract management."""

    @staticmethod
    def show_contract_menu():
        """Displays the Contract panel menu."""
        console.print("[bold cyan]\nContract Panel[/bold cyan]")
        console.print("[green]1 - Show all contracts[/green]")
        console.print("[green]2 - Filter unsigned contracts[/green]")
        console.print("[green]3 - Filter unpaid contracts[/green]")
        console.print("[green]4 - Create a contract[/green]")
        console.print("[red]5 - Return to main menu[/red]")
        return Prompt.ask("Make your choice")

    @staticmethod
    def display_contracts_and_get_choice(contracts):
        """Displays the list of contracts and allows viewing details or going back."""
        if not contracts:
            console.print("[bold red]\nNo contracts found.[/bold red]")
            return None

        table = Table(title="Contract List", show_lines=True)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Amount", style="magenta")
        table.add_column("Amount Due", style="yellow")
        table.add_column("Status", style="green")

        for contract in contracts:
            table.add_row(
                str(contract['id']),
                str(contract['amount']),
                str(contract['amount_due']),
                contract['status']
            )

        console.print(table)
        console.print("[bold]Enter a contract ID to view details or press Enter to return.[/bold]")
        contract_id = Prompt.ask("Contract ID", default="")
        return int(contract_id) if contract_id.isdigit() else None

    @staticmethod
    def display_contract_details_and_get_choice(contract):
        """Displays contract details and provides action options."""
        console.print("[bold cyan]\nContract Details[/bold cyan]")
        console.print(f"[magenta]ID:[/magenta] {contract.id}")
        console.print(f"[magenta]Amount:[/magenta] {contract.amount}")
        console.print(f"[magenta]Amount Due:[/magenta] {contract.amount_due}")
        console.print(f"[magenta]Status:[/magenta] {contract.status}")

        console.print("\n[bold]Actions:[/bold]")
        console.print("[green]1 - Edit contract[/green]")
        console.print("[green]2 - Delete contract[/green]")
        console.print("[red]3 - Return to contract list[/red]")

        return Prompt.ask("Make your choice")

    @staticmethod
    def get_contract_creation_data():
        """Retrieves data to create a contract."""
        print("\nCreate a new contract")
        customer_id = input("Customer ID: ").strip()
        amount = input("Amount: ").strip()
        amount_due = input("Amount Due: ").strip()
        status = input("Status (signed/unsigned): ").strip().lower()

        return {
            "customer_id": (
                int(customer_id) if customer_id.isdigit() else None
            ),
            "amount": (
                float(amount) if amount.replace(".", "", 1).isdigit()
                else None
            ),
            "amount_due": (
                float(amount_due) if amount_due.replace(".", "", 1).isdigit()
                else None
            ),
            "status": (
                status if status in ["signed", "unsigned"]
                else "unsigned"),
        }

    @staticmethod
    def get_contract_update_data():
        """Prompts for new contract data."""
        print("\nEdit Contract")
        amount = input("New amount (leave blank to keep unchanged): ").strip()
        amount_due = input(
            "New amount due (leave blank to keep unchanged): "
        ).strip()
        status = input(
            "New status (signed/unsigned) (leave blank to keep unchanged): "
        ).strip().lower()

        contract_data = {}

        if amount:
            contract_data["name"] = amount
        if amount_due:
            contract_data["amount_due"] = amount_due
        if status:
            contract_data["status"] = status

        return contract_data
