from pydantic import BaseModel , BaseConfig , HttpUrl
from typing import List, Optional
import datetime
from enum import Enum

class Qualities(str,Enum):
    quality_240 = '240p'
    quality_360 = '360p'
    quality_480 = '480p'
    quality_720 = '720p'
    quality_1080 = '1080p'
    quality_2160 = '2160p'

class Url(BaseModel):
    quality: Qualities
    url: str

class Sources(BaseModel):
    urls: List[Url]
    subtiles: Optional[List[Url]] = []
    audios: Optional[List[HttpUrl]] = []

class Comment(BaseModel):
    username: str
    text: str
    comment_date: str
    is_public: bool = False

class Rating(BaseModel):
    rate: float
    rates_amount: str

class PersonIn(BaseModel):
    name: str
    id: str

class Crew(BaseModel):
    stars: List[PersonIn]
    directors: Optional[List[str]] = None
    writers: Optional[List[str]] = None

class ContentType(str,Enum):
    movie: 'movie'
    series: 'series'

class MiniMedia(BaseModel):
    imdb_id: str
    name: str
    free: bool
    poster: str
    genres: List[str]
    rating: Rating
    content_type: ContentType

class PlainMedia(BaseModel):
    imdb_id: str
    name: str
    farsi_name: Optional[str] = None
    free: bool = False
    summary: str
    poster: str
    rating: Rating
    likes: int = 0
    dislikes: int = 0
    comments: Optional[List[Comment]] = []
    countries: List[str]
    languages: List[str]
    genres: List[str]
    crew: Crew
    sub_urls: Optional[List[HttpUrl]] = []

class PlainMediaUpdate(BaseModel):
    name: Optional[str] = None
    farsi_name: Optional[str] = None
    free: Optional[bool] = None
    summary: Optional[str] = None
    poster: Optional[str] = None
    rating: Optional[Rating] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    comments: Optional[List[Comment]] = []
    countries: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    genres: Optional[List[str]] = []
    crew: Optional[Crew] = None
    sub_urls: Optional[List[HttpUrl]] = []


# # MOVIE RELATED
class MiniMovie(MiniMedia):
    year: int
    content_type: ContentType = 'movie'

class Movie(PlainMedia):
    year: Optional[int] = 100
    sources: Sources
    runtime: int = 100
    budget: Optional[str] = None
    related_movies: Optional[List[MiniMedia]] = []

class MovieUpdate(PlainMediaUpdate):
    year: Optional[int] = None
    movie_sources: Optional[Sources] = None
    directors: Optional[List[str]] = []
    runtime: Optional[int] = None
    budget: Optional[str] = None
    related_movies: Optional[List[MiniMedia]] = []

# SERIES RELATED
class Episode(BaseModel):
    ep_number: int
    sources: Optional[List[Sources]] = []

class Season(BaseModel):
    season_number: int
    episodes: List[Episode]

class MiniSeries(MiniMedia):
    years: List[int]
    content_type: ContentType = 'series'

class Series(PlainMedia):
    creators: Optional[List[str]] = []
    years: List[int]
    each_episode_runtime: int
    seasons: List[Season]
    related_series: Optional[List[MiniMedia]] = []

class SeriesUpdate(PlainMediaUpdate):
    creator: Optional[List[str]] = []
    years: Optional[List[int]] = []
    each_episode_runtime: Optional[int] = None
    seasons: Optional[List[Season]] = None
    related_movies: Optional[List[MiniMedia]] = []

# GENRES
class Genre(BaseModel):
    genre_name: str
    icon: Optional[str] = None
