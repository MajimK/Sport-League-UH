from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db import get_session
from app.schemas.leagues import LeagueOut

from sqlmodel import Session
from app.schemas.match import SearchLeagueMatches, MatchOut, CreateMatches
from app.core.match import get_matches_by_league, create_matches


router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[MatchOut])
def get_matches(search: SearchLeagueMatches,session: Session=Depends(get_session)):
    matches = get_matches_by_league(search, session)
    return matches

@router.post("/")
def create_match(data: CreateMatches, session: Session=Depends(get_session)):
    match = create_matches(data, session)
    return match


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
