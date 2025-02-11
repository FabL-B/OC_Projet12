from sqlalchemy.orm import Session
from repository.contract_repository import ContractRepository
from models.contract import Contract


class ContractService:
    """Handles business logic for contracts."""
    @staticmethod
    def create_contract(
        session: Session,
        customer_id: int,
        amount: float,
        amount_due: float,
        status: bool
    ):
        """Creates a new contract."""
        contract = Contract(
            customer_id=customer_id,
            amount=amount,
            amount_due=amount_due,
            status=status
        )
        return ContractRepository.create_contract(session, contract)

    @staticmethod
    def update_contract(session: Session, contract_id: int, data: dict):
        """Update an existing contract."""
        contract = ContractRepository.get_contract_by_id(session, contract_id)
        if not contract:
            raise ValueError("Contract not found.")
        return ContractRepository.update_contract(session, contract_id, data)

    @staticmethod
    def delete_contract(session: Session, contract_id: int):
        """Delete a contract."""
        contract = ContractRepository.get_contract_by_id(session, contract_id)
        if not contract:
            raise ValueError("Contract not found.")

        return ContractRepository.delete_contract(session, contract_id)

    @staticmethod
    def list_all_contracts(session: Session):
        """Get all clients as dictionnaries."""
        contracts = ContractRepository.get_all_contracts(session)
        return [{"id": contract.id,
                 "amount": contract.amount,
                 "status": contract.status}
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
