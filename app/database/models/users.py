from sqlmodel import SQLModel, Field
from typing import Optional
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"


class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    email: str
    is_admin: bool
    is_manager: bool
    # role: UserRole = Field(default=UserRole.manager)
