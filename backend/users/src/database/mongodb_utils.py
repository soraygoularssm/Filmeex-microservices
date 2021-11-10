from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING
from .mongodb import db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient('mongodb://users_db:27017')
    db.usersDb = db.client.users.users_collection

    #indexing
    # email_index = IndexModel([("email", ASCENDING)], unique=True , partialFilterExpression = {"Values": None})
    # phone_index = IndexModel([("phone", ASCENDING)], unique=True , partialFilterExpression = {"Values": None})

    # await db.usersDb.create_indexes([email_index , phone_index])


async def close_mongo_connection():
    db.client.close()
