from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
import os 

# Variables de entorno (con valores por defecto para prueba local)
# DB_USER = os.getenv("DB_USER", "postgres")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_NAME = os.getenv("DB_NAME", "hermesdb")
# DB_PORT = os.getenv("DB_PORT", "5432")

DB_USER = os.getenv("DB_USER", "postgres.lgoxhgpvhzskohpbhskf")
DB_PASSWORD = os.getenv("DB_PASSWORD", "hermespass")
DB_HOST = os.getenv("DB_HOST", "aws-0-us-west-1.pooler.supabase.com")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "6543")

# Construcción de la URL de la base de datos
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos como una dependencia de FastAPI
def get_database_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para probar la conexión a la base de datos
def test_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print(f"\033[92m✅ Conectado a la base de datos: {DATABASE_URL}\033[0m")
    except Exception as e:
        print(f"\033[91m❌ Error de conexión a la base de datos:\n{e}\033[0m")

if __name__ == "__main__":
    test_database_connection()