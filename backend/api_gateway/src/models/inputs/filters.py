from ..models.filters import GenreModel , CategoryModel , SlideModel , SliderModel , MediaSlideModel , GenreModel , CastSlideModel
import pydantic2graphene
import graphene

from graphene_pydantic import PydanticInputObjectType

class GenreConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = GenreModel

# Mutaiton
GenreInput = GenreConverter.as_class(graphene.InputObjectType)

class CategoryConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = GenreModel

# Mutaiton
CategoryInput = CategoryConverter.as_class(graphene.InputObjectType)


# Mutaiton
class CastSlideInput(PydanticInputObjectType):
    class Meta:
        model = CastSlideModel

class GenreInput(PydanticInputObjectType):
    class Meta:
        model = GenreModel

class MediaSlideInput(PydanticInputObjectType):
    class Meta:
        model = MediaSlideModel

class SlideInput(PydanticInputObjectType):
    class Meta:
        model = SlideModel

class SliderInput(PydanticInputObjectType):
    class Meta:
        model = SliderModel
