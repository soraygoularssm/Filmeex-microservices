from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING
from .mongodb import db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient('mongodb://cast_db:27017')
    db.castDb = db.client.filmix.cast

    #indexing
    cast_index = IndexModel([("imdb_id", ASCENDING)], unique=True)
    await db.castDb.create_indexes([cast_index])


async def close_mongo_connection():
    db.client.close()
