import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import DATABASE_URL

# Ajuste para Supabase y otros servicios que requieren SSL
connect_args = {}
if "supabase.co" in DATABASE_URL or "render.com" in DATABASE_URL:
    if "sslmode" not in DATABASE_URL:
        # Si no tiene sslmode, lo intentamos añadir via connect_args
        connect_args["sslmode"] = "require"

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()