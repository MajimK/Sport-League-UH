from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.leagues import LeagueCreate, LeagueOut
from app.schemas.teams import TeamOut
from app.schemas.players import PlayerOut
from app.schemas.season import SeasonOut
from sqlmodel import Session
from app.core.league import (get_all_leagues, 
                            save_league, 
                            get_league_by_id, 
                            get_players_by_league, 
                            get_teams_by_league,
                            get_seasons_by_league)


router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[LeagueOut])
def get_leagues(session: Session=Depends(get_session)):
    league = get_all_leagues(session)
    return league

@router.get("/{league_id}", response_model=LeagueOut)
def get_one_league(league_id: int, session= Depends(get_session)):
    league = get_league_by_id(league_id, session)
    if not league:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el equipo")
    return league

# Esta ruta va en otra parte
@router.get("/{league_id}/teams", response_model=list[TeamOut])
def get_teams(league_id: int, session= Depends(get_session)):
    teams = get_teams_by_league(league_id, session)
    return teams

# Esta ruta no va dento de admin
@router.get("/{league_id}/players", response_model= list[PlayerOut])
def get_players(league_id: int, session = Depends(get_session)):
    players = get_players_by_league(league_id, session)
    return players

@router.get("/{league_id}/seasons", response_model=SeasonOut)
def get_seasons(league_id: int, session = Depends(get_session)):
    seasons = get_seasons_by_league(league_id, session)
    return seasons

@router.post("/", response_model=LeagueOut, status_code=status.HTTP_201_CREATED)
def create_league(league: LeagueCreate, session=Depends(get_session)):
    try:
        return save_league(league, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)





# @router.put("/{team_id}", response_model=TeamOut)
# def update_team(team_id: int, team: TeamUpdate, db=Depends(get_session)):
#     cur = db.cursor(cursor_factory=RealDictCursor)

#     cur.execute(
#         "UPDATE teams SET name=%s, description=%s WHERE id=%s RETURNING id, name, description",
#         (team.name, team.description, team_id),
#     )

#     updated = cur.fetchone()
#     if not updated:
#         raise HTTPException(status_code=404, detail="Team not found")

#     db.commit()
#     return updated


# @router.delete("/{team_id}")
# def delete_team(team_id: int, db=Depends(get_session)):
#     cur = db.cursor()

#     cur.execute("DELETE FROM teams WHERE id=%s RETURNING id", (team_id,))
#     result = cur.fetchone()

#     if not result:
#         raise HTTPException(status_code=404, detail="Team not found")

#     db.commit()
#     return {"message": "Team deleted successfully"}
