from pydantic import BaseModel

class LeagueBase(BaseModel):
    name: str
    description: str
    initial_date: int
    final_date: int

class LeagueCreate(LeagueBase):
    pass

class LeagueUpdate(LeagueBase):
    league_id: int
    pass

class LeagueOut(LeagueBase):
    league_id: int
    pass

    class Config:
        from_attributes = True
