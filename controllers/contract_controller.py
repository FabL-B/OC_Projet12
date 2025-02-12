from sqlalchemy.orm import Session
from models.auth import auth_required
from models.permission import permission_required
from services.contract_service import ContractService


class ContractController:
    """Controler to handle contracts."""
    @staticmethod
    @auth_required
    def create_contract(
        user_payload,
        session: Session,
        customer_id: int,
        amount: float,
        amount_due: float,
        status: bool
    ):
        """Create a new contract."""
        contract = ContractService.create_contract(
            session,
            customer_id,
            amount,
            amount_due,
            status
        )
        print("Contract created successfully.")
        return contract

    @staticmethod
    @auth_required
    def update_contract(
        user_payload,
        session: Session,
        contract_id: int,
        data: dict
    ):
        """Update an existing contract."""

        contract = ContractService.update_contract(
            session,
            contract_id,
            data
        )
        print("Contract updated successfully.")
        return contract

    @staticmethod
    @auth_required
    @permission_required("Management")
    def delete_contract(user_payload, session: Session, contract_id: int):
        """Delete a contract."""
        contract = ContractService.delete_contract(session, contract_id)
        print("Contract deleted successfully.")
        return contract

    @staticmethod
    @auth_required
    def list_contracts(user_payload, session: Session):
        """List all contracts."""
        contracts = ContractService.list_all_contracts(session)
        return contracts

    @staticmethod
    @auth_required
    def get_contract(user_payload, session: Session, contract_id: int):
        """Get contract witrh its ID."""
        try:
            return ContractService.get_by_id(session, contract_id)
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None
