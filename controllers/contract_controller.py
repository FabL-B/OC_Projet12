from services.contract_service import ContractService
from models.auth import auth_required
from sqlalchemy.orm import Session
from models.permission import ContractPermission

class ContractController:
    """Controller for handling contracts."""

    def __init__(self):
        self.service = ContractService
        self.permission_class = ContractPermission

    @auth_required
    def list_all(self, user_payload, session: Session):
        """Retrieve all contracts."""
        return self.service.list_all(session)

    @auth_required
    def get(self, user_payload, session: Session, entity_id: int):
        """Retrieve a specific contract by ID."""
        return self.service.get_by_id(session, entity_id)

    @auth_required
    def create(self, user_payload, session: Session, **kwargs):
        """Create a new contract."""
        return self.service.create(session, **kwargs)

    @auth_required
    def update(self, user_payload, session: Session, entity_id, data):
        """Update an existing contract."""
        return self.service.update(session, entity_id, data)

    @auth_required
    def delete(self, user_payload, session: Session, entity_id):
        """Delete a contract."""
        return self.service.delete(session, entity_id)
