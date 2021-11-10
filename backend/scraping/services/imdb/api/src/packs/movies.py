from fastapi import APIRouter
from .media.imdb_reciver import Movies
from .models import ImdbList
import urllib.request
from pathlib import Path
import os

router = APIRouter()

movie = Movies()

@router.get('/top250')
async def get_top_250():
    res = movie.get_tops()
    return res

@router.get('/id')
async def get_movie_id(name: str , year: int):
    movie_id = movie.get_id(name , year)
    return movie_id

@router.post('/details')
async def movie_details(body: ImdbList):
    res = movie.get_details(body.imdb_ids)
    # poster = res[0]['poster']
    # for r in res:
    #     id = r['imdb_id']
    #     poster = r['poster']

    
    # print(os.path.dirname(os.path.realpath(__file__)))
    # print(str(Path.home()))

    # print(poster)

    #     opener = urllib.request.URLopener()
    #     opener.addheader('User-Agent', 'whatever')
    #     try:
    #         opener.retrieve(poster , f'{str(Path.home())}/backend/assets/photos/full/testttt.jpg')
    #         opener.retrieve(poster , f'photos/{id}.jpg')
    #     except Exception as e:
    #         print(e)
    
    # final_res = []
    # for r in res:
    #     r['poster'] = '/photos/full/' + r['imdb_id']
    #     final_res.append(r)

    return res

@router.get('/imgs/{imdb_id}')
async def get_all_images(imdb_id : str):
    res = movie.get_images(movie_id=imdb_id)
    return res
