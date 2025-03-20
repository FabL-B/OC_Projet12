from config.database import SessionLocal
from app.controllers.app_controller import AppController


def main():
    """Application entry point."""
    print("\nStarting CRM app...\n")

    session = SessionLocal()
    try:
        app = AppController(session)
        app.run()
    finally:
        session.close()


if __name__ == "__main__":
    main()
