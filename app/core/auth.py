from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import Settings
from app.database.db import get_session
from sqlmodel import Session, select
from app.database.models.users import Users, Permission, UserPermission
from typing import Optional
from config import settings
from app.schemas.users import UsersCreate
from app.utils.permissions import ROLE_PERMISSIONS

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica la contraseña usando pbkdf2_sha256."""
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    """Hashea la contraseña para nuevos usuarios."""
    return pwd_context.hash(password)


def get_user_by_username(username: str, session: Session):
    query = select(Users).where(Users.username == username)
    return session.exec(query).first()

def get_user_by_id(user_id: int, session: Session):
    query = select(Users).where(Users.user_id == user_id)
    return session.exec(query).first()


def authenticate_user(username: str, password: str, session: Session):
    user = get_user_by_username(username, session)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> Users:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: Optional[str] = payload.get("sub")
        role: Optional[str] = payload.get("role")
        if not username or not role:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = get_user_by_username(username, session)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def require_permission(permission: str):
    def checker(
        user: Users = Depends(get_current_user),
        session: Session = Depends(get_session)
    ):
        if not has_permission(user, permission, session):
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos suficientes"
            )
        return user
    return checker


def create_user(user: UsersCreate, session: Session):
    user_existing = get_user_by_username(user.username, session)
    if user_existing:
        raise ValueError("Ya existe el usuario")
    
    db_user = Users.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def delete_user(user_id: int, session: Session):
    user_existing = get_user_by_id(user_id, session)
    if not user_existing:
        raise ValueError("El usuario no existe")
    session.delete(user_existing)
    session.commit()
    return 

def has_permission(user: Users, permission: str, session: Session) -> bool:
    perms = set(ROLE_PERMISSIONS.get(user.role, []))
    query = (
        select(Permission.name)
        .join(UserPermission)
        .where(UserPermission.user_id == user.user_id)
    )
    extra_perms = session.exec(query).all()
    perms.update(extra_perms)
    return permission in perms


def add_perms_to_user(user_id: int, perm_names: list[str], session: Session):
    user = session.exec(select(Users).where(Users.user_id == user_id)).first()
    if not user:
        raise ValueError("Usuario no encontrado")

    for perm_name in perm_names:
        perm = session.exec(select(Permission).where(Permission.name == perm_name)).first()
        if not perm:
            raise ValueError(f"Permiso '{perm_name}' no existe")

        # Evitar duplicados
        exists = session.exec(
            select(UserPermission).where(
                (UserPermission.user_id == user_id) &
                (UserPermission.permission_id == perm.id)
            )
        ).first()

        if not exists:
            session.add(UserPermission(user_id=user_id, permission_id=perm.id or 0))

    session.commit()


