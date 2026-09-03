from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.schemas import RegisterRequest, RegisterResponse
from app.models import Company, User
from app.security import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
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
