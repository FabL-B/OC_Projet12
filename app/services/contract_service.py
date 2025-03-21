from app.repository.contract_repository import ContractRepository
from app.models.contract import Contract
from app.utils.transaction import transactional_session


class ContractService:
    """Handles business logic for contracts."""

    @staticmethod
    def get_by_id(session, contract_id):
        """Get a contract with its ID."""
        contract = ContractRepository.get_contract_by_id(session, contract_id)
        if not contract:
            raise ValueError("Contract not found.")
        return contract

    @staticmethod
    def list_all(session):
        """Return all contracts as dictionnaries."""
        contracts = ContractRepository.get_all_contracts(session)
        return [{"id": contract.id,
                 "amount": contract.amount,
                 "amount_due": contract.amount_due,
                 "status": contract.status}
                for contract in contracts]

    @staticmethod
    def list_unsigned(session):
        """Return unsigned contracts."""
        contracts = ContractRepository.get_unsigned_contracts(session)
        return [{"id": contract.id,
                 "amount": contract.amount,
                 "amount_due": contract.amount_due,
                 "status": contract.status}
                for contract in contracts]

    @staticmethod
    def list_unpaid(session):
        """Return contracts where amount_due ≠ amount."""
        contracts = ContractRepository.get_unpaid_contracts(session)
        return [{"id": contract.id,
                 "amount": contract.amount,
                 "amount_due": contract.amount_due,
                 "status": contract.status}
                for contract in contracts]

    @staticmethod
    def create(session, customer_id, amount, amount_due, status):
        """Creates a new contract."""
        contract = Contract(
            customer_id=customer_id,
            amount=amount,
            amount_due=amount_due,
            status=status
        )
        return ContractRepository.create_contract(session, contract)

    @staticmethod
    def update(session, contract_id, data):
        """Update an existing contract."""
        with transactional_session(session) as s:
            contract = ContractRepository.get_contract_by_id(s, contract_id)
            if not contract:
                raise ValueError("Contract not found.")
            return ContractRepository.update_contract(s, contract_id, data)

    @staticmethod
    def delete(session, contract_id):
        """Delete a contract."""
        with transactional_session(session) as s:
            contract = ContractRepository.get_contract_by_id(s, contract_id)
            if not contract:
                raise ValueError("Contract not found.")
            return ContractRepository.delete_contract(s, contract_id)
