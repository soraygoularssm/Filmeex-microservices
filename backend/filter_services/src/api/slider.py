from fastapi import APIRouter, HTTPException, Depends
from database.mongodb import db
from .models import Slider
from typing import List
from pydantic import Json

router = APIRouter()


@router.get('/sliders', response_model=List[Slider], status_code=200)
async def get_sliders(condition: Json = {}):
    sliders_cursor = db.sliderDb.find(condition)
    sliders = await sliders_cursor.to_list(length=50)
    sliders = [Slider(**slider) for slider in sliders]
    return sliders


@router.post('/sliders')
async def add_sliders(sliders: List[Slider],  status_code=200):
    for slider in sliders:
        slider.slider_exp_date = slider.slider_exp_date.strftime("%Y-%m-%d")

        db.sliderDb.insert_one(slider.dict())
    return {'detail': 'done'}


@router.put('/sliders/{slider}', status_code=200)
async def update_slider(slider: str, change: Slider):
    res = db.sliderDb.update_one({'slider_name': slider}, {
                                 '$set': change.dict()})
    if not res:
        raise HTTPException(
            status_code=400, detail='could not update the slider')

    return {'detail': 'slider successfully updated'}


@router.delete('/sliders/{slider}', status_code=204)
async def delete_slider(slider: str):
    res = db.sliderDb.delete_one({'slider_name': slider})
    if not res:
        raise HTTPException(
            status_code=404)

    return None
