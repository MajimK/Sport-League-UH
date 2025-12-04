from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.contracts import ContractCreate
from app.schemas.teams import TeamOut
from app.core.contracts import (get_all_teams_season_league, 
                            save_contract)


router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def registry_contract(contract: ContractCreate, session=Depends(get_session)):
    try:
        return save_contract(contract, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/season/{season_id}/league/{league_id}/teams", response_model= list[TeamOut])
def get_teams(season_id: int, league_id:int, session= Depends(get_session)):
    teams = get_all_teams_season_league(season_id, league_id, session)
    return teams






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
