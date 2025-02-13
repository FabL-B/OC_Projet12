from services.customer_service import CustomerService
from controllers.base_controller import BaseController
from models.permission import CustomerPermission

class CustomerController(BaseController):
    """Controller for handling customers."""
    
    service = CustomerService
    permission_class = CustomerPermission
