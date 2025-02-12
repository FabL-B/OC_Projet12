from functools import wraps

def role_required(user_payload, *allowed_roles):
    """Checks if the user has an authorized role."""
    user_role = user_payload.get("role")
    if user_role not in allowed_roles:
        raise PermissionError(
            f"Access denied: role '{user_role}' "
            "is not authorized for this action."
        )

def affiliation_required(user_payload, entity_id, get_entity, relation_field):
    """Checks if the user is affiliated with a specific entity."""
    user_id = user_payload.get("id")
    entity = get_entity(entity_id)

    if getattr(entity, relation_field) != user_id:
        raise PermissionError(
            "Access denied: You are not authorized to modify this resource."
        )

def permission_required(*allowed_roles, get_entity=None, relation_field=None):
    """
    Check the user role and, if specified, its relation to a specific entity.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(user_payload, entity_id=None, *args, **kwargs):
            # Check user role
            role_required(user_payload, *allowed_roles)

            # Check affiliation if applicable
            if get_entity and relation_field and entity_id is not None:
                affiliation_required(
                    user_payload,
                    entity_id,
                    get_entity,
                    relation_field
                )

            return func(user_payload, entity_id, *args, **kwargs)
        return wrapper
    return decorator
