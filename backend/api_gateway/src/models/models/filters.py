from pydantic import BaseModel
from typing import List , Optional
import datetime

# GENRE MODELS
class GenreModel(BaseModel):
    genre_name: str
    icon: Optional[str] = None

# CATEGORY MODELS
class MiniMovieModel(BaseModel):
    imdb_id: str
    name: str
    image: str
    year: int 
    imdb: float

class CategoryModel(BaseModel):
    category_name: str
    icon: str
    selected_movies: List[MiniMovieModel] = []

# MOVIE MODELS
class MediaSlideModel(BaseModel):
    imdb_id: str
    name: str
    picture: str
    genre: List[GenreModel]
    year: int 
    director_or_creator: Optional[str] = None
    imdb: float
    summary: str

class CastSlideModel(BaseModel):
    imdb_id: str
    name: str
    pictur: str

class SlideModel(BaseModel):
    title: str
    movie: Optional[MediaSlideModel] = None
    cast: Optional[CastSlideModel] = None
    background_pic: Optional[str] = None

class SliderModel(BaseModel):
    slider_name: str
    slider_pre_picture: Optional[str] = None
    slides: List[SlideModel] = []
    slider_exp_date: datetime.date 
