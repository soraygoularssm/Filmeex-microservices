from fastapi import APIRouter
from .media.imdb_reciver import Movies
from .models import CastList

router = APIRouter()

@router.post('/details')
async def get_headshot(cast_list: CastList):
    movie = Movies()
    res = movie.get_cast(cast_list.cast_ids)
    return res