from config.database import SessionLocal
from controllers.app_controller import AppController


def main():
    """Point d'entrée de l'application."""
    print("\n🚀 Démarrage de l'application CRM...\n")

    session = SessionLocal()

    try:
        app = AppController(session)
        app.run()
    finally:
        session.close()


if __name__ == "__main__":
    main()
