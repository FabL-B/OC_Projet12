import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import engine, Base  # noqa: E402
from app.models.user import User  # noqa: F401, E402
from app.models.customer import Customer  # noqa: F401, E402
from app.models.contract import Contract  # noqa: F401, E402
from app.models.event import Event  # noqa: F401, E402


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()
