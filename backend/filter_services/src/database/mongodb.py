from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None
    genreDb = None
    categoryDb= None
    sliderDb = None

db = DataBase()
