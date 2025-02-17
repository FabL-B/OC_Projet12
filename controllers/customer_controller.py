from services.customer_service import CustomerService
from models.auth import auth_required
from sqlalchemy.orm import Session
from models.permission import CustomerPermission, permission_required


class CustomerController:
    """Controller for handling customers."""

    def __init__(self):
        self.service = CustomerService
        self.permission_class = CustomerPermission

    @auth_required
    @permission_required("list_all")
    def list_all(self, user_payload, session: Session):
        """Retrieve all customers."""
        return self.service.list_all(session)

    @auth_required
    @permission_required("get")
    def get(self, user_payload, session: Session, entity_id: int):
        """Retrieve a specific customer by ID."""
        return self.service.get_by_id(session, entity_id)

    @auth_required
    @permission_required("create")
    def create(self, user_payload, session: Session, **kwargs):
        """Create a new customer."""
        return self.service.create(session, **kwargs)

    @auth_required
    @permission_required("update")
    def update(self, user_payload, session: Session, entity_id, data):
        """Update an existing customer."""
        return self.service.update(session, entity_id, data)

    @auth_required
    @permission_required("delete")
    def delete(self, user_payload, session: Session, entity_id):
        """Delete a customer."""
        return self.service.delete(session, entity_id)
