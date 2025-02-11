from sqlalchemy.orm import Session
from models import User


class UserRepository:
    """Handles database operations related to the User entity."""
    @staticmethod
    def create_user(session: Session, user: User):
        """Create a new user in data base."""
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update_user(session: Session, user_id: int, data: dict):
        """Update an existing user in data base."""
        user = session.get(User, user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            session.commit()
        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: int):
        """Get user from database with its ID."""
        return session.get(User, user_id)

    @staticmethod
    def get_user_by_email(session: Session, user_email: str):
        """Get user from database with its email."""
        return session.query(User).filter_by(email=user_email).first()

    @staticmethod
    def get_all_users(session: Session):
        """Get all users database."""
        return session.query(User).all()
