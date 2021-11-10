from fastapi import APIRouter, HTTPException, Depends, status
from database.mongodb import db
from .models import Genre 
from typing import List

router = APIRouter()

@router.get('/genres', response_model=List[Genre] , status_code = 200)
async def get_genres():
    genres_cursor = db.genreDb.find()
    genres = await genres_cursor.to_list(length=30)
    genres = [Genre(**genre) for genre in genres]
    return genres

@router.post('/genres',status_code = 200)
async def add_genres(genres: List[Genre]):
    for genre in genres:
        try:
            await db.genreDb.insert_one(genre.dict())
        except:
            pass
    return None

@router.put('/genres/{genre}' , status_code = 200)
async def update_genre(genre: str , change: Genre):
    res = await   db.genreDb.update_one({'genre_name':genre} , {'$set':change.dict()})
    if not res:
        raise HTTPException(status_code = 400 , detail = 'could not update the genre')
    return {'detail': 'genre successfully updated'}

@router.delete('/genres' , status_code = 204)
async def delete_genre(genre: str):
    res = await db.genreDb.delete_one({'genre_name':genre})
    if not res:
        raise HTTPException(status_code= 404)
    return None
