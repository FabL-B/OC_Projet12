class AppView:
    """View for the main user interface (menu and authentication)."""

    @staticmethod
    def get_login_credentials():
        """Prompts for login credentials."""
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        return email, password

    @staticmethod
    def show_main_menu(menu_actions):
        """Dynamically displays the main menu and gets the user's choice."""
        print("\nMain Menu")
        for key, (description, _) in menu_actions.items():
            print(f"{key}️ - {description}")
        return input("Make your choice: ").strip()

    @staticmethod
    def show_user_menu():
        """Displays the User panel menu and gets the user's choice."""
        print("\nUser Panel")
        print("1 - Show all users")
        print("2 - Create a user")
        print("3 - Return to main menu")

        return input("Make your choice: ").strip()
