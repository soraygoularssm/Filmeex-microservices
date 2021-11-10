from fastapi import FastAPI
from api import media
from database import mongodb_utils

app = FastAPI()

app.add_event_handler("startup", mongodb_utils.connect_to_mongo)
app.add_event_handler("shutdown", mongodb_utils.close_mongo_connection)

app.include_router(media.movie_router , tags=['movies'])
app.include_router(media.series_router , tags=['series']) 