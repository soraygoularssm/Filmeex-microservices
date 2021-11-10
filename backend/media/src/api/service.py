import httpx
from typing import List
import json


def url_discovery(service):
    serv = httpx.get(
        f'http://discovery_service:8000/discovery/services/{service}')
    serv = json.loads(serv.text)['url']
    return serv


try:
    cast_service_url = url_discovery('cast')
    filters_service_url = url_discovery('filters')
    imdb_crawler_url = url_discovery('imdb_crawler')
except Exception as e:
    pass


# CAST SERVICE
async def get_cast_exist(id: str):
    async with httpx.AsyncClient(base_url=cast_service_url, timeout=None) as client:
        r = await client.get(url='/cast/' + id)
    if r.status_code != 200:
        return False
    return r.json()


async def add_cast(cast_info):
    payload = json.dumps(cast_info)
    async with httpx.AsyncClient(base_url=cast_service_url, timeout=None) as client:
        r = await client.post(url='/cast', data = payload)

    if r.status_code != 200:
        return False
    return True

async def update_cast(id , cast_info):
    payload = json.dumps(cast_info)
    async with httpx.AsyncClient(base_url=cast_service_url,  timeout=None) as client:
        await client.put(url=f'/cast/{id}' , data = payload)

# FILTERS SERVICE
async def add_genres(genres):
    payload = json.dumps(genres , ensure_ascii=False)
    async with httpx.AsyncClient(base_url=filters_service_url , timeout=None) as client:
        await client.post(url='/genres', data = payload)

# IMDB SCRAPING SERVICE
async def get_cast(cast_list):
    cast_id_list = [cast['imdb_id'] for cast in cast_list]
    payload = {'cast_ids': cast_id_list}
    payload = json.dumps(payload)
    async with httpx.AsyncClient(base_url=imdb_crawler_url, timeout=None) as client:
        cast_info = await client.post(url='/crew/details', data=payload)

    if cast_info.status_code == 200:
        cast_info_res = list()
        for cast in cast_list:
            for cast_i in cast_info.json():
                if cast['imdb_id'] == cast_i['imdb_id']:
                    cast_data = {**cast , **cast_i}

                    cast_info_res.append(cast_data)
        return cast_info_res
    else:
        return False
