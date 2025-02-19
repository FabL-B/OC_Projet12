class ContractView:
    """View for contract management."""

    @staticmethod
    def show_contract_menu():
        """Displays the Contract panel menu."""
        print("\nContract Panel")
        print("1 - Show all contracts")
        print("2 - Filter unsigned contracts")
        print("3 - Filter unpaid contracts")
        print("4 - Create a contract")
        print("5 - Return to main menu")
        return input("Make your choice: ").strip()

    @staticmethod
    def display_contracts_and_get_choice(contracts):
        """
        Displays the list of contracts and allows viewing
        details or going back.
        """
        if not contracts:
            print("\nNo contracts found.")
            return None

        print("\nContract List:")
        for contract in contracts:
            print(
                f"ID: {contract['id']} | Amount: {contract['amount']} | "
                f"Status: {contract['status']}"
            )

        print("\nActions:")
        print("Enter a contract ID to view details.")
        print("Press Enter to return to the previous menu.")

        contract_id = input("Contract ID: ").strip()
        return int(contract_id) if contract_id.isdigit() else None

    @staticmethod
    def display_contract_details_and_get_choice(contract):
        """Displays contract details and provides action options."""
        print("\nContract Details")
        print(f"ID: {contract.id}")
        print(f"Amount: {contract.amount}")
        print(f"Amount Due: {contract.amount_due}")
        print(f"Status: {contract.status}")

        print("\nActions:")
        print("1 - Edit contract")
        print("2 - Delete contract")
        print("3 - Return to contract list")

        return input("Make your choice: ").strip()

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
