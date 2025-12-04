from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from app.database.models.games import League_games

if TYPE_CHECKING:
    from app.database.models.seasons import Season
    from app.database.models.games import Games
    from app.database.models.teams import Team

class Leagues(SQLModel, table=True):
    league_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(index= True)
    initial_date: int = Field(ge=1, le=12)
    final_date: int = Field(ge=1, le=12)

    games: List["Games"] = Relationship(back_populates="leagues", link_model=League_games)



