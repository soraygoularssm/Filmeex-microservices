from fastapi import APIRouter , HTTPException
from typing import List
from .models import Subscription , SubscriptionUpdate
from database.mongodb import db
from pydantic import Json

router = APIRouter()

@router.get('/plans' ,  response_model=List[Subscription])
async def get_subscription_plans():
    plans_cursor = db.subscriptionDb.find({}).sort('price',1)
    plans = await plans_cursor.to_list(length=50)
    # plans = [Subscription(**plan) for plan in plans]
    return plans

@router.post('/plans' ,  status_code=200)
async def add_subscription_plan(plan: Subscription):
    try:
        res = await db.subscriptionDb.insert_one()

        user_id = res.inserted_id
        user_id = str(user_id)

        return {'user_id': user_id}
    except:
        raise HTTPException(status_code=400,detail='plan already exists')

@router.put('/plans/{days}' , status_code=200)
async def update_subscription_plan(days: int ,body: SubscriptionUpdate):
    change = {k: v for k, v in body.dict().items() if v != None and v != []}
    plan_update = await db.subscriptionDb.update_one({},{'$set' : change})
    if not plan_update:
        raise HTTPException(status_code=400,detail='could not update the subscription plan')
    return {'detail': 'plan successfully updated'}

@router.delete('/plans/{days}' , status_code=200)
async def delete_subscription_plan(days: int):
    plan_delete = await db.subscriptionDb.delete_one({'days': days})
    if not plan_delete:
        raise HTTPException(status_code=404, detail="couldn't delete the plan")
    return {'detail': 'plan successfully deleted'}
