from pydantic import BaseModel, EmailStr
from datetime import date

class FloorCreate(BaseModel):
    floor_name: str
    restaurant_id: int

class FloorResponse(BaseModel):
    floor_id: int
    floor_name: str
    restaurant_id: int
    floor_created_date: date

    class Config:
        from_attributes = True
