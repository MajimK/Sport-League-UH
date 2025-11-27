import os
from enum import Enum
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    FOOTBALL_DATA_API_KEY = os.getenv('FOOTBALL_DATA_API_KEY')

class LDAPConfig:
    LDAP_SERVER = '10.6.240.65'
    LDAP_ADMIN = 'cn=admin,dc=uh,dc=cu'
    LDAP_PASS = 'Nodo.2024'

class Query(str, Enum):
    APPROVED = "APPROBADO"
    ERROR_USER_CATEGORY = "ERROR_USER_CATEGORY"
    ERROR_NOT_FOUND = "ERROR_NO_ENCONTRADO"
    ERROR_PASSWORD = "ERROR_CONTRASEÑA"
    ERROR_SERVICE = "ERROR_SERVICIO"

class Settings(BaseSettings):
    APP_NAME: str = "Sport League UH"
    ALLOWED_ORIGINS: list[str] = ["*"]  # Cambia luego para producción
    DATABASE_URL: str = "postgresql+psycopg://user:password@db:5432/sportdb"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    model_config = SettingsConfigDict(extra='ignore')

settings = Settings()
