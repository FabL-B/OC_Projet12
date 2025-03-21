from app.models import User


class UserRepository:
    """Handles database operations related to the User entity."""
    @staticmethod
    def create_user(session, user):
        """Create a new user in the database."""
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update_user(session, user_id, data):
        """Update an existing user in the database."""
        user = session.get(User, user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
        return user

    @staticmethod
    def delete_user(session, user_id):
        """Delete a user from the database."""
        user = session.get(User, user_id)
        session.delete(user)
        return user

    @staticmethod
    def get_user_by_id(session, user_id):
        """Get user from database with its ID."""
        return session.get(User, user_id)

    @staticmethod
    def get_user_by_email(session, email):
        """Get user from database with its email."""
        return session.query(User).filter_by(email=email).first()

    @staticmethod
    def get_all_users(session):
        """Retrieve all users from the database."""
        return session.query(User).all()
