from fastapi import FastAPI
from api import users
from database import mongodb_utils

app = FastAPI()

app.add_event_handler("startup", mongodb_utils.connect_to_mongo)
app.add_event_handler("shutdown", mongodb_utils.close_mongo_connection)

app.include_router(users.router)