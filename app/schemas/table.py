from pydantic import BaseModel, EmailStr
from datetime import date

class TableCreate(BaseModel):
    floor_id: int
    table_number: str
    table_capacity: int
    table_created_date: date

class TableResponse(BaseModel):
    table_id: int
    floor_id: int
    table_number: str
    table_capacity: int
    table_created_date: date

    class Config:
        from_attributes = True
