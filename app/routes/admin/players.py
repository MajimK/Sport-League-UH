from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.players import PlayerCreate, PlayerOut
from app.schemas.teams import TeamOut
from sqlmodel import Session
from app.core.players import save_player


router = APIRouter(prefix="/players", tags=["player"])

@router.post("/", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
def create_player(team: PlayerCreate, session: Session =Depends(get_session)):
    try: 
        return save_player(team, session)
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Ya existe el jugador")