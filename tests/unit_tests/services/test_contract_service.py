from unittest.mock import MagicMock, patch
import pytest
from app.services.contract_service import ContractService
from app.models.contract import Contract


def test_get_contract_by_id():
    """Test retrieving a contract by its ID."""
    mock_session = MagicMock()
    mock_contract = Contract(
        id=1,
        customer_id=2,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )

    with patch(
        "app.repository.contract_repository.ContractRepository.get_contract_by_id",  # noqa: E501
        return_value=mock_contract
    ):
        contract = ContractService.get_by_id(mock_session, 1)

    assert contract.id == 1
    assert contract.amount == 5000


def test_get_contract_by_id_not_found():
    """Test attempting to retrieve a non-existent contract."""
    mock_session = MagicMock()

    with patch(
        "app.repository.contract_repository.ContractRepository.get_contract_by_id",  # noqa: E501
        return_value=None
    ):
        with pytest.raises(ValueError, match="Contract not found."):
            ContractService.get_by_id(mock_session, 99)


def test_create_contract():
    """Test creating a new contract."""
    mock_session = MagicMock()
    mock_contract = Contract(
        id=1,
        customer_id=2,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )

    with patch(
        "app.repository.contract_repository.ContractRepository.create_contract",  # noqa: E501
        return_value=mock_contract
    ):
        created_contract = ContractService.create(
            mock_session,
            2,
            5000,
            2000,
            "unsigned"
        )

    assert created_contract.amount == 5000
    assert created_contract.status == "unsigned"


def test_update_contract():
    """Test updating an existing contract."""
    mock_session = MagicMock()
    mock_contract = Contract(
        id=1,
        customer_id=2,
        amount=5000,
        amount_due=2000,
        status="unsigned"
    )
    updated_contract = Contract(
        id=1,
        customer_id=2,
        amount=5000,
        amount_due=2000,
        status="signed"
    )

    with patch(
        "app.repository.contract_repository.ContractRepository.get_contract_by_id",  # noqa: E501
        return_value=mock_contract
    ):
        with patch(
            "app.repository.contract_repository.ContractRepository.update_contract",  # noqa: E501
            return_value=updated_contract
        ):
            result = ContractService.update(
                mock_session,
                1,
                {"status": "signed"}
            )

    assert result.status == "signed"
