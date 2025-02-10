from sqlalchemy.orm import Session
from models.auth import auth_required
from services.contract_service import ContractService


class ContractController:
    """Controler to handle contracts."""

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
