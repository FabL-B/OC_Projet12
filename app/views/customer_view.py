class CustomerView:
    """View for customer management."""

    @staticmethod
    def show_customer_menu():
        """Displays the Customer panel menu and gets the user's choice."""
        print("\nCustomer Panel")
        print("1 - Show all customers")
        print("2 - Show my customers only")
        print("3 - Create a customer")
        print("4 - Return to main menu")
        return input("Make your choice: ").strip()

    @staticmethod
    def display_customers_and_get_choice(customers):
        """
        Displays the list of customers and allows viewing details
        or going back.
        """
        if not customers:
            print("\nNo customers found.")
            return None

        print("\nCustomer List:")
        for customer in customers:
            print(
                f"ID: {customer['id']} | "
                f"Name: {customer['name']} | "
                f"Company name: {customer['company_name']} | "
                f"Email: {customer['email']} | "
                f"Phone: {customer['phone']}"
            )

        print("\nActions:")
        print("Enter a customer ID to view details.")
        print("Press Enter to return to the previous menu.")

        customer_id = input("Customer ID: ").strip()
        return int(customer_id) if customer_id.isdigit() else None

    @staticmethod
    def display_customer_details_and_get_choice(customer):
        """Displays customer details and provides action options."""
        print("\nCustomer Details")
        print(f"ID: {customer.id}")
        print(f"Name: {customer.name}")
        print(f"Company name: {customer.company_name}")
        print(f"Email: {customer.email}")
        print(f"Phone: {customer.phone}")

        print("\nActions:")
        print("1 - Edit customer")
        print("2 - Delete customer")
        print("3 - Return to the customer list")

        return input("Make your choice: ").strip()

    @staticmethod
    def get_customer_creation_data():
        """Retrieves and sanitizes customer data."""
        print("\nCreate a new customer")
        name = input("Name: ").strip().title()
        company_name = input("Company name: ").strip().title()
        email = input("Email: ").strip().lower()
        phone = input("Phone: ").strip()
        sales_contact_id = input("Sales representative ID: ").strip()

        return {
            "name": name,
            "company_name": company_name,
            "email": email,
            "phone": phone,
            "sales_contact_id": (
                int(sales_contact_id) if sales_contact_id.isdigit() else None
            ),
        }

    @staticmethod
    def get_customer_update_data():
        """Prompts for updated customer data."""
        print("\nEdit Customer")
        name = input(
            "Updated name (leave blank to keep unchanged): "
        ).strip().title()
        company_name = input(
            "Updated company name (leave blank to keep unchanged): "
        ).strip().title()
        email = input(
            "Updated email (leave blank to keep unchanged): "
        ).strip().lower()
        phone = input(
            "Updated phone (leave blank to keep unchanged): "
        ).strip()

        customer_data = {}

        if name:
            customer_data["name"] = name
        if company_name:
            customer_data["company_name"] = company_name
        if email:
            customer_data["email"] = email
        if phone:
            customer_data["phone"] = phone

        return customer_data
