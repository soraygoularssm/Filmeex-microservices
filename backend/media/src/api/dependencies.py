from fastapi import Depends
from pydantic import Json
from typing import Optional
import json

class GetQueryParams:
    def __init__(self, q: Json, page: int = 1, limit: int = 50):
        self.q = q
        self.page = (page - 1) * limit
        self.limit = limit
