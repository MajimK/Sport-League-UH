from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.season import SeasonCreate, SeasonOut
from app.schemas.teams import TeamOut
from app.schemas.players import PlayerOut
from app.schemas.season import SeasonOut
from sqlmodel import Session
from app.core.seasons import (get_all_seasons, 
                            save_season, 
                            get_season_by_id, 
                            get_players_by_season, 
                            get_teams_by_season,
                            get_leagues_by_season)


router = APIRouter(prefix="/season", tags=["season"])


@router.get("/", response_model=list[SeasonOut])
def get_season(session: Session=Depends(get_session)):
    seasons = get_all_seasons(session)
    return seasons

@router.get("/{season_id}", response_model=SeasonOut)
def get_one_season(season_id: int, session= Depends(get_session)):
    season = get_season_by_id(season_id, session)
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el equipo")
    return season

# Esta ruta va en otra parte
@router.get("/{season_id}/teams", response_model=list[TeamOut])
def get_teams(season_id: int, session= Depends(get_session)):
    teams = get_teams_by_season(season_id, session)
    return teams

# Esta ruta no va dento de admin
@router.get("/{season_id}/players", response_model= list[PlayerOut])
def get_players(season_id: int, session = Depends(get_session)):
    players = get_players_by_season(season_id, session)
    return players

@router.get("/{season_id}/leagues", response_model=SeasonOut)
def get_seasons(season_id: int, session = Depends(get_session)):
    seasons = get_leagues_by_season(season_id, session)
    return seasons

@router.post("/", response_model=SeasonOut, status_code=status.HTTP_201_CREATED)
def create_team(team: SeasonCreate, session=Depends(get_session)):
    try:
        return save_season(team, session)
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
