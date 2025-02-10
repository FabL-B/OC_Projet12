from sqlalchemy.orm import sessionmaker
from config.database import engine
from models.auth import Auth
from controllers.user_controller import UserController

# Création de la session SQLAlchemy
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def main():
    print("=== Connexion ===")
    email = input("Email : ")
    password = input("Mot de passe : ")

    # Authentification de l'utilisateur
    tokens = Auth.authenticate_user(session, email, password)
    if not tokens:
        print("❌ Échec de l'authentification.")
        return

    # Stockage des tokens
    Auth.save_token(tokens["access_token"], tokens["refresh_token"])
    print(f"✅ Connexion réussie ! Bienvenue {tokens['user'].name} ({tokens['user'].role})") # noqa

    # Vérification du rôle pour la création d'un utilisateur
    if tokens["user"].role == "Management":
        print("\n=== Création d'un nouvel utilisateur ===")
        name = input("Nom : ")
        new_email = input("Email : ")
        new_password = input("Mot de passe : ")
        role = input("Rôle (Sales, Support, Management) : ")

        # Création de l'utilisateur
        UserController.create_user(session, name, new_email, new_password, role) # noqa
        print("✅ Utilisateur créé avec succès.")

    else:
        print("❌ Vous n'avez pas l'autorisation de créer un utilisateur.")


if __name__ == "__main__":
    main()
