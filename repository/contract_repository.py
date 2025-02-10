from sqlalchemy.orm import Session
from models.contract import Contract


class ContractRepository:
    """Handles database operations related to the Contract entity."""

    @staticmethod
    def get_all_contracts(session: Session):
        """Get all contracts."""
        return session.query(Contract).all()

    @staticmethod
    def get_contract_by_id(session: Session, contract_id: int):
        """Get a contract with its ID."""
        return session.get(Contract, contract_id)
