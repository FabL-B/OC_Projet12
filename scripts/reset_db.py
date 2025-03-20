import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import engine, Base  # noqa: E402


def reset_database():
    """Completely resets the database and recreate tables."""

    Base.metadata.reflect(bind=engine)

    print("Deleting all tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables recreated successfully.")


if __name__ == "__main__":
    reset_database()
