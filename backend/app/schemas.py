import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.models import CompanyStatus

class RegisterRequest(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("company_name", mode="before")
    @classmethod
    def strip_company_name(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.lower()
        return v

class CompanyResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: CompanyStatus

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class RegisterResponse(BaseModel):
    company: CompanyResponse
    user: UserResponse
