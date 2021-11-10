from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING
from .mongodb import db

async def connect_to_mongo():
    db.mediaClient = AsyncIOMotorClient('mongodb://media_db:27017')
    db.movieDb = db.mediaClient.media.movie
    db.seriesDb = db.mediaClient.media.series

    db.usersClient = AsyncIOMotorClient('mongodb://users_db:27017')
    db.usersDb = db.usersClient.users.users_collection



async def close_mongo_connection():
    db.client.close()

