from fastapi import APIRouter, HTTPException
from .models import Coupon
from database.mongodb import db
import datetime
from typing import List

router = APIRouter()


@router.get('/coupons', response_model=List[Coupon], status_code=200)
async def get_coup():
    coupons_cursor = db.couponDb.find({})
    coupons = await coupons_cursor.to_list()
    coupons = [Coupon(**coupon) for coupon in coupons]
    if not coupons:
        HTTPException(status_code=400, detail='Coupons not found')
    return coupons


@router.get('/coupons/{name}', response_model=Coupon, status_code=200)
async def get_one_coup(name: str):
    coup = await db.couponDB.find_one({'name': name})
    if not coup:
        HTTPException(status_code=404)
    coupon = Coupon(**coup)
    return coupon


@router.post('/couposn', status_code=200)
async def add_coup(coupon: Coupon):
    if coupon.expires_at < datetime.date.today():
        raise HTTPException(
            status_code=400, detail='expiration time has passed')

    await db.couponDb.insert_one(coupon.dict())

    return {'detail': 'coupon successfully added'}


@router.delete('/coupons/{name}', status_code=204)
async def delete_coup(name: str):
    try:
        await db.couponDb.delete_one({'name': name})
    except:
        raise HTTPException(status_code=404)
    return None
