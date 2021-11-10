from fastapi import APIRouter , HTTPException , Form
import json

router = APIRouter()

@router.get('/services/{service}' ,  status_code=200)
async def get_services(service: str):
    with open('api/addresses.json') as f:
        data = json.load(f)
    try:
        address = data[service]
        return {'url': address}
    except:
        raise HTTPException(status_code = 404 , detail = 'service not found')
    
@router.post('/services' , status_code=200)
async def add_services(name: str = Form(...) , address: str = Form(...)):
    try:
        with open('api/addresses.json') as f:
            data = json.load(f)
        
        data[name] = address

        with open('api/addresses.json' , 'w') as f:
            json.dump(data, f)
        return {'detail':'service added'}
    except:
        raise HTTPException(status_code=400,detail='could not add the address')

@router.put('/services/{service}' , status_code=200)
async def update_services(service: str , name: str = Form(None) , address: str = Form(None)):
    try:
        with open('api/addresses.json') as f:
            data = json.load(f)

        if not address:
            address = data[service]
        
        if name:
            if service != name:
                del data[service]
        else:
            name = service

        data[name] = address

        with open('api/addresses.json' , 'w') as f:
            json.dump(data, f)
        return {'detail':'service updated'}
    except:
        raise HTTPException(status_code=400,detail='could not update the address')

@router.delete('/services/{service}' , status_code=204)
async def update_services(service: str):
    try:
        with open('api/addresses.json') as f:
            data = json.load(f)
        
        del data[service]

        with open('api/addresses.json' , 'w') as f:
            json.dump(data, f)
        return None
    except:
        raise HTTPException(status_code=404)