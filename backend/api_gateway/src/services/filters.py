import json

# CATEGORY METHODS
async def categories_get(client):
    response = await client.get('/categories')
    if response.status_code != 200:
        return None
    return response.json()

async def categories_post(client , payload):
    response = await client.post('/categories' , data = json.dumps(payload))
    if response.status_code != 200:
        return False
    return True

async def categories_put(client , category ,payload):
    response = await client.put(f'/categories/{category}' , data = json.dumps(payload))
    if response.status_code != code:
        return False
    return True

async def categories_delete(cliet , category):
    response = await cliet.delete(f'/categories/{category}')
    if response.status_code != 204:
        return False
    return True



# GENRE METHODS
async def genres_get(client):
    response = await client.get('/genres')
    if response.status_code != 200:
        return None
    return response.json()

async def genres_post(client , payload):
    response = await client.post('/genres' , data = json.dumps(payload))
    if response.status_code != 200:
        return False
    return True

async def genres_put(client , genre ,payload):
    response = await client.put(f'/genres/{genre}' , data = json.dumps(payload))
    if response.status_code != code:
        return False
    return True

async def genres_delete(cliet , genre):
    response = await cliet.delete(f'/genres/{genre}')
    if response.status_code != 204:
        return False
    return True



# SLIDER METHODS
async def sliders_get(client , payload = None):
    if payload:
        response = await client.get('/sliders', params = payload)
    response = await client.get('/sliders')
    if response.status_code != 200:
        return None
    return response.json()

async def sliders_post(client , payload):
    payload = json.dumps(payload)
    response = await client.post('/sliders' , data = payload)
    if response.status_code != 200:
        return False
    return True

async def sliders_put(client , slider ,payload):
    payload = json.dumps(payload)
    response = await client.put(f'/sliders/{slider}' , data = payload)
    if response.status_code != code:
        return False
    return True

async def sliders_delete(cliet , slider):
    response = await cliet.delete(f'/sliders/{slider}')
    if response.status_code != 204:
        return False
    return True