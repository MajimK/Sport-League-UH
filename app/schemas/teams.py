from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    description: str =""

class TeamCreate(TeamBase):
    game_name: str
    pass

class TeamUpdate(TeamBase):
    team_id: int
    pass

class TeamOut(TeamBase):
    team_id: int
    pass

    class Config:
        from_attributes = True

class TempTeam(BaseModel):
    name: str
    description: str
    game_id: int
    
    class Config:
        orm_mode = True
