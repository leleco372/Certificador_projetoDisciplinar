from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "mysql+aiomysql://root:110806le@localhost:3306/sistema_certificacao"
    DBBaseModel: ClassVar = declarative_base()

    #Secret gerado com comando no terminal
    JWT_SECRET:str = "Aq74UWexBKhtlIhiduaMxweoml63naXZGFD7rHju8dI"
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 60*24*7

    class Config:
        case_sensitive = True

settings: Settings = Settings()