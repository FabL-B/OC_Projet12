class UserView:
    """View for user management."""

    @staticmethod
    def show_user_menu():
        """Displays the User panel menu."""
        print("\nUser Panel")
        print("1 - Show all users")
        print("2 - Create a user")
        print("3 - Return to main menu")
        return input("Make your choice: ").strip()

    @staticmethod
    def display_users_and_get_choice(users):
        """
        Displays the list of users and allows selecting details
        or going back.
        """
        if not users:
            print("\nNo users found.")
            return None

        print("\nUser List:")
        for user in users:
            print(
                f"ID {user['id']} | {user['name']} | "
                f"{user['email']} | {user['role']}"
            )

        print("\n Actions:")
        print("Enter a user ID to view details.")
        print("Press Enter to return to the previous menu.")

        user_id = input("User ID: ").strip()
        return int(user_id) if user_id.isdigit() else None

    @staticmethod
    def display_user_details_and_get_choice(user):
        """Displays a user's details and provides action options."""
        print("\nUser Details")
        print(f"ID: {user.id}")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")

        print("\nActions:")
        print("1 - Edit user")
        print("2 - Delete user")
        print("3 - Return to the user list")

        return input("Make your choice: ").strip()

    @staticmethod
    def get_user_update_data():
        """Prompts for new user data."""
        print("\nEdit User")
        name = input("New name (leave blank to keep unchanged): ").strip()
        email = input("New email (leave blank to keep unchanged): ").strip()
        role = input("New role (leave blank to keep unchanged): ").strip()

        user_data = {}

        if name:
            user_data["name"] = name
        if email:
            user_data["email"] = email
        if role:
            user_data["role"] = role

        return user_data

    @staticmethod
    def get_user_creation_data():
        """Prompts for information to create a new user."""
        print("\nCreate a New User")
        name = input("Name: ").strip().title()
        email = input("Email: ").strip().lower()
        password = input("Password: ").strip()
        role = input("Role (Support, Manager, Sales): ").strip()

        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        }
