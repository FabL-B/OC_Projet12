from services.contract_service import ContractService
from controllers.base_controller import BaseController

class ContractController(BaseController):
    """Controller for handling contracts."""
    
    service = ContractService
