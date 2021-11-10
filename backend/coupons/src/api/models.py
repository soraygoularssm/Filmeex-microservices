from pydantic import BaseModel
import datetime

class Coupon(BaseModel):
    name: str
    discount: int
    expires_at: datetime.date
