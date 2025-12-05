from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    description: str =""

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    team_id: int
    pass

class TeamOut(TeamBase):
    team_id: int
    pass

    class Config:
        from_attributes = True
