from auth.authentication import fastapi_users
from fastapi import Depends
from pydantic import Json
from typing import Optional
import json

class GetQueryParams:
    def __init__(self, q: Json, page: int = None, limit: int = None):
        payload = {
            'q': json.dumps(q)
        }
        if limit:
            payload.update({'limit': limit})
        if page:
            payload.update({'page': page})
        
        self.payload = payload

get_current_user = fastapi_users.get_current_user
get_current_active_user = fastapi_users.get_current_active_user
get_optional_current_user = fastapi_users.get_optional_current_user
get_optional_current_active_user = fastapi_users.get_optional_current_active_user
get_current_superuser = fastapi_users.get_current_superuser
get_optional_current_superuser = fastapi_users.get_optional_current_superuser