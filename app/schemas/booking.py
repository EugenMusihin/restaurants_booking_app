from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime, timezone

class BookingCreate(BaseModel):
    user_id: int
    table_id: int
    booking_date: date
    booking_start_hours: int
    booking_end_hours: int
    booking_start_minutes: int
    booking_end_minutes: int
    booking_status_id: int
    booking_created_date: date

class BookingResponse(BaseModel):
    booking_id: int
    booking_date: date
    booking_start_hours: int
    booking_end_hours: int
    booking_start_minutes: int
    booking_end_minutes: int
    booking_created_date: date
    table_name: str
    restaurant_name: str
    user_id: int
    booking_status_id: int

    class Config:
        from_attributes = True
class BookingStatusUpdate(BaseModel):
    booking_status_id: int