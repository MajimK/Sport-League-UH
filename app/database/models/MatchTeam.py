from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class TeamRole(str, Enum):
    home = "home"
    away = "away"

class MatchTeam(SQLModel, table=True):
    match_team_id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="match.match_id")
    team_id: int = Field(foreign_key="team.team_id")
    role: TeamRole = Field(index=True) 
    score: int = Field(index=True)

