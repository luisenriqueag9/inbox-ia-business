import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from repository root (three levels up from this file)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)


def get_cookie_secure() -> bool:
    """Devuelve el valor booleano de la variable COOKIE_SECURE.

    - La variable debe estar presente en el entorno.
    - Solo se aceptan los valores (ignorando mayúsculas/minúsculas):
        "true"  → True
        "false" → False
    - Cualquier otro valor producirá RuntimeError con mensaje en español.
    """
    value = os.getenv("COOKIE_SECURE")
    if value is None:
        raise RuntimeError("La variable de entorno COOKIE_SECURE no está definida.")
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise RuntimeError("COOKIE_SECURE debe ser 'true' o 'false' (sin comillas), caso insensible.")
