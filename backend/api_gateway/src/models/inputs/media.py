from ..models.media import MovieModel , MovieUpdateModel , SeriesModel , SeriesUpdateModel , RatingModel , CommentModel , CrewModel , PersonInModel , SourcesModel , UrlModel , SeasonModel , EpisodeModel
from graphene_pydantic import PydanticInputObjectType

# Mutaiton
class UrlInput(PydanticInputObjectType):
    class Meta:
        model = UrlModel

class PersonInInput(PydanticInputObjectType):
    class Meta:
        model = PersonInModel

class RatingInput(PydanticInputObjectType):
    class Meta:
        model = RatingModel

class CommentInput(PydanticInputObjectType):
    class Meta:
        model = CommentModel

class CrewInput(PydanticInputObjectType):
    class Meta:
        model = CrewModel

class PersonInInput(PydanticInputObjectType):
    class Meta:
        model = PersonInModel

class SourcesInput(PydanticInputObjectType):
    class Meta:
        model = SourcesModel

class EpisodeInput(PydanticInputObjectType):
    class Meta:
        model = EpisodeModel

class SeasonInput(PydanticInputObjectType):
    class Meta:
        model = SeasonModel

class MovieInput(PydanticInputObjectType):
    class Meta:
        model = MovieModel

class MovieUpdateInput(PydanticInputObjectType):
    class Meta:
        model = MovieUpdateModel

class SeriesInput(PydanticInputObjectType):
    class Meta:
        model = SeriesModel

class SeriesUpdateInput(PydanticInputObjectType):
    class Meta:
        model = SeriesUpdateModel