from app.models.contract import Contract
from app.repository.contract_repository import ContractRepository


def test_create_contract(mock_session):
    """Test the creation and saving of a contract in the database."""
    contract = Contract(
        customer_id=101, amount=5000.0, amount_due=2000.0, status="signed"
    )

    ContractRepository.create_contract(mock_session, contract)

    assert mock_session.add.called
    assert mock_session.commit.called


def test_get_contract_by_id(mock_session):
    """Test retrieving a contract by ID."""
    contract = Contract(id=1, customer_id=101, amount=5000.0, status="signed")
    mock_session.get.return_value = contract

    result = ContractRepository.get_contract_by_id(mock_session, 1)

    assert result == contract


def test_delete_contract(mock_session):
    """Test deleting a contract from the database."""
    contract = Contract(id=1, customer_id=101, amount=5000.0, status="signed")
    mock_session.get.return_value = contract

    result = ContractRepository.delete_contract(mock_session, 1)

    assert mock_session.delete.called
    assert mock_session.commit.called
    assert result == contract
