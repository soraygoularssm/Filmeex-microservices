from fastapi import APIRouter , HTTPException , Depends
from services import media , cast , users , discovery , subscription , filters
import httpx
from pydantic import Json
from .models import Body
from .dependencies import GetQueryParams
import json
from auth import security
from typing import Optional

# must be removed later
router = APIRouter()

def url_discovery(service):
    serv = httpx.get(f'http://discovery_service:8007/discovery/services/{service}')
    serv = json.loads(serv.text)['url']
    return serv

try:
    users_url = url_discovery('users')
    media_url = url_discovery('media')
    cast_url = url_discovery('cast')
    filters_url = url_discovery('filters')
    subscription_url = url_discovery('subscription')
except:
    pass

@router.get('/home')
async def get_home():
    home_page = dict()
    async with httpx.AsyncClient(base_url=filters_url) as client:
        categories = await filters.categories_get(client)
        home_page['categories'] = categories

        genres = await filters.genres_get(client)
        home_page['genres'] = genres

        sliders = await filters.sliders_get(client)
        home_page['sliders'] = sliders

    # async with httpx.AsyncClient(base_url=users_url) as client:
    #     await users.users_get_one(client , user , False)
    
    movies = list()
    async with httpx.AsyncClient(base_url=media_url) as client:
        for genre in genres:
            genre = genre['genre_name']
            condition = {"genres": { "$in":[genre] }}
            condition = json.dumps(condition)
            payload = {'q': condition}
            movie = await media.movies_get(client, payload)
            if movie:
                movie = movies.append(movie[0])

    home_page['movies'] = movies
    return home_page

# MOVIE
@router.get('/movies')
async def get_movies(params: GetQueryParams = Depends()):
    async with httpx.AsyncClient(base_url=media_url) as client:
        return await media.movies_get(client, params.payload)

@router.get('/movies/{id}')
async def get_movies(id: str , logged: bool = Depends(security.is_logged) , subscription: bool = Depends(security.is_subscribed)):
    async with httpx.AsyncClient(base_url=media_url) as client:
        res = await media.movies_get_one(client, id)
    if logged:
        if not res['free']:
            if not subscription:
                del res['sources']
    else:
        del res['sources']
        
    return res

@router.put('/movies/{id}' , status_code=200)
async def put_movies(id: str, body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await media.movies_put(client, id, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'updated': res}

# SERIES
@router.get('/series')
async def get_series(params: GetQueryParams = Depends()):
    async with httpx.AsyncClient(base_url=media_url) as client:
        return await media.series_get(client, params.payload)

@router.get('/series/{id}')
async def get_series(id: str , logged: bool = Depends(security.is_logged) , subscription: bool = Depends(security.is_subscribed)):
    async with httpx.AsyncClient(base_url=media_url) as client:
        res = await media.series_get_one(client, id)
    if logged:
        if not res['free']:
            if not subscription:
                for se in res['seasons']:
                    for ep in se['episodes']:
                        del ep['sources']
    else:
        del res['movie_sources']
    return res

@router.put('/series/{id}')
async def put_series(id: str , body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await media.series_put(client, id, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'updated': res}


# STARS
@router.get('/stars')
async def get_stars(condition: Json = {}, limit: int = None, page: int = None):
    condition = json.dumps(condition)
    payload = {
        'condition': condition
    }
    if limit:
        payload.update({'limit': limit})
    if page:
        payload.update({'page': page})
    async with httpx.AsyncClient(base_url=cast_url) as client:
        return await cast.cast_get(client , payload)

# DIRECTORS
@router.get('/directors')
async def get_directors(condition: Json = {}, limit: int = None, page: int = None):
    condition = json.dumps(condition)
    payload = {
        'condition': condition
    }
    if limit:
        payload.update({'limit': limit})
    if page:
        payload.update({'page': page})
    async with httpx.AsyncClient(base_url=cast_url) as client:
        return await cast.cast_get(client , payload)

# CAST
@router.get('/cast/{id}')
async def get_directors(id: str):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        return await cast.cast_get_one(client, id)

# SUBSCRIPTION
@router.get('/subscriptions')
async def subscriptions():
    async with httpx.AsyncClient(base_url=subscription_url) as client:
        return await subscription.subscriptions_get(client)