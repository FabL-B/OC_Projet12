from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User


class UserRepository:
    """Handles database operations related to the User entity."""
    @staticmethod
    def save(session: Session, user: User):
        """Save user in data base."""
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except IntegrityError:
            session.rollback()
            raise ValueError("Email already exists.")

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
        return session.query(User).all()
