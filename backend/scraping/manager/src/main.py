from fastapi import FastAPI
from api import manager
from enum import Enum

class ContentEnum(str, Enum):
    movies = "movies"
    series = "series"
    animations = "animations"

app = FastAPI()

@app.get('/{start}')
async def get(start: int , content_type: ContentEnum):
    if content_type == content_type.movies:
        return await manager.get5_movies(start)
    elif content_type == content_type.series:
        return await manager.get5_series(start)
    elif content_type == content_type.animations:
        return await manager.get5_animations(start)
