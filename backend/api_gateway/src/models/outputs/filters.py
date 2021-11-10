from ..models.filters import GenreModel , CategoryModel , SliderModel
import pydantic2graphene
import graphene

class GenreConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = GenreModel

Genre = GenreConverter.as_class()

class CategoryConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = CategoryModel

Category = CategoryConverter.as_class()

class SliderConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = SliderModel

Slider = SliderConverter.as_class()
