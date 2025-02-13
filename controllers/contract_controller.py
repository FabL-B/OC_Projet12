from services.contract_service import ContractService
from controllers.base_controller import BaseController
from models.permission import ContractPermission

class ContractController(BaseController):
    """Controller for handling contracts."""
    
    service = ContractService
    permission_class = ContractPermission
