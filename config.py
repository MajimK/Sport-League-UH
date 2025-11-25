import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    FOOTBALL_DATA_API_KEY = os.getenv('FOOTBALL_DATA_API_KEY')

# ldap_config.py
import ldap3
from config import Config

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
