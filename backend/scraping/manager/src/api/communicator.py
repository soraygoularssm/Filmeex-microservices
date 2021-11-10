import httpx
import json
from . import services as sc


def url_discovery(service):
    serv = httpx.get(
        f'http://discovery_service:8000/discovery/services/{service}')
    serv = json.loads(serv.text)['url']
    return serv

try:
    media_crawler = url_discovery('media_crawler')
    imdb_crawler = url_discovery('imdb_crawler')
    subtitle_crawler = url_discovery('subtitle_crawler')
    media_service = url_discovery('media')
except:
    pass

async def remove_existing_media(content_type , media):
    async with httpx.AsyncClient(base_url=media_service) as client:
        not_existing_media = []
        for med in media:
            if content_type == 'series':
                if not await sc.series_exist(client, med):
                    not_existing_media.append(med)
            else:
                if not await sc.movies_exist(client, med):
                    not_existing_media.append(med)
    return not_existing_media

def get_five_pages(content_type, start):
    with httpx.Client(base_url=media_crawler, timeout=None) as client:
        payload = {'start': start, 'end': 4}
        response = sc.media_get(client, payload, content_type)
    return response

def get_five_pages_imdb_info(media, tv=False):
    with httpx.Client(base_url=imdb_crawler, timeout=None) as client:
        if tv:
            imdb = sc.imdb_series(client)
        else:
            imdb = sc.imdb_movie(client)

    info = imdb.details_get(media)
    return info

def get_five_pages_subtitles(sub_inputs):
    payload = {'sub_list': sub_inputs}
    payload = json.dumps(payload)
    with httpx.Client(base_url=subtitle_crawler, timeout=None) as client:
        response = sc.subtitle_get(client, payload)
    return response

async def add_five_pages_movie(content_type, media):
    async with httpx.AsyncClient(base_url=media_service, timeout=None) as client:
        payload = json.dumps(media)
        if content_type == 'series':
            response = await sc.series_add(client, payload)
        else:
            response = await sc.movies_add(client, payload)

    return response
