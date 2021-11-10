from fastapi import APIRouter , Depends
import services
from .models import Body
from .dependencies import GetQueryParams
from auth import security
from pydantic import Json
import json
import httpx
from services import media , cast , users , discovery , subscription , filters

router = APIRouter()

# @router.get('/home')
# async def get_home():
#     pass

router = APIRouter()

# must be removed later
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
    coupons_url = url_discovery('coupons')
except:
    pass

# MOVIES
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
                del res['movie_sources']
    else:
        del res['movie_sources']
        
    return res

@router.post('/movies')
async def post_movies(body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await media.movies_post(client, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'added: {res}')
    return {'added': res}

@router.put('/movies/{id}' , status_code=200)
async def put_movies(id: str, body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await media.movies_put(client, id, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'updated': res}

@router.delete('/movies/{id}')
async def delete_movies(id: str):
    async with httpx.AsyncClient(base_url=media_url) as client:
        res = await media.movies_delete(client, id)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'deleted': res}

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

@router.post('/series')
async def post_series(body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await media.series_post(client, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'added: {res}')
    return {'added': res}

@router.put('/series/{id}')
async def put_series(id: str , body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await media.series_put(client, id, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'updated': res}

@router.delete('/series/{id}')
async def delete_series(id: str):
    async with httpx.AsyncClient(base_url=media_url) as client:
        res = await media.series_delete(client, id)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'deleted': res}

# STARS
@router.get('/stars')
async def get_stars(params: GetQueryParams = Depends()):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        return await cast.stars_get(client , params.payload)

@router.get('/stars/{id}')
async def get_stars(id: str):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        return await cast.stars_get_one(client, id)

@router.post('/stars')
async def post_stars(body: Body):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        payload = json.loads(body.data)
        res = await cast.stars_post(client, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'added: {res}')
    return {'added': res}

@router.put('/stars/{id}')
async def put_stars(id: str , body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await cast.stars_put(client, id, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'updated': res}

@router.delete('/stars/{id}')
async def delete_stars(id: str):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        res = await cast.delete_stars(client, id)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'deleted': res}

# DIRECTORS
@router.get('/directors')
async def get_directors(params: GetQueryParams = Depends()):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        return await cast.directors_get(client , params.payload)

@router.get('/directors/{id}')
async def get_directors(id: str):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        return await cast.directors_get_one(client, id)

@router.post('/directors')
async def post_directors(body: Body):
    async with httpx.AsyncClient(base_url=cast_url) as client:
        payload = json.loads(body.data)
        res = await cast.directors_post(client, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'added: {res}')
    return {'added': res}

@router.put('/directors/{id}')
async def put_directors(id: str , body: Body):
    async with httpx.AsyncClient(base_url=media_url) as client:
        payload = json.dumps(body.data)
        res = await cast.directors_put(client, id, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'updated: {res}')
    return {'updated': res}

@router.delete('/directors/{id}')
async def delete_directors(id: str):
    pass

# AUTO SCRAPING
@router.get('/scraping')
async def scraping():
    pass

# USERS
@router.get('/users')
async def get_users():
    async with httpx.AsyncClient(base_url=users_url) as client:
        return await users.users_get(client)

@router.get('/users/{id}')
async def get_users(id: str):
    async with httpx.AsyncClient(base_url=users_url) as client:
        return await users.users_get_one(client, id)

@router.post('/users')
async def post_users(body: Body):
    async with httpx.AsyncClient(base_url=users_url) as client:
            payload = body.data
            res = await media.movies_post(client, payload)
    if res == False:
        raise HTTPException(status_code=400, detail= f'added: {res}')
    return {'added': res}

@router.put('/users/{id}')
async def put_users(id: str):
    pass

@router.delete('/users/{id}')
async def delete_users(id: str):
    pass