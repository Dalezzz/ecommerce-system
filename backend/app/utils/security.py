from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..config import API_PREFIX, ALGORITHM, SECRET_KEY
from ..db.database import get_db
from ..db.models import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

def require_admin(current_user: Usuario = Depends(get_current_user)):
    role_value = getattr(current_user.rol, "value", str(current_user.rol))
    if role_value != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return current_user