from pydantic import BaseModel ,HttpUrl
from typing import List , Optional
from enum import Enum

class QualitiesModel(str,Enum):
    quality_240 = '240p'
    quality_360 = '360p'
    quality_480 = '480p'
    quality_720 = '720p'
    quality_1080 = '1080p'
    quality_2160 = '2160p'

class UrlModel(BaseModel):
    # quality: QualitiesModel
    quality: str
    url: str

class SourcesModel(BaseModel):
    urls: List[UrlModel]
    subtiles: Optional[List[UrlModel]] = []
    audios: Optional[List[HttpUrl]] = []

class CommentModel(BaseModel):
    username: str
    text: str
    comment_date: str
    is_public: bool = False

class PersonInModel(BaseModel):
    id: str
    name: str

class CrewModel(BaseModel):
    stars: List[PersonInModel]
    directors: Optional[List[str]] = None
    writers: Optional[List[str]] = None

class RatingModel(BaseModel):
    rate: float
    rates_amount: str

class PlainMediaModel(BaseModel):
    imdb_id: str
    name: str
    farsi_name: Optional[str] = None
    free: bool = False
    summary: str
    poster: str
    rating: RatingModel
    likes: int = 0
    dislikes: int = 0
    comments: Optional[List[CommentModel]] = []
    countries: List[str]
    languages: List[str]
    genres: List[str]
    runtime: int = 100
    crew: CrewModel
    images: Optional[List[HttpUrl]] = []
    sub_urls: Optional[List[HttpUrl]] = []

class PlainMediaUpdate(BaseModel):
    name: Optional[str] = None
    farsi_name: Optional[str] = None
    free: Optional[bool] = None
    summary: Optional[str] = None
    poster: Optional[str] = None
    rating: Optional[RatingModel] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    comments: Optional[List[CommentModel]] = []
    countries: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    genres: Optional[List[str]] = []
    crew: Optional[CrewModel] = None
    images: Optional[List[HttpUrl]] = []
    sub_urls: Optional[List[HttpUrl]] = []

class MovieModel(PlainMediaModel):
    year: Optional[int] = 2000
    sources: Optional[SourcesModel] = None
    budget: Optional[str] = None
    # related_movies: Optional[List[MiniMedia]] = []

class MovieUpdateModel(PlainMediaUpdate):
    year: Optional[int] = None
    sources: Optional[SourcesModel] = None
    budget: Optional[str] = None
    # related_movies: Optional[List[MiniMedia]] = []

class EpisodeModel(BaseModel):
    ep_number: int
    sources: Optional[List[SourcesModel]] = []

class SeasonModel(BaseModel):
    season_number: int
    episodes: List[EpisodeModel]

class SeriesModel(PlainMediaModel):
    creators: Optional[List[str]] = []
    years: List[int]
    each_episode_runtime: int
    seasons: List[SeasonModel]
    # related_series: Optional[List[MiniMedia]] = []

class SeriesUpdateModel(PlainMediaUpdate):
    creator: Optional[List[str]] = []
    years: Optional[List[int]] = []
    each_episode_runtime: Optional[int] = None
    seasons: Optional[List[SeasonModel]] = None
    # related_movies: Optional[List[MiniMedia]] = []


class MiniMediaModel(BaseModel):
    imdb_id: str
    name: str
    free: bool
    poster: str
    rating: RatingModel

class AllGenresModel(BaseModel):
    name: str
    media: List[MiniMediaModel]

class AllCategoriesModel(BaseModel):
    name: str
    media: List[MiniMediaModel]