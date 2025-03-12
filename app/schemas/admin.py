from pydantic import BaseModel
from datetime import date


class AdminCreate(BaseModel):
    user_id: int
    restaurant_id: int
    admin_created_date: date

class AdminResponse(BaseModel):
    admin_id: int
    user_id: int
    restaurant_id: int
    admin_created_date: date

    class Config:
        from_attributes = True
