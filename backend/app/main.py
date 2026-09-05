from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.database import check_db_connection
from app.routers import auth, conversations

app = FastAPI(title="Inbox IA Business API", version="0.0.1")

app.include_router(auth.router)
app.include_router(conversations.router)


@app.get("/")
def root():
    return {"message": "Inbox IA Business API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    """Comprueba la conectividad con PostgreSQL ejecutando SELECT 1."""
    try:
        check_db_connection()
        return {"status": "ok", "database": "reachable"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "database": "unreachable"},
        )
