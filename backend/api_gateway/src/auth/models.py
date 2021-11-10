from fastapi_users import models
import datetime
from pydantic import BaseModel, validator
from typing import Optional,List

class UserSubscriptionPlan(BaseModel):
    name: str
    days: int

class UserSubscription(BaseModel):
    plan: UserSubscriptionPlan
    exp_date: datetime.date

class User(models.BaseUser):
    name: Optional[str] = None
    devices: Optional[List[str]] = []
    subscription: Optional[UserSubscription] = None
    register_date: Optional[str] = None
    following: Optional[List[str]] = ['']
    archived: List[str] = ['']
    loved: List[str] = ['']
    watch_history: List[str] = []

    @validator("register_date", pre=True, always=True)
    def default_register_date(cls,v):
        return datetime.datetime.now().strftime("%Y-%m-%d")

class UserCreate(models.BaseUserCreate):
    pass

class UserUpdate(User, models.BaseUserUpdate):
    name: Optional[str]
    devices: Optional[List[str]]
    subscription: Optional[UserSubscription]
    following: Optional[List[str]]
    archived: Optional[List[str]]
    loved: Optional[List[str]]
    watch_history: Optional[List[str]]

class UserDB(User, models.BaseUserDB):
    pass