from sqlmodel import SQLModel, Field
from typing import Optional

class Season_league_team_player(SQLModel, table = True):
    lsgtp_id: Optional[int] = Field(default=None, primary_key=True)
    season_id: int = Field(foreign_key="season.season_id")
    league_id: int = Field(foreign_key="leagues.league_id")
    team_id: int = Field(foreign_key="team.team_id")
    player_id: int = Field(foreign_key="players.player_id")

