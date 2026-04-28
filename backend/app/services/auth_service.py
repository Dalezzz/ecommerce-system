from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from ..db.models import RolUsuario, Usuario
from ..schemas.user import UserCreate
from sqlalchemy.orm import Session
from ..utils.exceptions import AuthenticationError, ConflictError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def hash_password(password):
    return pwd_context.hash(password)


def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def crear_usuario(db: Session, user_data: UserCreate):
    if obtener_usuario_por_email(db, user_data.email):
        raise ConflictError("Email ya registrado")

    hashed = hash_password(user_data.password)
    nuevo = Usuario(
        email=user_data.email,
        password_hash=hashed,
        nombre=user_data.nombre,
        rol=RolUsuario.cliente,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def autenticar_usuario(db: Session, email: str, password: str):
    user = obtener_usuario_por_email(db, email)
    if not user or not verificar_password(password, user.password_hash):
        raise AuthenticationError("Credenciales incorrectas")
    return user


def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)