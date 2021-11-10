import uuid
from typing import List, Optional, TypeVar
import datetime

from pydantic import UUID4, BaseModel, EmailStr, validator

class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={"id", "is_superuser", "is_active", "oauth_accounts"},
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})

class BaseUser(CreateUpdateDictModel):
    """Base User model."""

    id: Optional[UUID4] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

class UserSubscriptionPlan(BaseModel):
    name: str
    days: int

class UserSubscription(BaseModel):
    plan: UserSubscriptionPlan
    exp_date: datetime.date

class User(BaseUser):
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

class BaseUserUpdate(BaseUser):
    password: Optional[str]

class UserUpdate(User, BaseUserUpdate):
    name: Optional[str]
    devices: Optional[List[str]]
    subscription: Optional[UserSubscription]
    following: Optional[List[str]]
    archived: Optional[List[str]]
    loved: Optional[List[str]]
    watch_history: Optional[List[str]]