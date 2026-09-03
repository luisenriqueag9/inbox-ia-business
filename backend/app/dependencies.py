from datetime import datetime, timezone
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.models import Session as SessionModel, User, CompanyStatus
from app.security import hash_session_token


def get_current_user(
    session_token: str | None = Cookie(default=None, alias="session"),
    db: DBSession = Depends(get_db),
) -> User:
    """Retrieve the authenticated user from the opaque session cookie.

    The function validates the presence of the cookie, hashes the raw token,
    looks up the corresponding SessionModel, checks expiration, and verifies that
    the associated company is not suspended.
    """
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado."
        )

    token_hash = hash_session_token(session_token)
    stmt = select(SessionModel).where(SessionModel.token_hash == token_hash)
    session_obj = db.execute(stmt).scalars().first()
    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado."
        )

    if session_obj.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado."
        )

    user = session_obj.user
    if user.company.status == CompanyStatus.SUSPENDED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La empresa está suspendida."
        )

    return user
