import json

async def services_get_one(client , name):
    response = client.get(f'/discovery/services/{name}') 
    if response.status_code != 200:
        return None
    return response.json()

async def services_post(client , payload):
    payload = json.dumps(payload)
    response = client.post('/discovery/services' , data = payload)
    if response.status_code != 200:
        return False
    return True

async def services_put(client , name , payload):
    payload = json.dumps(payload)
    response = client.post(f'/discovery/services/{name}' , data = payload)
    if response.status_code != 200:
        return False
    return True

async def services_delete(client , name):
    response = client.delete(f'/discovery/services/{name}')
    if response.status_code != 204:
        return False
    return True
