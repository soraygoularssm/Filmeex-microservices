import json

# scraping
# movies
def media_get(client, payload , content_type):
    response = client.get(f'/{content_type}', params=payload)
    if response.status_code != 200:
        return None
    return response.json()

# imdb
class imdb_movie:
    def __init__(self , client):
        self.client = client

    def tp250_get(self):
        response = self.client.get('/movies/top250')
        if response.status_code != 200:
            return None
        return response.json()

    def details_get(self, movies):
        payload = {
            'imdb_ids': movies
        }
        response = self.client.post(f'/movies/details' , data=json.dumps(payload))
        if response.status_code != 200:
            return None
        return response.json()

    def images_get(self, id):
        response = self.client.get(f'/movies/imgs/{id}')
        if response.status_code != 200:
            return None
        return response.json()

    def crew_headshot_get(self, id):
        response = self.client.get(f'/crew/headshot/{id}')
        if response.status_code != 200:
            return None
        return response.json()

class imdb_series:
    def __init__(self , client):
        self.client = client
    
    def tp250_get(self):
        response = self.client.get('/series/top250')
        if response.status_code != 200:
            return None
        return response.json()

    def details_get(self, series):
        payload = {
            'imdb_ids': series
        }
        response = self.client.post(f'/series/details' , data=json.dumps(payload))
        if response.status_code != 200:
            return None
        return response.json()

    def images_get(self, id):
        response = self.client.get(f'/series/imgs/{id}')
        if response.status_code != 200:
            return None
        return response.json()

# subtitle
def subtitle_get(client, payload):
    response = client.post('/subtitle', data=payload)
    if response.status_code != 200:
        return None
    return response.json()

# microservice
# movies
async def movies_add(client, payload):
    response = await client.post('/movies', data=payload)
    if response.status_code != 200:
        return False
    return True

async def movies_exist(client, imdb_id):
    response = await client.get(f'/movies/{imdb_id}')
    if response.status_code != 200:
        return False
    return True

# series
async def series_add(client, payload):
    response = await client.post('/series', data=payload)
    if response.status_code != 200:
        return False
    return True

async def series_exist(client, imdb_id):
    response = await client.get(f'/series/{imdb_id}')
    if response.status_code != 200:
        return False
    return True