from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient('mongodb://subscription_db:27017')
    db.subscriptionDb = db.client.filmix.subscription


async def close_mongo_connection():
    db.client.close()