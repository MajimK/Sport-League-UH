from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from app.database.models.players import Teams_Player

if TYPE_CHECKING:
    from app.database.models.players import Players
    from app.database.models.games import Games
    from app.database.models.leagues import Leagues

class Team(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(index=True)
    game_id: int = Field(foreign_key="games.game_id")

    players: List["Players"] = Relationship(back_populates="team", link_model=Teams_Player)
    game: "Games" = Relationship(back_populates="teams")


