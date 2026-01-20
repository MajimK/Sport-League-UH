from pydantic import BaseModel
from app.database.models.users import UserRole
from typing import List

class UsersBase(BaseModel):
    username: str
    password: str
    email:str
    faculty: str | None = None

class UsersCreate(UsersBase):
    role: UserRole
    pass

class UsersUpdate(UsersBase):
    user_id: int
    pass

class UsersOut(UsersBase):
    user_id: int
    pass

    class Config:
        from_attributes = True

class LoginRequest(UsersBase):
    pass


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PermsRequest(BaseModel):
    perms: List[str]
