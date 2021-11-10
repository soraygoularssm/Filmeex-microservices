import json

async def suggestions_get(client , id):
    response = await client.get(f'/similars/{id}')
    if response.status_code != 200:
        return None
    else:
        return response.json()