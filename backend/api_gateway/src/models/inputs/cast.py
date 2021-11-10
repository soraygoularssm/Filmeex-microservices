from ..models.cast import CastModel , CastUpdateModel
import pydantic2graphene
import graphene

class CastConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = CastModel

# Mutaiton
CastInput = CastConverter.as_class(graphene.InputObjectType)


class CastUpdateConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = CastUpdateModel

# Mutaiton
CastUpdateInput = CastUpdateConverter.as_class(graphene.InputObjectType)
