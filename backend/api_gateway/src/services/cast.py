import json


# STAR METHODS
async def cast_get_one(client, imdb_id):
    response = await client.get(f'/cast/{imdb_id}')
    if response.status_code != 200:
        return None
    return reponse.json()


async def cast_get(client, payload):
    response = await client.get('/cast', params=payload)
    if response.status_code != 200:
        return None
    return response.json()


async def cast_post(client, payload):
    payload = json.dumps(payload)
    response = await client.post('/cast', data=json.dumps(payload))
    if response.status_code != 200:
        return False
    return True


async def cast_put(client, imdb_id, payload):
    payload = json.dumps(payload)
    response = await client.put(f'/cast/{imdb_id}', data=payload)
    if response.status_code != 200:
        return False
    return True


async def cast_delete(client, imdb_id):
    response = await client.delete(f'/cast/{imdb_id}')
    if response.status_code != 204  :
        return False
    return True
