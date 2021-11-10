from pydantic import BaseModel
from typing import List, Optional

class Cast(BaseModel):
    imdb_id: str
    name: str
    actor: bool = False
    director: bool = False
    headshot: str
    birth_date: Optional[str] = None
    media: List[str] = []

class CastUpdate(BaseModel):
    name: Optional[str] = None
    headshot: Optional[str]
    actor: Optional[bool] = None
    director: Optional[bool] = None
    birth_date: Optional[str] = None
    media: Optional[List[str]] = []