import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.repository.contract_repository import ContractRepository
from app.models.contract import Contract
from app.services.contract_service import ContractService

class TestContractService(unittest.TestCase):

    def setUp(self):
        self.session_mock = MagicMock(spec=Session)
        self.contract_data = {
            "customer_id": 1,
            "amount": 1000,
            "amount_due": 500,
            "status": "pending"
        }

    def test_get_by_id(self):
        mock_contract = MagicMock(spec=Contract)
        ContractRepository.get_contract_by_id = MagicMock(return_value=mock_contract)
        contract = ContractService.get_by_id(self.session_mock, 1)
        self.assertEqual(contract, mock_contract)
        ContractRepository.get_contract_by_id.assert_called_once_with(self.session_mock, 1)

    def test_get_by_id_not_found(self):
        ContractRepository.get_contract_by_id = MagicMock(return_value=None)
        with self.assertRaises(ValueError) as context:
            ContractService.get_by_id(self.session_mock, 1)
        self.assertEqual(str(context.exception), "Contract not found.")

    def test_list_all(self):
        mock_contracts = [
            Contract(id=1, amount=1000, amount_due=500, status="pending"),
            Contract(id=2, amount=2000, amount_due=0, status="paid"),
        ]
        ContractRepository.get_all_contracts = MagicMock(return_value=mock_contracts)
        contracts = ContractService.list_all(self.session_mock)
        self.assertEqual(len(contracts), 2)
        self.assertEqual(contracts[0]["id"], 1)
        ContractRepository.get_all_contracts.assert_called_once_with(self.session_mock)

    def test_list_unsigned(self):
        mock_contracts = [
            Contract(id=1, amount=1000, amount_due=500, status="unsigned"),
        ]
        ContractRepository.get_unsigned_contracts = MagicMock(return_value=mock_contracts)
        contracts = ContractService.list_unsigned(self.session_mock)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0]["id"], 1)
        ContractRepository.get_unsigned_contracts.assert_called_once_with(self.session_mock)

    def test_list_unpaid(self):
        mock_contracts = [
            Contract(id=1, amount=1000, amount_due=500, status="pending"),
        ]
        ContractRepository.get_unpaid_contracts = MagicMock(return_value=mock_contracts)
        contracts = ContractService.list_unpaid(self.session_mock)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0]["id"], 1)
        ContractRepository.get_unpaid_contracts.assert_called_once_with(self.session_mock)


    @patch("app.services.contract_service.ContractRepository.create_contract")
    def test_create(self, mock_create_contract):
        mock_contract = MagicMock(spec=Contract)
        mock_create_contract.return_value = mock_contract
        contract = ContractService.create(self.session_mock, self.contract_data["customer_id"], self.contract_data["amount"], self.contract_data["amount_due"], self.contract_data["status"])
        self.assertEqual(contract, mock_contract)
        mock_create_contract.assert_called_once()

    @patch("app.services.contract_service.ContractRepository.get_contract_by_id")
    @patch("app.services.contract_service.ContractRepository.update_contract")
    def test_update(self, mock_update_contract, mock_get_contract_by_id):
        mock_contract = MagicMock(spec=Contract)
        mock_get_contract_by_id.return_value = mock_contract
        updated_data = {"amount": 1500}
        updated_contract = ContractService.update(self.session_mock, 1, updated_data)
        self.assertEqual(updated_contract, mock_update_contract.return_value) # Or mock_contract if update returns the object
        mock_get_contract_by_id.assert_called_once_with(self.session_mock, 1)
        mock_update_contract.assert_called_once_with(self.session_mock, 1, updated_data)

    @patch("app.services.contract_service.ContractRepository.get_contract_by_id")
    def test_update_contract_not_found(self, mock_get_contract_by_id):
        mock_get_contract_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            ContractService.update(self.session_mock, 1, {"amount": 1500})
        self.assertEqual(str(context.exception), "Contract not found.")

    @patch("app.services.contract_service.ContractRepository.get_contract_by_id")
    @patch("app.services.contract_service.ContractRepository.delete_contract")
    def test_delete(self, mock_delete_contract, mock_get_contract_by_id):
        mock_contract = MagicMock(spec=Contract)
        mock_get_contract_by_id.return_value = mock_contract
        deleted = ContractService.delete(self.session_mock, 1)
        self.assertEqual(deleted, mock_delete_contract.return_value)  # or True if delete returns a boolean
        mock_get_contract_by_id.assert_called_once_with(self.session_mock, 1)
        mock_delete_contract.assert_called_once_with(self.session_mock, 1)

    @patch("app.services.contract_service.ContractRepository.get_contract_by_id")
    def test_delete_contract_not_found(self, mock_get_contract_by_id):
        mock_get_contract_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            ContractService.delete(self.session_mock, 1)
        self.assertEqual(str(context.exception), "Contract not found.")

if __name__ == '__main__':
    unittest.main()