from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING
from .mongodb import db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient('mongodb://filters_db:27017')
    db.genreDb = db.client.filmix.genre
    db.categoryDb = db.client.filmix.category
    db.sliderDb = db.client.filmix.slider

    #indexing
    genre_index = IndexModel([("genre_name", ASCENDING)], unique=True)
    category_index = IndexModel([("category_name", ASCENDING)], unique=True)

    await db.genreDb.create_indexes([genre_index])
    await db.categoryDb.create_indexes([category_index])

async def close_mongo_connection():
    db.client.close()
