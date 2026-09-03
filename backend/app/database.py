import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Carga .env desde la raiz del repositorio (un nivel arriba de backend/).
# En produccion las variables de entorno se inyectan directamente; load_dotenv
# no sobreescribe variables ya definidas en el entorno del proceso.
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "La variable de entorno DATABASE_URL no esta definida. "
        "Copia .env.example a .env en la raiz del repositorio y completa los valores."
    )

# SQLAlchemy 2.x con psycopg 3 requiere el prefijo 'postgresql+psycopg://'.
# Normalizamos el prefijo aqui para que .env.example pueda usar 'postgresql://'
# sin depender del driver, facilitando futuros cambios de driver.
SQLALCHEMY_DATABASE_URL = DATABASE_URL
if DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Engine creado una sola vez a nivel de modulo.
# pool_pre_ping=True verifica la conexion antes de usarla.
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


def check_db_connection() -> None:
    """Ejecuta SELECT 1 para verificar la conectividad con la base de datos."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))