from models.contract import Contract
from services.contract_service import ContractService
from repository.contract_repository import ContractRepository


def test_delete_contract_success(mock_session, mocker):
    """Test successful delete of a contract."""
    fake_contract = Contract(id=1, customer_id=5, amount=1000, status="signed")

    mocker.patch.object(
        ContractRepository, "get_contract_by_id", return_value=fake_contract)
    mocker.patch.object(
        ContractRepository, "delete_contract", return_value=fake_contract)

    deleted_contract = ContractService.delete_contract(mock_session, 1)

    assert deleted_contract == fake_contract
