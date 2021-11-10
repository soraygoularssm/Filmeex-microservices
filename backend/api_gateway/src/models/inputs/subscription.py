from ..models.subscription import SubscriptionModel , SubscriptionPlanModel
from graphene_pydantic import PydanticInputObjectType

class SubscriptionPlanInput(PydanticInputObjectType):
    class Meta:
        model = SubscriptionPlanModel
        
class SubscriptionInput(PydanticInputObjectType):
    class Meta:
        model = SubscriptionModel