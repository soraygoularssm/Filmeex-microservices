from ..models.users import UserUpdateModel , UserSubscriptionPlanModel , UserSubscriptionModel
from graphene_pydantic import PydanticInputObjectType

class UserSubscriptionPlanInput(PydanticInputObjectType):
    class Meta:
        model = UserSubscriptionPlanModel

class UserSubscriptionInput(PydanticInputObjectType):
    class Meta:
        model = UserSubscriptionModel

class UserUpdateInput(PydanticInputObjectType):
    class Meta:
        model = UserUpdateModel
        exclude_fields = ("id",)