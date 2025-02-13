from services.customer_service import CustomerService
from controllers.base_controller import BaseController

class CustomerController(BaseController):
    """Controller for handling customers."""
    
    service = CustomerService
