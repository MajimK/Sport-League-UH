from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from app.database.models.games import League_games

if TYPE_CHECKING:
    from app.database.models.seasons import Season
    from app.database.models.games import Games
    from app.database.models.teams import Team

class Match(SQLModel, table=True):
    match_id: Optional[int] = Field(default=None, primary_key=True)
    season_id: int = Field(foreign_key="season.season_id")
    league_id: int = Field(foreign_key="leagues.league_id")
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)
    location: str = Field(index=True)


