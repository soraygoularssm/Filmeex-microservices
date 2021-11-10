from . import communicator
import time
import random

async def _prime_media_list(content_type,start):
    media_list = list()
    media_mixed = communicator.get_five_pages(content_type , start)

    for med in media_mixed:
        imdb_id = med['imdb_id']
        media_list.append(imdb_id)
    
    media_list = await communicator.remove_existing_media(content_type , media_list)
    media = list()
    if media_list:
        for med in media_mixed:
            if med['imdb_id'] in media_list:
                media.append(med)
    return media , media_list
async def _latter_media_list(media_list , tv = False):
    media_imdb = communicator.get_five_pages_imdb_info(media_list , tv=tv)
    return media_imdb
def _get_subtitles(media_imdb):
    sub_inputs = [{'name':movie['name'] , 'year': int(movie['year'])} for movie in media_imdb if movie['name'] and movie['year']]
    subtitles = communicator.get_five_pages_subtitles(sub_inputs)
    return subtitles
    
def _get_all_media(media , media_imdb , subtitles = None):
    all_media = []

    for med in media:
        for med_imdb in media_imdb:
            if med['imdb_id'] == med_imdb['imdb_id']:
                combinded_movie = {**med , **med_imdb}

                try:
                    for subtitle in subtitles:
                        try:
                            if subtitle['imdb_id'] == combinded_movie['imdb_id']:
                                combinded_movie = {**combinded_movie , **subtitle}
                        except:
                            pass
                except:
                    pass

                all_media.append(combinded_movie)
    return all_media

async def get5_movies(start):
    content_type = 'movies'
    movies , movies_list = await _prime_media_list(content_type , start)
    movies_imdb = await _latter_media_list(movies_list)
    if movies:
        subtitles = _get_subtitles(movies_imdb)
    all_movies = _get_all_media(movies , movies_imdb)
    return await communicator.add_five_pages_movie(content_type , all_movies)

async def get5_series(start):
    content_type = 'series'
    series , series_list = await _prime_media_list(content_type , start)
    series_imdb = await _latter_media_list(series_list , tv = True)
    # if series:
    #     subtitles = _get_subtitles(series_imdb)
    all_series = _get_all_media(series , series_imdb)
    return await communicator.add_five_pages_movie(content_type , all_series)

async def get5_animations(start):
    content_type = 'animations'
    animations , animations_list = await _prime_media_list(content_type , start)
    animations_imdb = await _latter_media_list(animations_list)
    if animations:
        subtitles = _get_subtitles(animations_imdb)
    all_animations = _get_all_media(animations , animations_imdb)
    return await communicator.add_five_pages_movie(content_type , all_animations)
