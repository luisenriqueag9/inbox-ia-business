import uuid
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.models import CompanyStatus, ConversationStatus, MessageDirection

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
    id: UUID
    name: str
    status: CompanyStatus

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.lower()
        return v

class LoginResponse(BaseModel):
    company: CompanyResponse
    user: UserResponse

class RegisterResponse(BaseModel):
    company: CompanyResponse
    user: UserResponse

# New request schema for creating a conversation
class ConversationCreateRequest(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=10000)

    model_config = ConfigDict(extra="forbid")

    @field_validator("customer_name", mode="before")
    @classmethod
    def strip_customer_name(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("message", mode="before")
    @classmethod
    def strip_message(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

# Response schemas
class MessageResponse(BaseModel):
    id: UUID
    direction: MessageDirection
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(BaseModel):
    id: UUID
    customer_name: str
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse]

    model_config = ConfigDict(from_attributes=True)
class ConversationListItem(BaseModel):
    id: UUID
    customer_name: str
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime
    last_message: MessageResponse | None = None

    model_config = ConfigDict(from_attributes=True)

class ConversationPageResponse(BaseModel):
    items: list[ConversationListItem]
    page: int
    page_size: int
    total: int

    model_config = ConfigDict()

