from fastapi import APIRouter, Depends
from app.database.db import get_session
from app.schemas.teams import TeamOut
from app.schemas.players import PlayerOut
from app.core.league import (get_players_by_league, 
                            get_teams_by_league,)

router = APIRouter(prefix="/leagues", tags=["player"])


@router.get("/{league_id}/teams", response_model=list[TeamOut])
def get_teams(league_id: int, session= Depends(get_session)):
    teams = get_teams_by_league(league_id, session)
    return teams

# Esta ruta no va dento de admin
@router.get("/{league_id}/players", response_model= list[PlayerOut])
def get_players(league_id: int, session = Depends(get_session)):
    players = get_players_by_league(league_id, session)
    return players