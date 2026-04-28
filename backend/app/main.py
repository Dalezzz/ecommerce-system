from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .config import API_PREFIX, APP_NAME, APP_VERSION, CORS_ORIGINS
from .db.database import Base, engine
from .routers import auth, cart, orders, products, reports
from .utils.exceptions import DomainError

app = FastAPI(title=APP_NAME, version=APP_VERSION, docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        for column_name, column_ddl in (
            ("subtotal", "DOUBLE PRECISION NOT NULL DEFAULT 0"),
            ("impuestos", "DOUBLE PRECISION NOT NULL DEFAULT 0"),
            ("costo_envio", "DOUBLE PRECISION NOT NULL DEFAULT 0"),
            ("metodo_pago", "VARCHAR NOT NULL DEFAULT 'tarjeta'"),
        ):
            exists = connection.execute(
                text(
                    """
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'ordenes' AND column_name = :column_name
                    """
                ),
                {"column_name": column_name},
            ).first()
            if not exists:
                connection.execute(text(f"ALTER TABLE ordenes ADD COLUMN {column_name} {column_ddl}"))


@app.exception_handler(ValueError)
async def value_error_handler(_: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError):
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "Unexpected server error"},
    )


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(products.router, prefix=API_PREFIX)
app.include_router(cart.router, prefix=API_PREFIX)
app.include_router(orders.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)