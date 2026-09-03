from pwdlib import PasswordHash

# Creamos el hasher utilizando la configuracion recomendada de pwdlib (Argon2 por defecto).
password_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Genera un hash seguro utilizando Argon2."""
    return password_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Verifica si una contraseña coincide con su hash almacenado."""
    return password_context.verify(password, password_hash)
