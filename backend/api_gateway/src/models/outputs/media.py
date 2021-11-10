from ..models.media import MovieModel , SeriesModel , MiniMediaModel , AllGenresModel , AllCategoriesModel
import pydantic2graphene
import graphene


class MovieConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = MovieModel

# class model
Movie = MovieConverter.as_class()

class SeriesConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = SeriesModel

# class model
Series = SeriesConverter.as_class()

class MiniMediaConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = MiniMediaModel

# class model
MiniMedia = MiniMediaConverter.as_class()

class AllGenresConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = AllGenresModel

# class model
AllGenres = AllGenresConverter.as_class()

class AllCategoriesConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = AllCategoriesModel

# class model
AllCategories = AllCategoriesConverter.as_class()
