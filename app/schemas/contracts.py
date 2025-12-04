from pydantic import BaseModel

class ContractBase(BaseModel):
    pass
class ContractCreate(ContractBase):
    player_id: int
    league_id: int
    season_id: int
    team_id: int
    pass

class GameUpdate(ContractBase):
    Game_id: int
    pass

class GameOut(ContractBase):
    Game_id: int
    pass

    class Config:
        from_attributes = True
