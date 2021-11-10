from fastapi import FastAPI
from .tools.retriver import retrive_data
from .models import SubInputsList
import json

app = FastAPI()

@app.post('/subtitle')
async def get_subtitle(body: SubInputsList):
    search_url = f'http://moviesubtitles.xyz'
    sub_list = body.dict()
    meta = sub_list

    subtitles = retrive_data(search_url,'find_list_of_sub', meta=meta)

    return subtitles 
