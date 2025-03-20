import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import SessionLocal  # noqa: E402
from app.models.user import User  # noqa: E402
from app.repository.user_repository import UserRepository  # noqa: E402


def create_admin():
    """Create an admin user."""
    session = SessionLocal()

    existing_admin = UserRepository.get_user_by_email(
        session,
        "admin@test.com"
    )
    if existing_admin:
        print("Administrator already exists.")
    else:
        admin = User(name="admin", email="admin@test.com", role="Admin")

        admin.set_password("test")
        session.add(admin)

        session.commit()

        print("Admin user successfully inserted.")
    session.close()


if __name__ == "__main__":
    create_admin()
