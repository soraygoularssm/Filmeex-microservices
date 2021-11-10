from ..models.cast import CastModel
import pydantic2graphene
import graphene

class CastConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = CastModel

Cast = CastConverter.as_class()
