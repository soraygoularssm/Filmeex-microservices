from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    mediaClient: AsyncIOMotorClient = None
    usersClient: AsyncIOMotorClient = None
    movieDb = None
    seriesDb = None
    usersDb = None

db = DataBase()

