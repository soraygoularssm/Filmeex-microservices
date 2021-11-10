from fastapi import Depends, Response
from fastapi_users import FastAPIUsers
from . import security as auth_security
from . import models as auth_models
from typing import List

SECRET = "soraygoular"

fastapi_users = FastAPIUsers(
    auth_security.user_db,
    [auth_security.jwt_authentication],
    auth_models.User,
    auth_models.UserCreate,
    auth_models.UserUpdate,
    auth_models.UserDB,
)

AUTH_ROUTER = fastapi_users.get_auth_router(auth_security.jwt_authentication)

REGISTER_ROUTER = fastapi_users.get_register_router(auth_security.on_after_register)

RESET_PASWORD_ROUTER = fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=auth_security.on_after_forgot_password
    )