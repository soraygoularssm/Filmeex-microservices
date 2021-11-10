from fastapi import APIRouter, HTTPException, Depends 
from database.mongodb import db
from .models import Category 
from typing import List

router = APIRouter()

@router.get('/categories', response_model=List[Category] ,  status_code = 200)
async def get_categories():
    categories_cursor = db.categoryDb.find()
    categories = await categories_cursor.to_list(length=20)
    categories = [Category(**category) for category in categories]
    return categories

@router.post('/categories')
async def add_categories(categories: List[Category] ,  status_code = 200):
    for category in categories:
        db.categoryDb.insert_one(category.dict())
    return {'detail':'done'}

@router.put('/categories/{category}' , status_code = 200)
async def update_category(category: str , change: Category):
    res = db.categoryDb.update_one({'category_name':category} , {'$set':change.dict()})
    if not res:
        raise HTTPException(status_code = 400 , detail = 'could not update the category')
    return {'detail': 'category successfully updated'}

@router.delete('/categories/{category}' , status_code = 204)
async def delete_category(category: str):
    res = db.categoryDb.delete_one({'category_name':category})
    if not res:
        raise HTTPException(status_code= 404)
    return None
