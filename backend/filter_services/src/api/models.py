from pydantic import BaseModel
from typing import List , Optional
import datetime

# GENRE MODELS
class Genre(BaseModel):
    genre_name: str
    icon: Optional[str] = None

# CATEGORY MODELS
class Movie(BaseModel):
    imdb_id: str
    name: str
    image: str
    year: int 
    imdb: float

class Category(BaseModel):
    category_name: str
    icon: str
    selected_movies: List[Movie] = []

# MOVIE MODELS
class MediaSlide(BaseModel):
    imdb_id: str
    name: str
    picture: str
    genre: List[Genre]
    year: int 
    director_or_creator: Optional[str] = None
    imdb: float
    summary: str

class CastSlide(BaseModel):
    imdb_id: str
    name: str
    pictur: str

class Slide(BaseModel):
    title: str
    movie: Optional[MediaSlide] = None
    cast: Optional[CastSlide] = None
    background_pic: Optional[str] = None

class Slider(BaseModel):
    slider_name: str
    slider_pre_picture: Optional[str] = None
    slides: List[Slide] = []
    slider_exp_date: datetime.date 

