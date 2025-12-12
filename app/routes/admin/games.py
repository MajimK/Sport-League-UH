from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.games import GameOut
from sqlmodel import Session
from app.core.games import get_all_sports



router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/", response_model=list[GameOut])
def get_games(session: Session=Depends(get_session)):
    teams = get_all_sports(session)
    return teams