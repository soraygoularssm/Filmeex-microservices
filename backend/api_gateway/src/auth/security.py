from fastapi import Request
import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase
from .models import UserDB
from fastapi_users.authentication import JWTAuthentication

DATABASE_URL = "mongodb://users_db:27017"
SECRET = "SECRET"

client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["users"]
collection = db["users_collection"]
user_db = MongoDBUserDatabase(UserDB, collection)

def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")

jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds= 2592000, tokenUrl="/auth/jwt/login"
)