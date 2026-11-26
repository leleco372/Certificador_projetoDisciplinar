from typing import Any, ClassVar
from sqlalchemy.orm import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

DBBaseModel = declarative_base()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Certificador de Atividades Complementares"
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "sqlite+aiosqlite:///./certificador.db"
    JWT_SECRET: str = "chave-padrao-apenas-para-testes-locais"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DBBaseModel: ClassVar[Any] = DBBaseModel

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()