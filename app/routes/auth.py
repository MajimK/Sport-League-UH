from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.auth import create_access_token, create_refresh_token
from app.core.auth import verify_password, get_user_by_username, get_current_user
from sqlmodel import Session
from app.database.db import get_session

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = get_user_by_username(data.username, session)
    print(data.password)
    if user:
        print(user.password)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access = create_access_token({"sub": user.username, "role": user.is_admin})
    refresh = create_refresh_token({"sub": user.username})

    return TokenResponse(access_token=access, refresh_token=refresh)


@router.get("/me")
def me(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }
