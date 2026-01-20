from fastapi import APIRouter, Depends
from app.database.db import get_session
from app.schemas.players import PlayerOut
from app.schemas.teams import TeamOut
from sqlmodel import Session
from app.core.players import (get_teams_by_player, 
                              get_all_players, 
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