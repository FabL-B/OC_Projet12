from sqlalchemy.orm import Session
from services.user_service import UserService
from app.auth.auth import auth_required, Auth
from app.permissions.permission import UserPermission, permission_required
from views.user_view import UserView


class UserController:
    """Controller for handling users."""

    def __init__(self):
        self.service = UserService
        self.permission_class = UserPermission

    @auth_required
    @permission_required("list_all")
    def list_all_users(self, user_payload, session: Session):
        """Display all users."""
        while True:
            users = self.service.list_all(session)
            user_id = UserView.display_users_and_get_choice(users)

            if user_id is None:
                break

            self.show_user_details(session, user_id)

    @auth_required
    @permission_required("get")
    def show_user_details(self, user_payload, session: Session, user_id: int):
        """Display user details and prompt for update or delete selection."""
        user = self.service.get_by_id(session, user_id)
        if not user:
            print("\nUser not found.")
            return

        while True:
            choice = UserView.display_user_details_and_get_choice(user)

            if choice == "1":
                self.update_user(session, user_id)
            elif choice == "2":
                self.delete_user(session, user_id)
                break
            elif choice == "3":
                break
            else:
                print("\nInvalid choice, please try again.")

    @auth_required
    @permission_required("get")
    def get(self, user_payload, session: Session, user_id: int):
        """Retrieve a specific user by ID."""
        return self.service.get_by_id(session, user_id)

    @auth_required
    @permission_required("create")
    def create_user(self, user_payload, session: Session):
        """Create a new user."""
        user_data = UserView.get_user_creation_data()
        self.service.create(session, **user_data)
        print("User successfully created.")

    @auth_required
    @permission_required("update")
    def update_user(self, user_payload, session: Session, user_id: int):
        """Update an existing user."""
        updated_data = UserView.get_user_update_data()
        if updated_data:
            self.service.update(session, user_id, updated_data)
            print(f"User {user_id} successfully updated.")

    @auth_required
    @permission_required("delete")
    def delete_user(self, user_payload, session: Session, user_id: int):
        """Delete a user."""
        confirm = input(
            f"Confirm deletion of user {user_id}? (y/n): "
        ).strip().lower()

        if confirm == "y":
            self.service.delete(session, user_id)
            print(f"User {user_id} successfully deleted.")

    def login_user(self, session: Session, email: str, password: str):
        """Allow a user to log in."""
        tokens = Auth.authenticate_user(session, email, password)
        if tokens:
            Auth.save_token(tokens["access_token"], tokens["refresh_token"])
            print(f"Connected! Welcome, {tokens['user'].name}.")
            return tokens

        print("Incorrect email or password.")
        return None
