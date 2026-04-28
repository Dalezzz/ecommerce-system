# ecommerce-system

Sistema e-commerce con arquitectura modular para backend, frontend y analitica.

## Backend (FastAPI)

El backend sigue separacion por capas para escalar el dominio sin acoplar rutas con acceso a datos:

- `app/routers`: capa HTTP (valida entrada/salida y expone endpoints).
- `app/services`: reglas de negocio y casos de uso.
- `app/db`: persistencia con SQLAlchemy (engine, sesion, modelos).
- `app/schemas`: contratos de entrada/salida con Pydantic.
- `app/utils`: seguridad, excepciones y utilidades transversales.
- `app/config.py`: configuracion centralizada por variables de entorno.

### Buenas practicas aplicadas

- Versionado de API por prefijo (`/api/v1`) configurable.
- Manejo de errores consistente con excepciones de dominio (`DomainError`, `ValidationError`, `ConflictError`, etc.).
- Seguridad con JWT Bearer y dependencia de usuario autenticado/admin.
- Validaciones de datos con Pydantic (email, password, limites de campos).
- CORS configurable para integracion con frontend.
- Separacion de responsabilidades entre routers y servicios.

## Endpoints base

- Salud: `GET /health`
- Auth: `POST /api/v1/auth/registro`, `POST /api/v1/auth/login`
- Products: `GET /api/v1/products/`, `POST /api/v1/products/`, `PUT /api/v1/products/{id}`
- Cart: `GET /api/v1/cart/`, `POST /api/v1/cart/items`
- Orders: `POST /api/v1/orders/checkout`, `GET /api/v1/orders/mine`
- Reports (admin): `GET /api/v1/reports/sales-summary`, `GET /api/v1/reports/top-products`

## Variables de entorno backend

- `APP_NAME` (default: `API E-commerce`)
- `APP_VERSION` (default: `0.1.0`)
- `API_PREFIX` (default: `/api/v1`)
- `DATABASE_URL`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `60`)
- `CORS_ORIGINS` (lista separada por comas)

## Ejecucion local backend

Desde la carpeta raiz:

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Documentacion OpenAPI:

- `http://127.0.0.1:8000/docs`
