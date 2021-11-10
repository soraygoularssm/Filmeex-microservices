from fastapi import APIRouter, HTTPException, Depends, status
from database.mongodb import db
from .models import Movie , MovieUpdate , Series , SeriesUpdate , Genre , MiniMovie , MiniSeries
from .service import get_cast_exist , add_genres , add_cast, get_cast , update_cast
from bson.objectid import ObjectId
from typing import List , Dict , Optional
from pydantic import Json
from .dependencies import GetQueryParams    

# MOVIE RELATED
movie_router = APIRouter()

@movie_router.get('/movies' , response_model = List[Movie])
async def get_movies(params: GetQueryParams = Depends()):
    movies_cursor = db.movieDb.find(params.q).skip(params.page).limit(params.limit).sort("rating",-1)
    movies = await movies_cursor.to_list(length=params.limit)
    movies = [Movie(**movie) for movie in movies]
    print(len(movies))
    return movies

@movie_router.get('/movies/{id}' , response_model=Movie)
async def get_movie(id:str):
    movie = await db.movieDb.find_one({'imdb_id' : id})
    if not movie:
        raise HTTPException(status_code=404, detail='movie does not exist')
    
    movie = Movie(**movie)
    return movie

@movie_router.post('/movies' ,  status_code=200)
async def add_movie(body: List[Movie]):
    not_existing_cast_ids = list()
    not_existing_cast = list()
    for movie in body:
        for star in movie.crew.stars:
            if not star.id in not_existing_cast_ids:
                cast_exist = await get_cast_exist(star.id)
                if cast_exist == False:
                    cast_info = {'imdb_id': star.id , 'actor':True , 'director':False , 'media': [movie.imdb_id]}
                    not_existing_cast.append(cast_info)
                    not_existing_cast_ids.append(star.id)
                else:
                    cast_info = dict()
                    if not movie.imdb_id in cast_exist['media']:   
                        cast_info['media'] = cast_exist['media'].append(movie.imdb_id)
                        await update_cast(star.id , cast_info)

        for director in movie.crew.directors:
            if not director in not_existing_cast_ids:
                cast_exist = await get_cast_exist(director)
                if cast_exist == False:
                    cast_info = {'imdb_id': director , 'actor':False , 'director':True , 'media': [movie.imdb_id]}
                    not_existing_cast.append(cast_info)
                    not_existing_cast_ids.append(director)
                else:
                    cast_info = dict()
                    cast_info['media'] = cast_exist['media'].append(movie.imdb_id)
                    await update_cast(director , cast_info)
        
    res_not_existing_cast = [] 
    [res_not_existing_cast.append(x) for x in not_existing_cast if x not in res_not_existing_cast] 
    if res_not_existing_cast:
        cast_data = await get_cast(res_not_existing_cast)
        if cast_data:
            cast_add = await add_cast(cast_data)
            if not cast_add:
                raise HTTPException(status_code=400, detail='Cannot add')

    try:
        genres_list_name = []
        genres_list_name_added = []
        genres_list = []
        for movie in body:
            genres_list_name = genres_list_name + [genre for genre in movie.genres]
            genres_list_name = list(set(genres_list_name))
            genres = []
            for mg in movie.genres:
                if not mg in genres_list_name_added:
                    genres.append(Genre(genre_name = mg).dict()) 
                    genres_list_name_added.append(mg)
        
            genres_list = genres_list + genres
        # print()
        # print(genres_list_name)
        # print()
        await add_genres(genres_list)

        await db.movieDb.insert_many([movie.dict() for movie in body])
        return {'detail':'movie successfully added'}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='movie already exists')

@movie_router.put('/movies' , status_code=200)
async def update_movies(body: MovieUpdate , id: Optional[str] = None):
    try:
        change = {k: v for k, v in body.dict().items() if v != None and v != [] }
        if id:
            await db.movieDb.update_one({'imdb_id' : id} , {'$set': change})
            return {'detail': 'movie successfully updated'}
        await db.movieDb.update_many({} , {'$set': change})
        return {'detail': 'all movies successfully updated'}
    except:
        raise HTTPException(status_code=400)
    
@movie_router.delete('/movies/{id}', status_code=204)
async def delete_movies(id:str):
    try:
        await db.movieDb.delete_one({'imdb_id': id})
        return None 
    except:
        raise HTTPException(status_code=404)


# SERIES RELATED
series_router = APIRouter()

@series_router.get('/series' ,  response_model=List[Series])
async def get_all_series(params: GetQueryParams = Depends()):
    series_cursor = db.seriesDb.find(params.q).skip(params.page).limit(params.limit).sort("rating",-1)
    return await series_cursor.to_list(length=params.limit)
    # all_series = [Series(**series) for series in all_series]

@series_router.get('/series/{id}' , response_model=Series)
async def get_series(id: str):
    series = await db.seriesDb.find_one({'imdb_id' : id})
    if not series:
            raise HTTPException(status_code=400, detail='series does not exist')
    
    series = Series(**series)
    return series

@series_router.post('/series' , status_code=200)
async def add_series(body: List[Series]):
    not_existing_cast_ids = list()
    not_existing_cast = list()
    for series in body:
        for star in series.crew.stars:
            if not star.id in not_existing_cast_ids:
                cast_exist = await get_cast_exist(star.id)
                if cast_exist == False:
                    cast_info = {'imdb_id': star.id , 'actor':True , 'creator':False , 'series': [series.imdb_id]}
                    not_existing_cast.append(cast_info)
                    not_existing_cast_ids.append(star.id)
                else:
                    cast_info = dict()
                    if not series.imdb_id in cast_exist['media']:   
                        cast_info['media'] = cast_exist['media'].append(series.imdb_id)
                        await update_cast(star.id , cast_info)

        # for director in series.crew.directors:
        #     if not director in not_existing_cast_ids:
        #         cast_exist = await get_cast_exist(director)
        #         if cast_exist == False:
        #             cast_info = {'imdb_id': director , 'actor':False , 'director':True , 'movies': [movie.imdb_id]}
        #             not_existing_cast.append(cast_info)
        #             not_existing_cast_ids.append(director)
        #         else:
        #             cast_info = dict()
        #             cast_info['movies'] = cast_exist['movies'].append(movie.imdb_id)
        #             await update_cast(director , cast_info)
        
    res_not_existing_cast = [] 
    [res_not_existing_cast.append(x) for x in not_existing_cast if x not in res_not_existing_cast] 
    if res_not_existing_cast:
        cast_data = await get_cast(res_not_existing_cast)
        if cast_data:
            cast_add = await add_cast(cast_data)
            if not cast_add:
                raise HTTPException(status_code=400, detail='Cannot add')

    try:
        genres_list_name = []
        genres_list_name_added = []
        genres_list = []
        for series in body:
            genres_list_name = genres_list_name + [genre for genre in series.genres]
            genres_list_name = list(set(genres_list_name))
            genres = []
            for mg in series.genres:
                if not mg in genres_list_name_added:
                    genres.append(Genre(genre_name = mg).dict()) 
                    genres_list_name_added.append(mg)
        
            genres_list = genres_list + genres
        # print()
        # print(genres_list_name)
        # print()
        await add_genres(genres_list)

        await db.seriesDb.insert_many([series.dict() for series in body])
        return {'detail':'series successfully added'}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='series already exists')

@series_router.put('/series' , status_code=200)
async def update_series(body: SeriesUpdate , id: Optional[str] = None):
    try:
        change = {k: v for k, v in body.dict().items() if v is not None}
        if db:
            series = await db.seriesDb.update_one({'imdb_id' : id} , {'$set': change})
            return {'detail': 'series successfully updated'}
        series = await db.seriesDb.update_one({} , {'$set': change})
        return {'detail': 'all series successfully updated'}
    except:
        raise HTTPException(status_code=400)
    
@series_router.delete('/series/{id}', status_code=204)
async def delete_series(id:str):
    try:
        await db.seriesDb.delete_one({'imdb_id': id})
        return None
    except:
        raise HTTPException(status_code=404)
