from ..models.users import UserModel
import pydantic2graphene
import graphene

class UserConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = UserModel

User = UserConverter.as_class()
