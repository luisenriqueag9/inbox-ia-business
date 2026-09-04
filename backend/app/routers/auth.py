from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from app.config import get_cookie_secure
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.schemas import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.dependencies import get_current_user
from app.models import Company, CompanyStatus, User, Session as SessionModel
from app.security import hash_password, verify_password, generate_session_token, hash_session_token
from datetime import datetime, timezone, timedelta

def authenticate_user(email: str, password: str, db: DBSession) -> User:
    """Valida credenciales y estado de la empresa.

    - Busca el usuario por email.
    - Si no existe o la contraseña es incorrecta, lanza 401.
    - Si la empresa está suspendida, lanza 403.
    - Si todo es correcto, devuelve el objeto ``User``.
    """
    stmt = select(User).where(User.email == email)
    user = db.execute(stmt).scalars().first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas."
        )
    if user.company.status == CompanyStatus.SUSPENDED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La empresa está suspendida."
        )
    return user
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register(request: RegisterRequest, db: DBSession = Depends(get_db)):
    # 1. Verificar si el email ya existe
    stmt = select(User).where(User.email == request.email)
    existing_user = db.execute(stmt).scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado."
        )

    # 2. Hashear password
    hashed = hash_password(request.password)

    # 3. Crear Company
    company = Company(name=request.company_name)
    db.add(company)

    try:
        db.flush()  # Asigna ID a la compañia
        
        # 4. Crear User vinculado
        user = User(
            company_id=company.id,
            email=request.email,
            password_hash=hashed
        )
        db.add(user)
        
        db.commit()
        db.refresh(company)
        db.refresh(user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado."
        )
    except Exception:
        db.rollback()
        raise

    return RegisterResponse(company=company, user=user)

@router.get("/me", response_model=LoginResponse)
def me(current_user: User = Depends(get_current_user)):
    return LoginResponse(company=current_user.company, user=current_user)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None, alias="session"),
    db: DBSession = Depends(get_db),
):
    
    if session_token is None:
        
        response.delete_cookie(
            key="session",
            path="/",
            secure=get_cookie_secure(),
            httponly=True,
            samesite="lax",
        )
        return

    token_hash = hash_session_token(session_token)
    stmt = select(SessionModel).where(SessionModel.token_hash == token_hash)
    session_obj = db.execute(stmt).scalars().first()
    if session_obj:
        try:
            db.delete(session_obj)
            db.commit()
        except Exception:
            db.rollback()
            raise
    
    response.delete_cookie(
        key="session",
        path="/",
        secure=get_cookie_secure(),
        httponly=True,
        samesite="lax",
    )
