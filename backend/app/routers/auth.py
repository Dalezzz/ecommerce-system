from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..schemas.user import UserCreate, UserResponse, Token
from ..services.auth_service import crear_usuario, autenticar_usuario, crear_token
from ..db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registro", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def registro(user: UserCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, user)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = autenticar_usuario(db, form_data.username, form_data.password)
    role_value = getattr(user.rol, "value", str(user.rol))
    token = crear_token({"sub": str(user.id), "rol": role_value})
    return {"access_token": token, "token_type": "bearer"}