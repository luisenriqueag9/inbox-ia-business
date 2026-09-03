from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.schemas import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
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


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: DBSession = Depends(get_db)):
    user = authenticate_user(request.email, request.password, db)

    raw_token = generate_session_token()
    token_hash = hash_session_token(raw_token)
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    new_session = SessionModel(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    try:
        db.add(new_session)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return LoginResponse(company=user.company, user=user)
