from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.players import PlayerCreate, PlayerOut
from app.schemas.teams import TeamOut
from sqlmodel import Session
from app.core.players import (get_teams_by_player, 
                              get_all_players, 
                              save_player, 
                              get_player_by_id)

router = APIRouter(prefix="/players", tags=["player"])


@router.get("/", response_model=list[PlayerOut])
def get_player(session: Session=Depends(get_session)):
    player = get_all_players(session)
    return player

@router.get("/{player_id}", response_model=PlayerOut)
def get_one_player(team_id: int, session= Depends(get_session)):
    team = get_player_by_id(team_id, session)
    return team

# Este endpoint no va en admin
@router.get("/{player_id}/teams", response_model=list[TeamOut])
def get_teams(player_id: int, session= Depends(get_session)):
    teams = get_teams_by_player(player_id, session)
    return teams

@router.post("/", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
def create_player(team: PlayerCreate, session=Depends(get_session)):
    try: 
        return save_player(team, session)
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Ya existe el jugador")