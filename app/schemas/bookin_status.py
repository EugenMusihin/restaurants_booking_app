from pydantic import BaseModel, EmailStr
from datetime import date

class BookingStatusCreate(BaseModel):
    booking_status_name: str


class BookingStatusResponse(BaseModel):
    booking_status_id: int
    booking_status_name: str

    class Config:
        from_attributes = True
