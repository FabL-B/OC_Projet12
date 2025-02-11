from sqlalchemy.orm import Session
from models.contract import Contract


class ContractRepository:
    """Handles database operations related to the Contract entity."""
    @staticmethod
    def create_contract(session: Session, contract: Contract):
        """Create a new contract in database."""
        session.add(contract)
        session.commit()
        session.refresh(contract)
        return contract

    @staticmethod
    def update_contract(session: Session, contract_id: int, data: dict):
        """Update an existing contract in database."""
        contract = session.get(Contract, contract_id)
        if contract:
            for key, value in data.items():
                setattr(contract, key, value)
            session.commit()
        return contract

    @staticmethod
    def get_all_contracts(session: Session):
        """Get all contracts from database."""
        return session.query(Contract).all()

    @staticmethod
    def get_contract_by_id(session: Session, contract_id: int):
        """Get a contract from database with its ID."""
        return session.get(Contract, contract_id)
