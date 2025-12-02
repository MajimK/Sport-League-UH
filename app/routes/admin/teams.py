from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.teams import TeamCreate, TeamOut
from app.schemas.utils import AddPlayersResponse, AddPlayersRequest
from app.schemas.players import PlayerOut
from sqlmodel import Session
from app.core.teams import (get_all_teams, 
                            save_team, 
                            get_teams_by_id, 
                            get_players_by_team, 
                            add_players_to_team)


router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/", response_model=list[TeamOut])
def get_teams(session: Session=Depends(get_session)):
    teams = get_all_teams(session)
    return teams

@router.get("/{team_id}", response_model=TeamOut)
def get_one_team(team_id: int, session= Depends(get_session)):
    team = get_teams_by_id(team_id, session)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el equipo")
    return team


# Esta ruta no va dento de admin
@router.get("/{team_id}/players", response_model= list[PlayerOut])
def get_players(team_id: int, session = Depends(get_session)):
    players = get_players_by_team(team_id, session)
    return players


@router.post("/{team_id}/add-players",response_model=AddPlayersResponse, status_code=status.HTTP_201_CREATED)
def add_player(team_id: int, body: AddPlayersRequest, session=Depends(get_session)):
    response = add_players_to_team(team_id, body, session)
    return response

@router.post("/", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
def create_team(team: TeamCreate, session=Depends(get_session)):
    try:
        return save_team(team, session)
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
