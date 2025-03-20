from unittest.mock import MagicMock
from app.models import Contract
from app.repository.contract_repository import ContractRepository


def test_create_contract():
    mock_session = MagicMock()
    contract = Contract(
        id=1,
        customer_id=1,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    created_contract = ContractRepository.create_contract(
        mock_session, contract)

    mock_session.add.assert_called_once_with(contract)
    mock_session.commit.assert_called_once()
    assert created_contract == contract


def test_get_contract_by_id():
    mock_session = MagicMock()
    mock_session.get.return_value = Contract(
        id=1,
        customer_id=1,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )

    retrieved_contract = ContractRepository.get_contract_by_id(mock_session, 1)

    mock_session.get.assert_called_once_with(Contract, 1)
    assert retrieved_contract.status == "unsigned"


def test_update_contract():
    mock_session = MagicMock()
    contract = Contract(
        id=1,
        customer_id=1,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )
    mock_session.get.return_value = contract

    updated_data = {"status": "signed", "amount_due": 8000}
    updated_contract = ContractRepository.update_contract(
        mock_session, 1,
        updated_data
    )

    mock_session.get.assert_called_once_with(Contract, 1)
    assert updated_contract.status == "signed"
    assert updated_contract.amount_due == 8000


def test_delete_contract():
    mock_session = MagicMock()
    contract = Contract(
        id=1,
        customer_id=1,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )
    mock_session.get.return_value = contract

    deleted_contract = ContractRepository.delete_contract(mock_session, 1)

    mock_session.get.assert_called_once_with(Contract, 1)
    mock_session.delete.assert_called_once_with(contract)
    assert deleted_contract == contract
