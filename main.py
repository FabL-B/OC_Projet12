from config.database import SessionLocal
from app.controllers.app_controller import AppController
from app.sentry.integration import init_sentry


def main():
    """Point d'entrée de l'application."""
    print("\n🚀 Démarrage de l'application CRM...\n")

    session = SessionLocal()
    init_sentry()
    try:
        app = AppController(session)
        app.run()
    finally:
        session.close()


if __name__ == "__main__":
    main()
