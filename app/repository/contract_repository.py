from app.models.contract import Contract


class ContractRepository:
    """Handles database operations related to the Contract entity."""
    @staticmethod
    def create_contract(session, contract):
        """Create a new contract in database."""
        session.add(contract)
        session.refresh(contract)
        return contract

    @staticmethod
    def update_contract(session, contract_id, data):
        """Update an existing contract in database."""
        contract = session.get(Contract, contract_id)
        if contract:
            for key, value in data.items():
                setattr(contract, key, value)
        return contract

    @staticmethod
    def delete_contract(session, contract_id):
        """Delete a contract from database."""
        contract = session.get(Contract, contract_id)
        session.delete(contract)
        return contract

    @staticmethod
    def get_all_contracts(session):
        """Get all contracts from database."""
        return session.query(Contract).all()

    @staticmethod
    def get_unsigned_contracts(session):
        """
        Retrieves all contracts that are unsigned.
        """
        return session.query(Contract).filter_by(status="unsigned").all()

    @staticmethod
    def get_unpaid_contracts(session):
        """Retrieves contracts where `amount_due` different from `amount`."""
        return (
            session.query(Contract)
            .filter(Contract.amount_due != Contract.amount)
            .all()
        )

    @staticmethod
    def get_contract_by_id(session, contract_id):
        """Get a contract from database with its ID."""
        return session.get(Contract, contract_id)
