from services.contract_service import ContractService
from models.auth import auth_required
from models.permission import ContractPermission, permission_required
from views.contract_view import ContractView


class ContractController:
    """Controller for managing contracts."""

    def __init__(self):
        self.service = ContractService
        self.permission_class = ContractPermission

    @auth_required
    @permission_required("list_all")
    def list_all_contracts(self, user_payload, session):
        """Displays all contracts and offers an action."""
        while True:
            contracts = self.service.list_all(session)
            contract_id = ContractView.display_contracts_and_get_choice(
                contracts
            )

            if contract_id is None:
                break

            self.show_contract_details(session, contract_id)

    @auth_required
    @permission_required("list_unsigned")
    def list_unsigned_contracts(self, user_payload, session):
        """Displays unsigned contracts."""
        while True:
            contracts = self.service.list_unsigned(session)
            contract_id = ContractView.display_contracts_and_get_choice(
                contracts
            )

            if contract_id is None:
                break

            self.show_contract_details(session, contract_id)

    @auth_required
    @permission_required("list_unpaid")
    def list_unpaid_contracts(self, user_payload, session):
        """Displays contracts where `amount_due` is different from `amount`."""
        while True:
            contracts = self.service.list_unpaid(session)
            contract_id = ContractView.display_contracts_and_get_choice(
                contracts
            )

            if contract_id is None:
                break

            self.show_contract_details(session, contract_id)

    @auth_required
    @permission_required("get")
    def show_contract_details(self, user_payload, session, contract_id):
        """Displays contract details and ask for update/delete options."""
        contract = self.service.get_by_id(session, contract_id)
        if not contract:
            print("\nContract not found.")
            return

        while True:
            choice = ContractView.display_contract_details_and_get_choice(
                contract
            )

            if choice == "1":
                self.update_contract(session, contract_id)
            elif choice == "2":
                self.delete_contract(session, contract_id)
                break
            elif choice == "3":
                break
            else:
                print("\nInvalid choice, please try again.")

    @auth_required
    @permission_required("create")
    def create_contract(self, user_payload, session):
        """Creates a new contract."""
        contract_data = ContractView.get_contract_creation_data()
        self.service.create(session, **contract_data)
        print("Contract successfully created.")

    @auth_required
    @permission_required("update")
    def update_contract(self, user_payload, session, contract_id):
        """Updates an existing contract."""
        updated_data = ContractView.get_contract_update_data()
        if updated_data:
            self.service.update(session, contract_id, updated_data)
            print(f"Contract {contract_id} successfully updated.")

    @auth_required
    @permission_required("delete")
    def delete_contract(self, user_payload, session, contract_id):
        """Deletes a contract after confirmation."""
        confirm = input(
            f"Confirm deletion of contract {contract_id}? (y/n): "
        ).strip().lower()

        if confirm == "y":
            self.service.delete(session, contract_id)
            print(f"Contract {contract_id} successfully deleted.")
