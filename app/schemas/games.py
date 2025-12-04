from pydantic import BaseModel

class GameBase(BaseModel):
    name: str

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    Game_id: int
    pass

class GameOut(GameBase):
    Game_id: int
    pass

    class Config:
        from_attributes = True
