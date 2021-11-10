import json

async def subscriptions_get(client):
    response = await client.get(f'/plans')
    if response.status_code != 200:
        return None
    else:
        return response.json()


async def subscription_post(payload, client):
    payload = json.dumps(payload)
    response = await client.post(f'/plan', data=payload)
    if response.status_code != 200:
        return None
    else:
        return response.json()


async def subscription_put(sub_days , payload, client):
    payload = json.dumps(payload)
    response = await client.put(f'/plan/{sub_days}', data=payload)
    if response.status_code != 200:
        return False
    else:
        return True

async def subscription_delete(sub_days , client):
    response = await client.delete(f'/plan/{sub_days}')
    if response.status_code != 204:
        return False
    else:
        return True
