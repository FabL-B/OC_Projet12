class BasePermission:
    """Base class for permission management."""

    def has_permission(self, user_payload, action):
        """Returns False by default to block access if not defined."""
        return False

    def has_object_permission(self, user_payload, obj, action):
        """Returns False by default to prevent access if not defined."""
        return False


class UserPermission(BasePermission):
    """Manages permissions for users."""

    def has_permission(self, user_payload, action):
        if action in ['get_all_users', 'get_user']:
            return True
        if action in ['create_user', 'update_user', 'delete_user']:
            return user_payload.get("role") == "management"
        return False

    def has_object_permission(self, user_payload, obj, action):
        return self.has_permission(user_payload, action)


class CustomerPermission(BasePermission):
    """Manages permissions for customers."""

    def has_permission(self, user_payload, action):
        if action in ['get_all_customers', 'get_customer']:
            return True
        if action == 'create_customer':
            return user_payload.get("role") == "sales"
        return True

    def has_object_permission(self, user_payload, customer, action):
        if action in ['edit_customer', 'delete_customer']:
            return (user_payload.get("role") == "sales" and
                    customer.sales_user_id == user_payload.get("id"))
        return True


class ContractPermission(BasePermission):
    """Manages permissions for contracts."""

    def has_permission(self, user_payload, action):
        if action in ['get_all_contracts', 'get_contract']:
            return True
        if action == 'create_contract':
            return user_payload.get("role") == "management"
        return True

    def has_object_permission(self, user_payload, contract, action):
        if action in ['update_contract', 'delete_contract']:
            if user_payload.get("role") == "management":
                return True
            return (user_payload.get("role") == "sales" and
                    contract.customer.sales_user_id == user_payload.get("id"))
        return True


class EventPermission(BasePermission):
    """Manages permissions for events."""

    def has_permission(self, user_payload, action):
        if action in ['get_all_events', 'get_event']:
            return True
        if action == 'create_event':
            return user_payload.get("role") == "sales"
        return True

    def has_object_permission(self, user_payload, event, action):
        if action == 'create_event':
            return (user_payload.get("role") == "sales" and
                    event.contract.is_signed and
                    event.contract.customer.sales_user_id == user_payload.get("id"))
        if action == 'update_event':
            return (user_payload.get("role") == "support" and
                    event.support_user_id == user_payload.get("id")) or (
                    user_payload.get("role") == "management")
        return True
