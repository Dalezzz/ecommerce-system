from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    nombre: str = Field(min_length=2, max_length=120)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    rol: str
    fecha_registro: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
