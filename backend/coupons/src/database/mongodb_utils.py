from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient('mongodb://localhost:27017')
    db.movieDb = db.client.coupon.movie


async def close_mongo_connection():
    db.client.close()