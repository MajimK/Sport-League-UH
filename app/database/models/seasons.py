from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.leagues import Leagues

class Season(SQLModel, table=True):
    season_id: Optional[int] = Field(default=None, primary_key=True)
    curso: str = Field(index=True, unique=True)

