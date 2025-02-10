from functools import wraps


def role_required(*allowed_roles):
    """Wrapper to restrain access to a specific role."""
    def decorator(func):
        @wraps(func)
        def wrapper(user_payload, *args, **kwargs):
            user_role = user_payload.get("role")
            if user_role not in allowed_roles:
                raise PermissionError(
                    f"Access denied: Role '{user_role}' "
                    "not authorized for this action"
                )
            return func(user_payload, *args, **kwargs)
        return wrapper
    return decorator
