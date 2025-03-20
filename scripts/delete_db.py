import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import engine, Base  # noqa: E402


def delete_database():
    """Completely deletes the database."""

    Base.metadata.reflect(bind=engine)

    print("Deleting all tables...")
    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    delete_database()
