from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base


class Settings(BaseSettings):
    PROJECT_NAME: str = "Certificador de Atividades Complementares"
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "sqlite+aiosqlite:///./certificador.db"
    DBBaseModel: ClassVar = declarative_base()
    JWT_SECRET: str = "chave-padrao-apenas-para-testes-locais"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()