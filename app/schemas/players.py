from pydantic import BaseModel
    

class PlayerBase(BaseModel):
    CI: str
    name: str
    faculty: str | None = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    player_id: int
    pass

class PlayerOut(PlayerBase):
    player_id: int
    pass

    class Config:
        from_attributes = True
