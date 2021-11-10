from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None
    movieDb = None
    seriesDb = None

db = DataBase()
