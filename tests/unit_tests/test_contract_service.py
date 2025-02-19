from app.models.contract import Contract
from app.services.contract_service import ContractService
from app.repository.contract_repository import ContractRepository


def test_create_contract_success(mock_session, mocker):
    """Test successful contract creation."""
    mocker.patch.object(
        ContractRepository,
        "get_contract_by_id",
        return_value=None,
    )

    fake_contract = Contract(
        id=1, customer_id=101, amount=5000.0, status="signed"
    )
    mocker.patch.object(
        ContractRepository,
        "create_contract",
        return_value=fake_contract,
    )

    contract = ContractService.create(
        mock_session,
        customer_id=101,
        amount=5000.0,
        amount_due=2000.0,
        status="signed"
    )

    assert contract.amount == 5000.0
    assert contract.status == "signed"


def test_delete_contract_success(mock_session, mocker):
    """Test successful contract deletion."""
    fake_contract = Contract(
        id=1, customer_id=101, amount=5000.0, status="signed"
    )

    mocker.patch.object(
        ContractRepository,
        "get_contract_by_id",
        return_value=fake_contract,
    )
    mocker.patch.object(
        ContractRepository,
        "delete_contract",
        return_value=fake_contract,
    )

    deleted_contract = ContractService.delete(mock_session, 1)

    assert deleted_contract == fake_contract
