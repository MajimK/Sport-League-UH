from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.teams import Team

class Teams_Player(SQLModel, table = True):
    tp_id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="players.player_id")
    team_id: int = Field(foreign_key="team.team_id")


class Players(SQLModel, table=True):
    player_id: Optional[int] = Field(default=None, primary_key=True)
    CI: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    faculty: str = Field(index=True)

    team: List["Team"] = Relationship(back_populates="players", link_model=Teams_Player)


