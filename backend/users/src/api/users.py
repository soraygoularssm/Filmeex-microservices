from fastapi import APIRouter, HTTPException, Depends, status , Header
from .models import User , UserUpdate
from typing import List
from database.mongodb import db
import datetime
import uuid
from bson.binary import Binary, UUID_SUBTYPE

router = APIRouter()

@router.get('/users', response_model=List[User])
async def get_users(limit: int = 1000, page: int = 1):
    users_cursor = db.usersDb.find({}).skip((page - 1) * limit).limit(limit)
    users = await users_cursor.to_list(length=limit)
    return users

@router.get('/users/{id}', response_model=User)
async def get_user(id: str):
    id=uuid.UUID(id).bytes
    user = await db.usersDb.find_one({'id': Binary(bytes(bytearray(id)), UUID_SUBTYPE)})
    return user

@router.put('/users/{id}' , status_code=200)
async def update_user(id: str , body: UserUpdate):
    try:
        id=uuid.UUID(id).bytes
        change = {k: v for k, v in body.dict().items() if v != None and v != []}
        del change['id']
        await db.usersDb.update_one({'id' : Binary(bytes(bytearray(id)), UUID_SUBTYPE)} , {'$set': change})
        return {'detail': 'stars successfully updated'}
    except:
        raise HTTPException(status_code=400, detail="couldn't update")

@router.delete('/users/{id}', status_code=204)
async def delete_cast(id:str):
    try:
        id=uuid.UUID(id).bytes
        # await db.usersDb.delete_one({'id': Binary(bytes(bytearray(id)), UUID_SUBTYPE)})
        await db.usersDb.delete_many({})
        return None
    except:
        raise HTTPException(status_code=404)