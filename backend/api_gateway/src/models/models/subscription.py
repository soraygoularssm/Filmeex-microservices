from pydantic import BaseModel
from typing import Optional
import datetime

class SubscriptionPlanModel(BaseModel):
    name: str
    days: int

class SubscriptionModel(BaseModel):
    plan: SubscriptionPlanModel
    expire_date: datetime.datetime
    price: int
