from pydantic import BaseModel
from typing import List

class ImdbList(BaseModel):
    imdb_ids: List[str]

class CastList(BaseModel):
    cast_ids: List[str]