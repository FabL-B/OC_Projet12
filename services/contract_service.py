from sqlalchemy.orm import Session
from repository.contract_repository import ContractRepository


class ContractService:
    """Handles business logic for contracts."""

    @staticmethod
    def list_all_contracts(session: Session):
        """Get all clients as dictionnaries."""
        contracts = ContractRepository.get_all_contracts(session)
        return [{"id": contract.id,
                 "amount": contract.amount,
                 "signed": contract.status}
                for contract in contracts]

    @staticmethod
    def get_by_id(session: Session, contract_id: int):
        """Get a contrat with its ID."""
        contract = ContractRepository.get_contract_by_id(session, contract_id)
        if not contract:
            raise ValueError("Contract not found.")
        return {
            "id": contract.id,
            "amount": contract.amount,
            "contract_status": contract.status
        }
