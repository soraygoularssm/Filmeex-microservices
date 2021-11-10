from .dependencies import *
import graphene
import httpx
from services import media, cast, filters, subscription, suggestions , users
from graphene.types.generic import GenericScalar
import json
from models import Movie, MovieModel, MiniMediaModel, MiniMedia, MovieUpdateModel, MovieInput, MovieUpdateInput, Series, SeriesModel, SeriesUpdateModel, SeriesInput, SeriesUpdateInput, Cast, CastModel, CastUpdateModel, CastInput, CastUpdateInput, Subscription, SubscriptionModel, SubscriptionInput, AllGenres, AllCategories
from models import Genre, GenreModel, GenreInput, Category, CategoryModel, CategoryInput, Slider, SliderModel, SliderInput, AllGenresModel, UserModel, UserUpdateModel, UserUpdateInput, User


def url_discovery(service):
    serv = httpx.get(
        f'http://discovery_service:8000/discovery/services/{service}')
    serv = json.loads(serv.text)['url']
    return serv


class Query(graphene.ObjectType):
    users = graphene.List(User, id=graphene.String(required=False, default_value=""), limit=graphene.Int(
        required=False, default_value=50), page=graphene.Int(required=False, default_value=1))

    async def resolve_users(parent, info, id, limit, page):
        current_user = info.context['request'].state.user

        if current_user:
            if current_user.is_superuser:
                if id:
                    async with httpx.AsyncClient(base_url=url_discovery('users')) as client:
                        user = await users.users_get_one(client, id)
                    user = [UserModel(**user)]
                    return user
                else:
                    QueryParameters = GetQueryParams({}, page=page, limit=limit)
                    payload = QueryParameters.payload
                    async with httpx.AsyncClient(base_url=url_discovery('users')) as client:
                        users_list = await users.users_get(client, payload)
                    users_list = [UserModel(**user) for user in users_list]
                    return users_list
            else:
                async with httpx.AsyncClient(base_url=url_discovery('users')) as client:
                    user = await users.users_get_one(client, current_user.id)
                user = [UserModel(**user)]
                return user

    movies = graphene.List(Movie, ids=graphene.List(graphene.String, required=False, default_value=[]), condition=GenericScalar(required=False, default_value={}), limit=graphene.Int(
        required=False, default_value=50), page=graphene.Int(required=False, default_value=1))

    async def resolve_movies(parent, info, ids, condition, limit, page):
        user = info.context['request'].state.user

        is_subscribed = False
        if user:
            if user.subscription:
                is_subscribed = True

        if ids:
            condition = {'imdb_id': {'$in': ids}}
            limit = len(ids)
            QueryParameters = GetQueryParams(condition, page=page, limit=limit)
        else:
            try:
                c = condition
                genres = c['genres']['in']
                animations = False
                for genre in genres:
                    if genre == 'انیمیشن':
                        animations = True
                c = json.dumps(c, ensure_ascii=False)
                c = c.replace('"in":', '"$in":')
                if not animations:
                    c = c + ' , {"genres": {"$nin": ["انیمیشن"]}}'
                    c = '{ "$and" : [' + c + ']}'
                c = json.loads(c)
                QueryParameters = GetQueryParams(c, page=page, limit=limit)
            except:
                QueryParameters = GetQueryParams({}, page=page, limit=limit)

        payload = QueryParameters.payload
        async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
            movies_list = await media.movies_get(client, payload)

            # if not is_subscribed:
            #     for movie_info in movies_list:
            #         if not movie_info['free']:
            #             del movie_info['sources']

        movies_list = [MovieModel(**movie_info) for movie_info in movies_list]
        return movies_list

    all_genres = graphene.List(AllGenres, content_type=graphene.String(
        required=False, default_value="movie"))

    async def resolve_all_genres(parent, info, content_type):
        all_genres = []
        async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
            genres_list = await filters.genres_get(client)
        genres_list = [GenreModel(**genre_info) for genre_info in genres_list]

        for genre in genres_list:
            if genre.genre_name == "انیمیشن":
                QueryParameters = GetQueryParams(
                    {'genres': {'$in': [genre.genre_name]}}, limit=15)
            else:
                QueryParameters = GetQueryParams({"$and": [{'genres': {'$in': [genre.genre_name]}}, {
                                                 "genres": {"$nin": ["انیمیشن"]}}]}, limit=15)
            payload = QueryParameters.payload

            async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                if content_type == 'movie':
                    movies_list = await media.movies_get(client, payload)
                    all_genres.append(
                        {'name': genre.genre_name, 'media': movies_list})
                elif content_type == 'series':
                    series_list = await media.series_get(client, payload)
                    all_genres.append(
                        {'name': genre.genre_name, 'media': series_list})

        all_genres = [AllGenresModel(**genre) for genre in all_genres]

        return all_genres

    series = graphene.List(Series, condition=GenericScalar(required=False, default_value={}), limit=graphene.Int(
        required=False, default_value=50), page=graphene.Int(required=False, default_value=1))

    async def resolve_series(parent, info, condition, limit, page):
        try:
            c = condition
            genres = c['genres']['in']
            animations = False
            for genre in genres:
                if genre == 'انیمیشن':
                    animations = True
            c = json.dumps(c, ensure_ascii=False)
            c = c.replace('"in":', '"$in":')
            if not animations:
                c = c + ' , {"genres": {"$nin": ["انیمیشن"]}}'
                c = '{ "$and" : [' + c + ']}'
            c = json.loads(c)
            QueryParameters = GetQueryParams(c, page=page, limit=limit)
        except:
            QueryParameters = GetQueryParams({}, page=page, limit=limit)

        payload = QueryParameters.payload

        async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
            series_list = await media.series_get(client, payload)

        series_list = [SeriesModel(**series_info)
                       for series_info in series_list]
        return series_list

    suggestions = graphene.List(MiniMedia, id=graphene.String(required=True))

    async def resolve_suggestions(parent, info, id):
        async with httpx.AsyncClient(base_url=url_discovery('suggestions')) as client:
            suggestions_list = await suggestions.suggestions_get(client, id)
        suggestions_list = [MiniMediaModel(
            **suggestion_info) for suggestion_info in suggestions_list]
        return suggestions_list

    cast = graphene.List(Cast, ids=graphene.List(graphene.String, required=False, default_value=[]), condition=GenericScalar(required=False, default_value={}), limit=graphene.Int(
        required=False, default_value=50), page=graphene.Int(required=False, default_value=1))

    async def resolve_cast(parent, info, ids, condition, limit, page):
        if ids:
            condition = {'imdb_id': {'$in': ids}}
        QueryParameters = GetQueryParams(condition, page=page, limit=limit)
        payload = QueryParameters.payload
        async with httpx.AsyncClient(base_url=url_discovery('cast')) as client:
            cast_list = await cast.cast_get(client, payload)

        cast_list = [CastModel(**cast_info) for cast_info in cast_list]
        return cast_list

    genres = graphene.List(Genre, condition=GenericScalar(required=False, default_value={}), limit=graphene.Int(
        required=False, default_value=50), page=graphene.Int(required=False, default_value=1))

    async def resolve_genres(parent, info, condition, limit, page):
        async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
            genres_list = await filters.genres_get(client)
        genres_list = [GenreModel(**genre_info) for genre_info in genres_list]
        return genres_list

    categories = graphene.List(Category)

    async def resolve_categories(parent, info):
        async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
            categories_list = await filters.categories_get(client)
        categories_list = [CategoryModel(**category_info)
                           for category_info in categories_list]
        return categories_list

    sliders = graphene.List(Slider, condition=GenericScalar(
        required=False, default_value={}))

    async def resolve_sliders(parent, info, condition):
        c = condition
        c = json.dumps(c, ensure_ascii=False)
        c = c.replace('"in":', '"$in":')
        c = json.loads(c)
        QueryParameters = GetQueryParams(c)
        payload = QueryParameters.payload
        async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
            sliders_list = await filters.sliders_get(client, payload)
        sliders_list = [SliderModel(**slider_info)
                        for slider_info in sliders_list]
        return sliders_list

    subscriptions = graphene.List(Subscription)

    async def resolve_subscriptions(parent, info):
        async with httpx.AsyncClient(base_url=url_discovery('subscription')) as client:
            subscription_list = await subscription.subscriptions_get(client)
        subscription_list = [SubscriptionModel(
            **subscription_info) for subscription_info in subscription_list]
        return subscription_list

# Mutation
class UpdateUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=False,default_value="")
        user_input = UserUpdateInput()

    @staticmethod
    async def mutate(parent, info, id, user_input):
        user = info.context['request'].state.user
        if user:
            if id:
                if user.is_superuser or id == user.id:
                    userModel = UserUpdateModel(**user_input)
                    async with httpx.AsyncClient(base_url=url_discovery('users')) as client:
                        status = await users.users_put(client, id, userModel.dict())
                    return dict(ok=status)
            else:
                userModel = UserUpdateModel(**user_input)
                userModel = userModel.dict()
                del userModel['id']
                async with httpx.AsyncClient(base_url=url_discovery('users')) as client:
                    status = await users.users_put(client, user.id , userModel)
                return dict(ok=status)
        return dict(ok=False)

class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user

        if user:
            if user.is_superuser or id == user.id:
                async with httpx.AsyncClient(base_url=url_discovery('users')) as client:
                    status = await users.users_delete(client, id)
                return dict(ok=status)
        return dict(ok=False)


class CreateMovie(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        movie_input = MovieInput()

    @staticmethod
    async def mutate(parent, info, movie_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                movieModel = MovieModel(**movie_input)
                async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                    status = await media.movies_post(client, movieModel.dict())

                return dict(ok=status)
        return dict(ok=False)

class UpdateMovie(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()
        movie_input = MovieUpdateInput()

    @staticmethod
    async def mutate(parent, info, id, movie_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                movieModel = MovieUpdateModel(**movie_input)
                async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                    status = await media.movies_put(client, id, movieModel.dict())
                    return dict(ok=status)
            else:
                if movie_input['likes']:
                    movieModel = MovieUpdateModel(likes=movie_input['likes'])
                    async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                        status = await media.movies_put(client, id, movieModel.dict())
                        return dict(ok=status)
                elif movie_input['dislikes']:
                    movieModel = MovieUpdateModel(
                        dislikes=movie_input['dislikes'])
                    async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                        status = await media.movies_put(client, id, movieModel.dict())
                        return dict(ok=status)
        return dict(ok=False)

class DeleteMovie(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                    status = await media.movies_delete(client, id)

                return dict(ok=status)
        return dict(ok=False)


class CreateSeries(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        series_input = SeriesInput()

    @staticmethod
    async def mutate(parent, info, series_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                seriesModel = SeriesModel(**series_input)
                async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                    status = await media.series_post(client, seriesModel.dict())

                return dict(ok=status)
        return dict(ok=False)

class UpdateSeries(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()
        series_input = SeriesUpdateInput()

    @staticmethod
    async def mutate(parent, info, id, series_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                seriesModel = SeriesUpdateModel(**series_input)
                async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                    status = await media.series_put(client, id, seriesModel.dict())
                return dict(ok=status)
            else:
                if movie_input['likes']:
                    movieModel = SeriesUpdateModel(likes=movie_input['likes'])
                    async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                        status = await media.series_put(client, id, seriesModel.dict())
                    return dict(ok=status)
                elif movie_input['dislikes']:
                    movieModel = SeriesUpdateModel(
                        dislikes=movie_input['dislikes'])
                    async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                        status = await media.series_put(client, id, seriesModel.dict())
                    return dict(ok=status)
        return dict(ok=False)

class DeleteSeries(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                async with httpx.AsyncClient(base_url=url_discovery('media')) as client:
                    status = await media.movies_delete(client, id)

                return dict(ok=status)
        return dict(ok=False)


class CreateCast(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        cast_input = CastInput()

    output = ok

    @staticmethod
    async def mutate(parent, info, cast_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                castModel = CastModel(**cast_input)
                async with httpx.AsyncClient(base_url=url_discovery('cast')) as client:
                    status = await cast.cast_post(client, [castModel.dict()])

                return dict(ok=status)
        return dict(ok=False)

class UpdateCast(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()
        cast_input = CastUpdateInput()

    @staticmethod
    async def mutate(parent, info, id, cast_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                castModel = CastUpdateModel(**cast_input)
                async with httpx.AsyncClient(base_url=url_discovery('cast')) as client:
                    status = await cast.cast_put(client, id, castModel.dict())
                return dict(ok=status)
            else:
                if cast_input['followers']:
                    castModel = CastUpdateModel(
                        followers=cast_input['followers'])
                    async with httpx.AsyncClient(base_url=url_discovery('cast')) as client:
                        status = await cast.cast_put(client, id, castModel.dict())
                    return dict(ok=status)
        return dict(ok=False)

class DeleteCast(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                async with httpx.AsyncClient(base_url=url_discovery('cast')) as client:
                    status = await cast.cast_delete(client, id)

                return dict(ok=status)
        return dict(ok=False)


class CreateSubscription(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        subscription_input = SubscriptionInput()

    output = ok

    @staticmethod
    async def mutate(parent, info, subscription_input):
        user = info.context['request'].state.user
        if user:
            subscriptionModel = SubscriptionModel(**subscription_input)
            async with httpx.AsyncClient(base_url=url_discovery('subscription')) as client:
                status = await subscription.subscription_post(client, [subscriptionModel.dict()])

            return dict(ok=status)
        return dict(ok=False)

class DeleteSubscription(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                async with httpx.AsyncClient(base_url=url_discovery('subscription')) as client:
                    status = await subscription.subscription_delete(client, id)

                return dict(ok=status)
        return dict(ok=False)


class CreateCategory(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        category_input = CategoryInput()

    output = ok

    @staticmethod
    async def mutate(parent, info, category_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                categoryModel = CategoryModel(**category_input)
                async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
                    status = await filters.categories_post(client, [categoryModel.dict()])

                return dict(ok=status)
        return dict(ok=False)

class DeleteCategory(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
                    status = await filters.categories_delete(client, id)

                return dict(ok=status)
        return dict(ok=False)


class CreateGenre(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        genre_input = GenreInput()

    output = ok

    @staticmethod
    async def mutate(parent, info, genre_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                genreModel = GenreModel(**genre_input)
                async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
                    status = await filters.genres_post(client, [genreModel.dict()])

                return dict(ok=status)
        return dict(ok=False)

class DeleteGenre(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
                    status = await filters.genres_delete(client, id)

                return dict(ok=status)
        return dict(ok=False)


class CreateSlider(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        slider_input = SliderInput()

    output = ok

    @staticmethod
    async def mutate(parent, info, slider_input):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                sliderModel = SliderModel(**slider_input)
                async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
                    status = await filters.sliders_post(client, [sliderModel.dict()])

                return dict(ok=status)
        return dict(ok=False)

class DeleteSlider(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()

    @staticmethod
    async def mutate(parent, info, id):
        user = info.context['request'].state.user
        if user:
            if user.is_superuser:
                async with httpx.AsyncClient(base_url=url_discovery('filters')) as client:
                    status = await filters.sliders_delete(client, id)

                return dict(ok=status)
        return dict(ok=False)


class Mutation(graphene.ObjectType):
    UpdateUser = UpdateUser.Field()
    DeleteUser = DeleteUser.Field()

    createMovie = CreateMovie.Field()
    updateMovie = UpdateMovie.Field()
    deleteMovie = DeleteMovie.Field()

    createSeries = CreateMovie.Field()
    updateSeries = UpdateMovie.Field()
    deleteSeries = DeleteMovie.Field()

    createCast = CreateCast.Field()
    updateCast = UpdateCast.Field()
    deleteCast = DeleteCast.Field()

    createSubscription = CreateSubscription.Field()
    deleteSubscription = DeleteSubscription.Field()

    createCategory = CreateCategory.Field()
    deleteCategory = DeleteCategory.Field()

    createGenre = CreateGenre.Field()
    deleteGenre = DeleteGenre.Field()

    createSlider = CreateSlider.Field()
    deleteSlider = DeleteSlider.Field()
