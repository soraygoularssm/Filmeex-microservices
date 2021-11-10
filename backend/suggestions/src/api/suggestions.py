import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from fastapi import APIRouter, Query, HTTPException
from database.mongodb import db
from .models import MiniMedia
from typing import List
import json
from bson.binary import Binary, UUID_SUBTYPE
import uuid

router = APIRouter()

def list_to_string(list_var):
    string = ' '.join(item for item in list_var)
    return string

async def get_movies():
    media_cursor = db.movieDb.find({})
    media = await media_cursor.to_list(length=5000)
    return media

async def get_series():
    media_cursor = db.seriesDb.find({})
    media = await media_cursor.to_list(length=5000)
    return media

async def save_similarities(series: bool = False):
    if series:
        media = await get_series()

        ids = []
        important_features = []
        i = 0
        for med in media:
            name = med['name']
            countries = list_to_string(med['countries'])
            languages = list_to_string(med['languages'])
            genres = list_to_string(med['genres'])
            stars = list_to_string([star['name'] for star in med['crew']['stars']])
            creators = list_to_string(med['creators'])

            ids.append(i)
            if creators:
                important_features.append(
                    f'{name} {countries} {languages} {genres} {stars} {creators}')
            else:
                important_features.append(
                    f'{name} {countries} {languages} {genres} {stars}')

            i = i + 1
    else:
        media = await get_movies()

        ids = []
        important_features = []

        i = 0
        for med in media:
            name = med['name']
            countries = list_to_string(med['countries'])
            languages = list_to_string(med['languages'])
            genres = list_to_string(med['genres'])
            stars = list_to_string([star['name'] for star in med['crew']['stars']])
            directors = list_to_string(med['crew']['directors'])

            ids.append(i)
            important_features.append(
                f'{name} {countries} {languages} {genres} {stars} {directors}')
            
            i = i + 1

    data = {
        'id':  ids,
        'important_features': important_features
    }

    df = pd.DataFrame (data, columns = ['id' , 'important_features'])

    cm = CountVectorizer().fit_transform(df['important_features'])
    cs = cosine_similarity(cm)

    if series:
        np.save('series_similarities.npy',cs)
    else:
        np.save('movies_similarities.npy',cs)

async def get_similar_movies(ids: List[str]):
    specified_media = [await db.movieDb.find_one({'imdb_id' : id}) for id in ids]
    if specified_media[0] == None:
        specified_media = [await db.seriesDb.find_one({'imdb_id' : id}) for id in ids]
        if specified_media[0] == None:
            raise HTTPException(status_code=400, detail='media does not exist')
        else:
            media = await get_series()
            specified_media_indexes = [media.index(med) for med in specified_media]
            cs =  np.load('series_similarities.npy')
    else:
        media = await get_movies()
        specified_media_indexes = [media.index(med) for med in specified_media]
        cs = np.load('movies_similarities.npy')

    scores_list = [list(enumerate(cs[specified_media_index])) for specified_media_index in specified_media_indexes]

    sorted_scores = [sorted(scores , key = lambda x:x[1] ,  reverse=True) for scores in scores_list]
    sorted_scores = [sorted[1:] for sorted in sorted_scores]

    recommendeds = [[MiniMedia(**media[item[0]]) for item in sorted[:10]] for sorted in sorted_scores]
    return recommendeds

@router.get('/save_movies_similarities')
async def save_movies_semilarities():
    await save_similarities()

@router.get('/save_series_similarities')
async def save_series_semilarities():
    await save_similarities(True)

@router.get('/similars/{id}')
async def similar_medias(id: str):
    recommendeds = await get_similar_movies([id])
    return recommendeds[0]

@router.get('/users_suggestion/{id}')
async def similar_medias(id: str , media_type: str):
    id = uuid.UUID(id).bytes
    user = await db.usersDb.find_one({"id": Binary(bytes(bytearray(id)), UUID_SUBTYPE)})
    if user['loved']:
        if media_type == "movie":
            loved_movies = [med['imdb_id'] for med in user['loved'] if med['media_type'] == 'movie']
            if len(loved_movies) > 3:
                recommendeds = await get_similar_movies(loved_movies[-7:])
                return recommendeds
                
        elif media_type == "series":
            loved_series = [med['imdb_id'] for med in user['loved'] if med['media_type'] == 'series']    
            if len(loved_series) > 3:
                recommendeds = await get_similar_movies(loved_series[-7:])
                return recommendeds
