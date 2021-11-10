import json

async def coupons_get_one(name, client):
    response = client.get(f'/coupon/get/coupon/{name}') 
    if response.status_code != 200:
        return None
    return response.json()

async def coupons_get(client):
    response = client.get(f'/coupon/get/coupons')
    if response.status_code != 200:
        return None
    return response.json()

async def coupons_post(payload, client):
    payload = json.dumps(payload)
    response = client.post('/coupon/add/coupon' , data = payload)
    if response.status_code != 200:
        return False
    return True

async def coupons_delete(name , client):
    response = client.delete(f'/coupon/delete/coupon/{name}')
    if response.status_code != 204:
        return False
    return True
