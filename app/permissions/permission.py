from functools import wraps


class BasePermission:
    """Base class for permission management."""

    def __init__(self, user_payload):
        self.user_role = user_payload.get("role")
        self.user_id = int(user_payload.get("id"))

    def has_permission(self, action):
        """Admin has all permissions by default."""
        if self.user_role == "Admin":
            return True
        return self.check_permission(action)

    def has_object_permission(self, obj, action):
        """Admin has all object permissions by default."""
        if self.user_role == "Admin":
            return True
        return self.check_object_permission(obj, action)

    def check_permission(self, action):
        """Méthode à implémenter dans les sous-classes."""
        return False

    def check_object_permission(self, obj, action):
        """Méthode à implémenter dans les sous-classes."""
        return False


class UserPermission(BasePermission):
    """Manages permissions for users."""

    def check_permission(self, action):
        if action in ['list', 'get']:
            return True
        if action in ['create', 'update', 'delete']:
            return self.user_role == "Management"
        return False

    def check_object_permission(self, obj, action):
        return self.check_permission(action)


class CustomerPermission(BasePermission):
    """Manages permissions for customers."""

    def check_permission(self, action):
        if action in ['list', 'get']:
            return True
        if action == 'create':
            return self.user_role == "Sales"
        return True

    def check_object_permission(self, customer, action):
        if action in ['update', 'delete']:
            return (self.user_role == "Sales" and
                    customer.sales_contact_id == self.user_id)
        return True


class ContractPermission(BasePermission):
    """Manages permissions for contracts."""

    def check_permission(self, action):
        if action in ['list', 'get']:
            return True
        if action == 'create':
            return self.user_role == "Management"
        return True

    def check_object_permission(self, contract, action):
        if action in ['update', 'delete']:
            if self.user_role == "Management":
                return True
            return (
                self.user_role == "Sales" and
                contract.customer.sales_contact_id == self.user_id
            )
        return True


class EventPermission(BasePermission):
    """Manages permissions for events."""

    def check_permission(self, action):
        """Checks if the user has general permissions for the action."""
        if action in ["list", "get"]:
            return True
        if action == "create":
            return self.user_role == "Sales"
        return True

    def check_object_permission(self, event, action):
        """Checks if the user has specific permissions on the event."""

        if action == "create":
            return (
                self.user_role == "Sales"
                and event.contract.is_signed
                and event.contract.customer.sales_contact_id == self.user_id
            )

        if action == "update":
            return (
                (self.user_role == "Support" and
                 event.support_contact_id == self.user_id)
                or self.user_role == "Management"
            )

        return True


def permission_required(action, requires_object=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, user_payload, *args, **kwargs):
            permission = self.permission_class(user_payload)

            if permission.user_role == "Admin":
                return func(self, user_payload, *args, **kwargs)

            if not permission.has_permission(action):
                raise PermissionError(
                    f"Access denied: No permission for {action}"
                )

            if requires_object:
                obj = kwargs.get("obj")
                if not permission.has_object_permission(obj, action):
                    raise PermissionError(
                        f"Access denied to this {obj.id}, {action}"
                    )

            return func(self, user_payload, *args, **kwargs)
        return wrapper
    return decorator
