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

    created_contract = ContractRepository.create_contract(
        mock_session, contract)

    mock_session.add.assert_called_once_with(contract)
    mock_session.commit.assert_called_once()
    assert created_contract == contract


def test_get_contract_by_id():
    mock_session = MagicMock()
    mock_session.get.return_value = Contract(
        id=2,
        customer_id=1,
        amount=7000,
        amount_due=5000,
        status="signed"
    )

    retrieved_contract = ContractRepository.get_contract_by_id(mock_session, 2)

    mock_session.get.assert_called_once_with(Contract, 2)
    assert retrieved_contract.status == "signed"
