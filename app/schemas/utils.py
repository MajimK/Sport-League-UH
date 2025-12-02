from typing import List
from pydantic import BaseModel

class AddPlayersResponse(BaseModel):
    added: List[int]
    skipped: List[dict]

class AddPlayersRequest(BaseModel):
    players: List[int]
