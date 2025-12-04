from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.leagues import Leagues
    from app.database.models.teams import Team

class League_games(SQLModel, table = True):
    lg_id: Optional[int] = Field(default=None, primary_key=True)
    league_id: int = Field(foreign_key="leagues.league_id")
    game_id: int = Field(foreign_key="games.game_id")

class Games(SQLModel, table=True):
    game_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


    teams: List["Team"] = Relationship(back_populates="game")
    leagues: List["Leagues"] = Relationship(back_populates="games", link_model= League_games)

