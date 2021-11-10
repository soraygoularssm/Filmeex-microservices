import json
# MOVIE METHODS


async def movies_get_one(client, imdb_id):
    response = await client.get(f'/movies/{imdb_id}')
    if response.status_code != 200:
        return None
    else:
        return response.json()


async def movies_get(client, payload):
    response = await client.get('/movies', params=payload)
    if response.status_code != 200:
        return None
    return response.json()


async def movies_post(client, payload):
    payload = json.dumps(payload)
    response = await client.post('/movies', data=payload)
    if response.status_code != 200:
        return False
    return True


async def movies_put(client, imdb_id, payload):
    payload = json.dumps(payload)
    response = await client.put(f'/movies', params={'id': imdb_id}, data=payload)
    if response.status_code != 200:
        return False
    return True


async def movies_delete(client, imdb_id):
    response = await client.delete(f'/movies/{imdb_id}')
    if response.status_code != 204:
        return False
    return True

# SERIES METHODS
async def series_get_one(client, imdb_id):
    response = await client.get(f'/series/{imdb_id}')
    if response.status_code != 200:
        return None
    else:
        return response.json()


async def series_get(client, payload):
    response = await client.get('/series', params=payload)
    if response.status_code != 200:
        return None
    return response.json()


async def series_post(client, payload):
    payload = json.dumps(payload)
    response = await client.post('/series', data=payload)
    if response.status_code != 200:
        return False
    return True


async def series_put(client, imdb_id, payload):
    payload = json.dumps(payload)
    response = await client.put(f'/series',  params={'id': imdb_id}, data=payload)
    if response.status_code != 200:
        return False
    return True


async def series_delete(client, imdb_id):
    response = await client.delete(f'/series/{imdb_id}')
    if response.status_code != 204:
        return False
    return True
