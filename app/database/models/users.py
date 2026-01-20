from sqlmodel import SQLModel, Field
from typing import Optional
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    comunicator = "comunicator"


class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    faculty: Optional[str]
    role: UserRole = Field(default=UserRole.manager)

class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

class UserPermission(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)

