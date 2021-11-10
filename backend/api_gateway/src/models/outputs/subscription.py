from ..models.subscription import SubscriptionModel
import pydantic2graphene
import graphene

class SubscriptionConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = SubscriptionModel

Subscription = SubscriptionConverter.as_class()
