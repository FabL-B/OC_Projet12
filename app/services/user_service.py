import re
from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.models.user import User
from app.models.customer import Customer
from app.models.event import Event
from app.auth.auth import Auth
from app.utils.transaction import transactional_session


class UserService:
    """Handles business logic for users."""

    @staticmethod
    def validate_email(email):
        """Validates that the email format is correct."""
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")

        return email

    @staticmethod
    def get_by_id(session, user_id):
        """Retrieves a user by ID."""
        return UserRepository.get_user_by_id(session, user_id)

    @staticmethod
    def list_all(session: Session):
        users = UserRepository.get_all_users(session)
        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
            for user in users
        ]

    @staticmethod
    def create(session, name, email, password, role):
        """Creates a user."""
        with transactional_session(session) as s:
            UserService.validate_email(email)
            existing_user = UserRepository.get_user_by_email(s, email)
            if existing_user:
                raise ValueError("A user with this email already exists.")
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            return UserRepository.create_user(s, user)

    @staticmethod
    def update(session, user_id, data):
        """Update an existing user."""
        with transactional_session(session) as s:
            user = UserRepository.get_user_by_id(s, user_id)

            if not user:
                raise ValueError("User not found.")

            if "email" in data:
                UserService.validate_email(data["email"])

            # Update related customers or events on role update
            new_role = data.get("role")
            if new_role and new_role != user.role:
                if user.role == "Sales":
                    s.query(Customer).filter_by(
                        sales_contact_id=user_id).update(
                            {"sales_contact_id": None}
                        )
                if user.role == "Support":
                    s.query(Event).filter_by(
                        support_contact_id=user_id).update(
                            {"support_contact_id": None}
                        )
            return UserRepository.update_user(s, user_id, data)

    @staticmethod
    def delete(session, user_id):
        """Delete a user."""
        with transactional_session(session) as s:
            user = UserRepository.get_user_by_id(s, user_id)
            if not user:
                raise ValueError("User not found.")
            # Update related customers or events on role update
            session.query(Customer).filter_by(sales_contact_id=user_id).update(
                {"sales_contact_id": None})
            session.query(Event).filter_by(support_contact_id=user_id).update(
                {"support_contact_id": None})
            return UserRepository.delete_user(s, user_id)

    @staticmethod
    def get_user_by_email(session, email):
        """Retrieves a user by email."""
        return UserRepository.get_user_by_email(session, email)

    @staticmethod
    def login_user(session, email, password):
        """Allows a user to log in."""
        tokens = Auth.authenticate_user(session, email, password)
        if tokens:
            Auth.save_token(tokens["access_token"], tokens["refresh_token"])
            return tokens
        return None
