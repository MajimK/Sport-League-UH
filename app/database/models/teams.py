from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from app.database.models.players import Teams_Player

if TYPE_CHECKING:
    from app.database.models.players import Players

class Team(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(index=True)

    players: List["Players"] = Relationship(back_populates="team", link_model=Teams_Player)

