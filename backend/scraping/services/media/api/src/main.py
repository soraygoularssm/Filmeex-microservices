from fastapi import FastAPI
from .tools.retriver import retrive_data

app = FastAPI()

@app.get('/movies')
async def get_movies(start: int , end: int):
    meta = {'page_counter' : end}

    if start > 1:
        movies_url = f'https://www.film2serial.ir/category/%d9%81%db%8c%d9%84%d9%85/%d8%ae%d8%a7%d8%b1%d8%ac%db%8c/page/{start}' 
    else:
        movies_url = 'https://www.film2serial.ir/category/%d9%81%db%8c%d9%84%d9%85/%d8%ae%d8%a7%d8%b1%d8%ac%db%8c' 

    movies = retrive_data(movies_url,'parse', 'movies' , meta = meta)

    return movies

@app.get('/animations')
async def get_series(start: int, end: int):
    meta = {'page_counter' : end}

    if start > 1:
        animations_url = f'https://my-film.pw/animation/animation-movie/page/{start}'
    else:
        animations_url = f'https://my-film.pw/animation/animation-movie'

    animations = retrive_data(animations_url , 'parse' , 'animations' ,  meta=meta)

    return animations

@app.get('/series')
async def get_series(start: int, end: int):
    meta = {'page_counter' : end}

    if start > 1:
        series_url = f'https://my-film.pw/series/page/{start}'
    else:
        series_url = f'https://my-film.pw/series'

    series = retrive_data(series_url , 'parse' , 'series' ,  meta=meta)

    return series
