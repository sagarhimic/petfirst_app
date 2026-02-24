from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------
    # Application
    # -------------------------
    APP_NAME: str = "PetFirst API"
    ENVIRONMENT: str = "local"
    DEBUG: bool = True

    # -------------------------
    # Base URL (IMPORTANT)
    # -------------------------
    BASE_URL: str = "http://127.0.0.1:8000"

    # -------------------------
    # Database
    # -------------------------
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "petfirst_db"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""

    # -------------------------
    # JWT CONFIG ✅
    # -------------------------
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # -------------------------
    # Media
    # -------------------------
    MEDIA_URL: str = "/uploads"
    MEDIA_ROOT: str = "uploads"

    class Config:
        env_file = ".env"
        case_sensitive = True

    CUSTOMER_SIDE_COMMISSION: int = 5  


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# ✅ import this everywhere
settings = get_settings()
