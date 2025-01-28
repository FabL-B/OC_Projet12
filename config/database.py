import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurer SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Test de connexion
def test_connection():
    try:
        with engine.connect() as connection:
            print("Connexion réussie à la base de données.")
    except Exception as e:
        print(f"Erreur de connexion : {e}")

if __name__ == "__main__":
    test_connection()
