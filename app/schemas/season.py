from pydantic import BaseModel

class SeasonBase(BaseModel):
    curso: str

class SeasonCreate(SeasonBase):
    pass

class SeasonUpdate(SeasonBase):
    season_id: int
    pass

class SeasonOut(SeasonBase):
    season_id: int
    pass

    class Config:
        from_attributes = True
