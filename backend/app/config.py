import os


APP_NAME = os.getenv("APP_NAME", "API E-commerce")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

DATABASE_URL = os.getenv(
	"DATABASE_URL",
	"postgresql://user:password@db:5432/ecommerce",
)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def _parse_cors_origins(raw_value: str) -> list[str]:
	values = [value.strip() for value in raw_value.split(",")]
	return [value for value in values if value]


CORS_ORIGINS = _parse_cors_origins(os.getenv("CORS_ORIGINS", "http://localhost:4200"))
