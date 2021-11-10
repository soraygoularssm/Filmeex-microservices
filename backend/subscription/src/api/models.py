from pydantic import BaseModel
from typing import Optional
import datetime

class SubscriptionPlan(BaseModel):
    name: str
    days: int

class Subscription(BaseModel):
    plan: SubscriptionPlan
    expire_date: datetime.datetime
    price: int

class SubscriptionUpdate(BaseModel):
    plan: Optional[SubscriptionPlan] = None
    expire_date: Optional[datetime.datetime] = None
    price: Optional[int] = None