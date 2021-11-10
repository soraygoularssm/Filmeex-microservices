from fastapi import APIRouter
from .media.imdb_reciver import Series
from .models import ImdbList

router = APIRouter()

series = Series()

@router.get('/top250')
async def get_top_250():
    res = series.get_tops()
    return res

@router.get('/id')
async def get_series_id(name: str , year: int):
    movie_id = series.get_id(name , year)
    return movie_id

@router.post('/details')
async def series_details(body: ImdbList):
    res = series.get_details(body.imdb_ids)
    return res

@router.get('/imgs/{imdb_id}')
async def get_all_images(imdb_id : str):
    res = series.get_images(movie_id=imdb_id)
    return res

@router.get('/season/{imdb_id}/{season}')
async def get_all_images(imdb_id : str , season : int):
    res = series.seasons(imdb_id=imdb_id , season=season)
    return res
