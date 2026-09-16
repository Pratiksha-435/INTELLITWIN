import json
import os
from typing import List, Union

# Dual compatibility handler for Pydantic v1 & v2
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pydantic import field_validator
    PYDANTIC_V2 = True
except ImportError:
    from pydantic import BaseSettings, validator
    PYDANTIC_V2 = False

if PYDANTIC_V2:
    class Settings(BaseSettings):
        PROJECT_NAME: str = "IntelliTwin AI Enterprise Core"
        API_V1_STR: str = "/api/v1"
        DEBUG: bool = False
        SECRET_KEY: str = "super-secret-key-change-this-in-production-intellitwin"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 Days

        # Database
        DATABASE_URL: str = "sqlite+aiosqlite:///./intellitwin.db"

        # Redis & Celery
        REDIS_URL: str = "redis://localhost:6379/0"
        CELERY_BROKER_URL: str = "redis://localhost:6379/1"
        CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

        # CORS
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ]

        @field_validator("BACKEND_CORS_ORIGINS", mode="before")
        def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
            if isinstance(v, str) and not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
            elif isinstance(v, str) and v.startswith("["):
                return json.loads(v)
            return v

        BASE_INDOOR_TARGET_TEMP: float = 22.5
        CARBON_INTENSITY_KG_KWH: float = 0.82

        model_config = SettingsConfigDict(
            case_sensitive=True,
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )
else:
    class Settings(BaseSettings):
        PROJECT_NAME: str = "IntelliTwin AI Enterprise Core"
        API_V1_STR: str = "/api/v1"
        DEBUG: bool = False
        SECRET_KEY: str = "super-secret-key-change-this-in-production-intellitwin"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 Days

        # Database
        DATABASE_URL: str = "sqlite+aiosqlite:///./intellitwin.db"

        # Redis & Celery
        REDIS_URL: str = "redis://localhost:6379/0"
        CELERY_BROKER_URL: str = "redis://localhost:6379/1"
        CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

        # CORS
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ]

        @validator("BACKEND_CORS_ORIGINS", pre=True)
        def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
            if isinstance(v, str) and not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
            elif isinstance(v, str) and v.startswith("["):
                return json.loads(v)
            return v

        BASE_INDOOR_TARGET_TEMP: float = 22.5
        CARBON_INTENSITY_KG_KWH: float = 0.82

        class Config:
            case_sensitive = True
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "ignore"

settings = Settings()