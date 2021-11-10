from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING
from .mongodb import db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient('mongodb://media_db:27017')
    db.movieDb = db.client.media.movie
    db.seriesDb = db.client.media.series

    #indexing
    id_index = IndexModel([("imdb_id", ASCENDING)], unique=True)

    await db.movieDb.create_indexes([id_index])
    await db.seriesDb.create_indexes([id_index])





async def close_mongo_connection():
    db.client.close()
