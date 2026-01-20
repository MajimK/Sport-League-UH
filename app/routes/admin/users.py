from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.database.models.users import UserRole
from app.schemas.users import UsersCreate, UsersOut, PermsRequest
from app.core.auth import create_user, delete_user, require_permission, add_perms_to_user
from sqlmodel import Session


router = APIRouter(prefix="/managing", tags=["player"])

@router.post("/create-user", 
        response_model=UsersOut, 
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(require_permission(UserRole.admin))]
        )
def create_users(user: UsersCreate, session: Session =Depends(get_session)):
    try:
        return create_user(user, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Ya existe el usuario")
    
@router.delete("/delete-user/{user_id}", 
               status_code=status.HTTP_202_ACCEPTED,
               dependencies=[Depends(require_permission(UserRole.admin))])
def remove_user(user_id:int, session: Session = Depends(get_session)):
    try:
        return delete_user(user_id, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="El jugador no existe")

@router.post("/add-perm/{user_id}", 
            status_code=status.HTTP_202_ACCEPTED, 
            dependencies=[Depends(require_permission(UserRole.admin))])
def add_perm(user_id: int, req: PermsRequest, session: Session = Depends(get_session)):
    try:
        add_perms_to_user(user_id, req.perms, session)
        return {"msg": f"Permisos agregados al usuario {user_id}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))