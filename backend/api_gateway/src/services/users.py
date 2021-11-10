import json

async def users_get_one(client , id):
    response = await client.get(f'/users/{id}')
    if response.status_code != 200:
        return None
    return response.json()

async def users_get(client , payload):
    response = await client.get('/users' , params = payload)
    if response.status_code != 200:
        return None
    return response.json()

async def users_put(client , ui, payload):
    payload = json.dumps(payload , ensure_ascii=False)
    response = await client.put(f'/users/{ui}', data=payload)
    if response.status_code != 200:
        return False
    return True

async def users_delete(client , ui):
    response = await client.put(f'/users/{ui}')
    if response.status_code != 204:
        return False
    return True
