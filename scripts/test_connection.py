import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import engine  # noqa: E402


def test_connection():
    """Tests the connection to the database."""
    try:
        with engine.connect():
            print("Connection to database successful.")
    except Exception as e:
        print(f"Connection error : {e}")


if __name__ == "__main__":
    test_connection()
