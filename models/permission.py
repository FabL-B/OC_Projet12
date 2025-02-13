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
        if action in ['list_all', 'get']:
            return True
        if action in ['create', 'update', 'delete']:
            return user_payload.get("role") == "management"
        return False

    def has_object_permission(self, user_payload, obj, action):
        return self.has_permission(user_payload, action)


class CustomerPermission(BasePermission):
    """Manages permissions for customers."""

    def has_permission(self, user_payload, action):
        if action in ['list_all', 'get']:
            return True
        if action == 'create':
            return user_payload.get("role") == "sales"
        return True

    def has_object_permission(self, user_payload, customer, action):
        if action in ['update', 'delete']:
            return (user_payload.get("role") == "sales" and
                    customer.sales_user_id == user_payload.get("id"))
        return True


class ContractPermission(BasePermission):
    """Manages permissions for contracts."""

    def has_permission(self, user_payload, action):
        if action in ['list_all', 'get']:
            return True
        if action == 'create':
            return user_payload.get("role") == "management"
        return True

    def has_object_permission(self, user_payload, contract, action):
        if action in ['update', 'delete']:
            if user_payload.get("role") == "management":
                return True
            return (user_payload.get("role") == "sales" and
                    contract.customer.sales_user_id == user_payload.get("id"))
        return True


class EventPermission(BasePermission):
    """Manages permissions for events."""

    def has_permission(self, user_payload, action):
        if action in ['list_all', 'get']:
            return True
        if action == 'create':
            return user_payload.get("role") == "sales"
        return True

    def has_object_permission(self, user_payload, event, action):
        if action == 'create':
            return (
                user_payload.get("role") == "sales" and
                event.contract.is_signed and
                event.contract.customer.sales_user_id == user_payload.get("id")
            )
        if action == 'update':
            return (user_payload.get("role") == "support" and
                    event.support_user_id == user_payload.get("id")) or (
                    user_payload.get("role") == "management")
        return True
