from pydantic import BaseModel
from typing import List
from enum import Enum

class MovieMedia(BaseModel):
    genres: List[str]
    year: int

class SeriesMedia(BaseModel):
    genres: List[str]
    years: List[str]




class Rating(BaseModel):
    rate: float
    rates_amount: str

class MiniMedia(BaseModel):
    imdb_id: str
    name: str
    free: bool
    poster: str
    rating: Rating