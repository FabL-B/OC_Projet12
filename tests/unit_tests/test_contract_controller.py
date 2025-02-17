import pytest
from models.contract import Contract
from controllers.contract_controller import ContractController
from services.contract_service import ContractService
from models.auth import Auth
from models.permission import ContractPermission


@pytest.fixture
def contract_controller():
    """Fixture to instantiate ContractController."""
    return ContractController()


def test_list_all_contracts(mocker, contract_controller, mock_session):
    """Test retrieving all contracts."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        ContractService,
        "list_all",
        return_value=[
            Contract(id=1, customer_id=101, amount=5000.0, status="signed"),
            Contract(id=2, customer_id=102, amount=3000.0, status="unsigned"),
        ],
    )

    contracts = contract_controller.list_all(mock_session)

    assert len(contracts) == 2
    assert contracts[0].status == "signed"
    assert contracts[1].status == "unsigned"
    ContractService.list_all.assert_called_once_with(mock_session)


def test_get_contract(mocker, contract_controller, mock_session):
    """Test retrieving a specific contract."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        ContractService,
        "get_by_id",
        return_value=Contract(
            id=1, customer_id=101, amount=5000.0, status="signed"
        ),
    )

    contract = contract_controller.get(mock_session, entity_id=1)

    assert contract.status == "signed"
    ContractService.get_by_id.assert_called_once_with(mock_session, 1)


def test_create_contract(mocker, contract_controller, mock_session):
    """Test creating a contract."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(
        ContractPermission,
        "has_permission",
        return_value=True,
    )
    mocker.patch.object(
        ContractService,
        "create",
        return_value=Contract(
            id=1, customer_id=101, amount=5000.0, status="signed"
        ),
    )

    contract_controller.create(
        mock_session,
        customer_id=101,
        amount=5000.0,
        amount_due=2000.0,
        status="signed",
    )

    ContractService.create.assert_called_once_with(
        mock_session,
        customer_id=101,
        amount=5000.0,
        amount_due=2000.0,
        status="signed",
    )


def test_update_contract(mocker, contract_controller, mock_session):
    """Test updating a contract."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(ContractService, "update", return_value=True)

    success = contract_controller.update(
        mock_session, entity_id=1, data={"amount_due": 1500.0}
    )

    assert success is True
    ContractService.update.assert_called_once_with(
        mock_session, 1, {"amount_due": 1500.0}
    )


def test_delete_contract(mocker, contract_controller, mock_session):
    """Test deleting a contract."""
    mocker.patch.object(
        Auth,
        "is_authenticated",
        return_value={"id": 1, "role": "Management"},
    )
    mocker.patch.object(ContractService, "delete", return_value=True)

    success = contract_controller.delete(mock_session, entity_id=1)

    assert success is True
    ContractService.delete.assert_called_once_with(mock_session, 1)
