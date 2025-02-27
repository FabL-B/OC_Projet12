from app.models import User


class UserRepository:
    """Handles database operations related to the User entity."""
    @staticmethod
    def create_user(session, user):
        """Create a new user in data base."""
        session.add(user)
        session.refresh(user)
        return user

    @staticmethod
    def update_user(session, user_id, data):
        """Update an existing user in data base."""
        user = session.get(User, user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
        return user

    @staticmethod
    def delete_user(session, user_id):
        """Delete a user from database."""
        user = session.get(User, user_id)
        session.delete(user)
        return user

    @staticmethod
    def get_user_by_id(session, user_id):
        """Get user from database with its ID."""
        return session.get(User, user_id)

    @staticmethod
    def get_user_by_email(session, user_email):
        """Get user from database with its email."""
        return session.query(User).filter_by(email=user_email).first()

    @staticmethod
    def get_all_users(session):
        """Get all users database."""
        return session.query(User).all()
