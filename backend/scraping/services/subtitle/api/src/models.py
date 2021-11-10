from pydantic import BaseModel
from typing import List

class SubInputs(BaseModel):
    name: str
    year: int

class SubInputsList(BaseModel):
    sub_list: List[SubInputs]