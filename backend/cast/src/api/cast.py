from fastapi import APIRouter, HTTPException, Depends, status
from database.mongodb import db
from .models import Cast , CastUpdate
from typing import List
from pydantic import Json

router = APIRouter()

class GetQueryParams:
    def __init__(self, q: Json, page: int = 1, limit: int = 50):
        self.q = q
        self.page = (page - 1) * limit
        self.limit = limit

# CAST RELATED
@router.get('/cast' , response_model=List[Cast] ,  status_code=200)
async def get_cast(params: GetQueryParams = Depends()):
    print(params.q)
    stars_cursor = db.castDb.find(params.q).skip(params.page).limit(params.limit)
    stars = await stars_cursor.to_list(length=params.limit)
    return stars

@router.get('/cast/{id}' , response_model=Cast , status_code = 200)
async def get_cast(id: str):
    stars = await db.castDb.find_one({'imdb_id': id})
    if not stars:
        raise HTTPException(status_code=404)
    return stars

@router.post('/cast' , status_code=200)
async def add_cast(body: List[Cast] , status_code=200):
    from pymongo.errors import BulkWriteError
    try:
        # import json
        # print(json.dumps([cast.dict() for cast in body]))
        res = await db.castDb.insert_many([cast.dict() for cast in body])
        return {'detail':'cast successfully added'}
    except BulkWriteError as e:
        print(e.details)
        raise HTTPException(status_code=400, detail='cast already exists')

@router.put('/cast/{id}' , status_code=200)
async def update_cast(id: str , body: CastUpdate):
    try:
        change = {k: v for k, v in body.dict().items() if v != None and v != []}
        stars = await db.castDb.update_one({'imdb_id' : id} , {'$set': change})
        return {'detail': 'stars successfully updated'}
    except:
        raise HTTPException(status_code=400, detail="couldn't update")

@router.delete('/cast/{id}', status_code=204)
async def delete_cast(id:str):
    try:
        await db.castDb.delete_one({'imdb_id': id})
        return None
    except:
        raise HTTPException(status_code=404)